# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Helper functions useful when writing scripts that integrate with GN.

The main functions are ToGNString() and FromGNString(), to convert between
serialized GN veriables and Python variables.

To use in an arbitrary Python file in the build:

  import os
  import sys

  sys.path.append(os.path.join(os.path.dirname(__file__),
                               os.pardir, os.pardir, 'build'))
  import gn_helpers

Where the sequence of parameters to join is the relative path from your source
file to the build directory.
"""

import os
import re
import sys


_CHROMIUM_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)

IMPORT_RE = re.compile(r'^import\("//(\S+)"\)')


class GNError(Exception):
  pass


def ToGNString(value, allow_dicts=True):
  """Returns a stringified GN equivalent of a Python value.

  Args:
    value: The Python value to convert.
    allow_dicts: Whether to enable converting dictionaries to GN scopes. This is
      only possible at the top level (GN scope cannot be nested in a list), so
      recursive calls should set this to False.

  Returns:
    The stringified GN equivalent to |value|.

  Raises:
    GNError: |value| cannot be printed to GN.
  """
  if isinstance(value, str):
    if value.find('\n') >= 0:
      raise GNError('Trying to print a string with a newline in it.')
    return '"' + \
        value.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$') + \
        '"'

  if sys.version_info.major < 3 and isinstance(value, unicode):
    return ToGNString(value.encode('utf-8'))

  if isinstance(value, bool):
    return 'true' if value else 'false'

  if isinstance(value, list):
    return '[ %s ]' % ', '.join(ToGNString(v) for v in value)

  if isinstance(value, dict):
    if not allow_dicts:
      raise GNError('Attempting to recursively print a dictionary.')
    result = ''
    for key in sorted(value):
      if not isinstance(key, str) and not isinstance(key, unicode):
        raise GNError('Dictionary key is not a string.')
      result += '%s = %s\n' % (key, ToGNString(value[key], False))
    return result

  if isinstance(value, int):
    return str(value)

  raise GNError('Unsupported type when printing to GN.')


def FromGNString(input_string):
  """Converts the input string from a GN serialized value to Python values.

  For details on supported types see GNValueParser.Parse() below.

  If your GN script did:
    something = [ "file1", "file2" ]
    args = [ "--values=$something" ]
  The command line would look something like:
    --values="[ \"file1\", \"file2\" ]"
  Which when interpreted as a command line gives the value:
    [ "file1", "file2" ]

  You can parse this into a Python list using GN rules with:
    input_values = FromGNValues(options.values)
  Although the Python 'ast' module will parse many forms of such input, it
  will not handle GN escaping properly, nor GN booleans. You should use this
  function instead.


  A NOTE ON STRING HANDLING:

  If you just pass a string on the command line to your Python script, or use
  string interpolation on a string variable, the strings will not be quoted:
    str = "asdf"
    args = [ str, "--value=$str" ]
  Will yield the command line:
    asdf --value=asdf
  The unquoted asdf string will not be valid input to this function, which
  accepts only quoted strings like GN scripts. In such cases, you can just use
  the Python string literal directly.

  The main use cases for this is for other types, in particular lists. When
  using string interpolation on a list (as in the top example) the embedded
  strings will be quoted and escaped according to GN rules so the list can be
  re-parsed to get the same result.
  """
  parser = GNValueParser(input_string)
  return parser.Parse()


def FromGNArgs(input_string):
  """Converts a string with a bunch of gn arg assignments into a Python dict.

  Given a whitespace-separated list of

    <ident> = (integer | string | boolean | <list of the former>)

  gn assignments, this returns a Python dict, i.e.:

    FromGNArgs('foo=true\nbar=1\n') -> { 'foo': True, 'bar': 1 }.

  Only simple types and lists supported; variables, structs, calls
  and other, more complicated things are not.

  This routine is meant to handle only the simple sorts of values that
  arise in parsing --args.
  """
  parser = GNValueParser(input_string)
  return parser.ParseArgs()


def UnescapeGNString(value):
  """Given a string with GN escaping, returns the unescaped string.

  Be careful not to feed with input from a Python parsing function like
  'ast' because it will do Python unescaping, which will be incorrect when
  fed into the GN unescaper.

  Args:
    value: Input string to unescape.
  """
  result = ''
  i = 0
  while i < len(value):
    if value[i] == '\\':
      if i < len(value) - 1:
        next_char = value[i + 1]
        if next_char in ('$', '"', '\\'):
          # These are the escaped characters GN supports.
          result += next_char
          i += 1
        else:
          # Any other backslash is a literal.
          result += '\\'
    else:
      result += value[i]
    i += 1
  return result


def _IsDigitOrMinus(char):
  return char in '-0123456789'


class GNValueParser(object):
  """Duplicates GN parsing of values and converts to Python types.

  Normally you would use the wrapper function FromGNValue() below.

  If you expect input as a specific type, you can also call one of the Parse*
  functions directly. All functions throw GNError on invalid input.
  """

  def __init__(self, string, checkout_root=_CHROMIUM_ROOT):
    self.input = string
    self.cur = 0
    self.checkout_root = checkout_root

  def IsDone(self):
    return self.cur == len(self.input)

  def ReplaceImports(self):
    """Replaces import(...) lines with the contents of the imports.

    Recurses on itself until there are no imports remaining, in the case of
    nested imports.
    """
    lines = self.input.splitlines()
    if not any(line.startswith('import(') for line in lines):
      return
    for line in lines:
      if not line.startswith('import('):
        continue
      regex_match = IMPORT_RE.match(line)
      if not regex_match:
        raise GNError('Not a valid import string: %s' % line)
      import_path = os.path.join(self.checkout_root, regex_match.group(1))
      with open(import_path) as f:
        imported_args = f.read()
      self.input = self.input.replace(line, imported_args)
    # Call ourselves again if we've just replaced an import() with additional
    # imports.
    self.ReplaceImports()


  def ConsumeWhitespace(self):
    while not self.IsDone() and self.input[self.cur] in ' \t\n':
      self.cur += 1

  def ConsumeComment(self):
    if self.IsDone() or self.input[self.cur] != '#':
      return

    # Consume each comment, line by line.
    while not self.IsDone() and self.input[self.cur] == '#':
      # Consume the rest of the comment, up until the end of the line.
      while not self.IsDone() and self.input[self.cur] != '\n':
        self.cur += 1
      # Move the cursor to the next line (if there is one).
      if not self.IsDone():
        self.cur += 1

  def Parse(self):
    """Converts a string representing a printed GN value to the Python type.

    See additional usage notes on FromGNString() above.

    * GN booleans ('true', 'false') will be converted to Python booleans.

    * GN numbers ('123') will be converted to Python numbers.

    * GN strings (double-quoted as in '"asdf"') will be converted to Python
      strings with GN escaping rules. GN string interpolation (embedded
      variables preceded by $) are not supported and will be returned as
      literals.

    * GN lists ('[1, "asdf", 3]') will be converted to Python lists.

    * GN scopes ('{ ... }') are not supported.

    Raises:
      GNError: Parse fails.
    """
    result = self._ParseAllowTrailing()
    self.ConsumeWhitespace()
    if not self.IsDone():
      raise GNError("Trailing input after parsing:\n  " + self.input[self.cur:])
    return result

  def ParseArgs(self):
    """Converts a whitespace-separated list of ident=literals to a dict.

    See additional usage notes on FromGNArgs(), above.

    Raises:
      GNError: Parse fails.
    """
    d = {}

    self.ReplaceImports()
    self.ConsumeWhitespace()
    self.ConsumeComment()
    while not self.IsDone():
      ident = self._ParseIdent()
      self.ConsumeWhitespace()
      if self.input[self.cur] != '=':
        raise GNError("Unexpected token: " + self.input[self.cur:])
      self.cur += 1
      self.ConsumeWhitespace()
      val = self._ParseAllowTrailing()
      self.ConsumeWhitespace()
      self.ConsumeComment()
      self.ConsumeWhitespace()
      d[ident] = val

    return d

  def _ParseAllowTrailing(self):
    """Internal version of Parse() that doesn't check for trailing stuff."""
    self.ConsumeWhitespace()
    if self.IsDone():
      raise GNError("Expected input to parse.")

    next_char = self.input[self.cur]
    if next_char == '[':
      return self.ParseList()
    elif _IsDigitOrMinus(next_char):
      return self.ParseNumber()
    elif next_char == '"':
      return self.ParseString()
    elif self._ConstantFollows('true'):
      return True
    elif self._ConstantFollows('false'):
      return False
    else:
      raise GNError("Unexpected token: " + self.input[self.cur:])

  def _ParseIdent(self):
    ident = ''

    next_char = self.input[self.cur]
    if not next_char.isalpha() and not next_char=='_':
      raise GNError("Expected an identifier: " + self.input[self.cur:])

    ident += next_char
    self.cur += 1

    next_char = self.input[self.cur]
    while next_char.isalpha() or next_char.isdigit() or next_char=='_':
      ident += next_char
      self.cur += 1
      next_char = self.input[self.cur]

    return ident

  def ParseNumber(self):
    self.ConsumeWhitespace()
    if self.IsDone():
      raise GNError('Expected number but got nothing.')

    begin = self.cur

    # The first character can include a negative sign.
    if not self.IsDone() and _IsDigitOrMinus(self.input[self.cur]):
      self.cur += 1
    while not self.IsDone() and self.input[self.cur].isdigit():
      self.cur += 1

    number_string = self.input[begin:self.cur]
    if not len(number_string) or number_string == '-':
      raise GNError('Not a valid number.')
    return int(number_string)

  def ParseString(self):
    self.ConsumeWhitespace()
    if self.IsDone():
      raise GNError('Expected string but got nothing.')

    if self.input[self.cur] != '"':
      raise GNError('Expected string beginning in a " but got:\n  ' +
                    self.input[self.cur:])
    self.cur += 1  # Skip over quote.

    begin = self.cur
    while not self.IsDone() and self.input[self.cur] != '"':
      if self.input[self.cur] == '\\':
        self.cur += 1  # Skip over the backslash.
        if self.IsDone():
          raise GNError('String ends in a backslash in:\n  ' + self.input)
      self.cur += 1

    if self.IsDone():
      raise GNError('Unterminated string:\n  ' + self.input[begin:])

    end = self.cur
    self.cur += 1  # Consume trailing ".

    return UnescapeGNString(self.input[begin:end])

  def ParseList(self):
    self.ConsumeWhitespace()
    if self.IsDone():
      raise GNError('Expected list but got nothing.')

    # Skip over opening '['.
    if self.input[self.cur] != '[':
      raise GNError('Expected [ for list but got:\n  ' + self.input[self.cur:])
    self.cur += 1
    self.ConsumeWhitespace()
    if self.IsDone():
      raise GNError('Unterminated list:\n  ' + self.input)

    list_result = []
    previous_had_trailing_comma = True
    while not self.IsDone():
      if self.input[self.cur] == ']':
        self.cur += 1  # Skip over ']'.
        return list_result

      if not previous_had_trailing_comma:
        raise GNError('List items not separated by comma.')

      list_result += [ self._ParseAllowTrailing() ]
      self.ConsumeWhitespace()
      if self.IsDone():
        break

      # Consume comma if there is one.
      previous_had_trailing_comma = self.input[self.cur] == ','
      if previous_had_trailing_comma:
        # Consume comma.
        self.cur += 1
        self.ConsumeWhitespace()

    raise GNError('Unterminated list:\n  ' + self.input)

  def _ConstantFollows(self, constant):
    """Checks and maybe consumes a string constant at current input location.

    Param:
      constant: The string constant to check.

    Returns:
      True if |constant| follows immediately at the current location in the
      input. In this case, the string is consumed as a side effect. Otherwise,
      returns False and the current position is unchanged.
    """
    end = self.cur + len(constant)
    if end > len(self.input):
      return False  # Not enough room.
    if self.input[self.cur:end] == constant:
      self.cur = end
      return True
    return False
