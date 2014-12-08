# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This module tests the init module."""

from __future__ import print_function

import glob
import imp

from chromite.lib import commandline
from chromite.lib import cros_build_lib_unittest
from chromite.lib import cros_test_lib
from chromite.lib import partial_mock
from chromite.cros import commands


class MockCommand(partial_mock.PartialMock):
  """Mock class for a generic cros command."""
  ATTRS = ('Run',)
  COMMAND = None
  TARGET_CLASS = None

  def __init__(self, args, base_args=None):
    partial_mock.PartialMock.__init__(self)
    self.args = args
    self.rc_mock = cros_build_lib_unittest.RunCommandMock()
    self.rc_mock.SetDefaultCmdResult()
    parser = commandline.ArgumentParser(caching=True)
    subparsers = parser.add_subparsers()
    subparser = subparsers.add_parser(self.COMMAND, caching=True)
    self.TARGET_CLASS.AddParser(subparser)

    args = base_args if base_args else []
    args += [self.COMMAND] + self.args
    options = parser.parse_args(args)
    self.inst = options.cros_class(options)

  def Run(self, inst):
    with self.rc_mock:
      self.backup['Run'](inst)


class CommandTest(cros_test_lib.MockTestCase):
  """This test class tests that we can load modules correctly."""

  # pylint: disable=W0212

  def testFindModules(self):
    """Tests that we can return modules correctly when mocking out glob."""
    fake_command_file = 'cros_command_test.py'
    filtered_file = 'cros_command_unittest.py'
    mydir = 'mydir'

    self.PatchObject(glob, 'glob',
                     return_value=[fake_command_file, filtered_file])

    self.assertEqual(commands._FindModules(mydir), [fake_command_file])

  def testLoadCommands(self):
    """Tests import commands correctly."""
    fake_command_file = 'cros_command_test.py'
    fake_module = 'cros_command_test'
    module_tuple = 'file', 'pathname', 'description'

    self.PatchObject(commands, '_FindModules', return_value=[fake_command_file])
    self.PatchObject(imp, 'find_module', return_value=module_tuple)
    load_mock = self.PatchObject(imp, 'load_module')

    commands._ImportCommands()

    load_mock.assert_called_with(fake_module, *module_tuple)
