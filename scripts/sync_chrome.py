# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Sync the Chrome source code used by Chrome OS to the specified directory."""

from __future__ import print_function

import functools
import os

from chromite.cbuildbot import constants
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import gclient
from chromite.lib import osutils


def GetParser():
  """Creates the argparse parser."""
  parser = commandline.ArgumentParser(description=__doc__)

  version = parser.add_mutually_exclusive_group()
  version.add_argument('--tag', help='Sync to specified Chrome release',
                       dest='version')
  version.add_argument('--revision', help='Sync to specified git revision',
                       dest='version')

  parser.add_argument('--internal', help='Sync internal version of Chrome',
                      action='store_true', default=False)
  parser.add_argument('--reset', help='Revert local changes',
                      action='store_true', default=False)
  parser.add_argument('--gclient', help=commandline.argparse.SUPPRESS,
                      default=None)
  parser.add_argument('--gclient_template', help='Template gclient input file')
  parser.add_argument('chrome_root', help='Directory to sync chrome in')

  return parser


def SyncChrome(gclient_path, options):
  """Sync new Chrome."""
  gclient.WriteConfigFile(gclient_path, options.chrome_root,
                          options.internal, options.version,
                          options.gclient_template)
  return functools.partial(
      gclient.Sync, gclient_path, options.chrome_root, reset=options.reset)


def main(argv):
  parser = GetParser()
  options = parser.parse_args(argv)

  if options.gclient is '':
    parser.error('--gclient can not be an empty string!')
  gclient_path = options.gclient or osutils.Which('gclient')
  if not gclient_path:
    gclient_path = os.path.join(constants.DEPOT_TOOLS_DIR, 'gclient')

  try:
    if options.reset:
      # Revert any lingering local changes.
      gclient.Revert(gclient_path, options.chrome_root)

    sync_fn = SyncChrome(gclient_path, options)
  except cros_build_lib.RunCommandError:
    # If we have an error resetting, or syncing, we clobber, and fresh sync.
    osutils.RmDir(options.chrome_root, ignore_missing=True, sudo=True)
    osutils.SafeMakedirs(options.chrome_root)
    sync_fn = SyncChrome(gclient_path, options)

  # Sync twice when run with --reset, which implies 'gclient sync -D'.
  #
  # There's a bug with 'gclient sync -D' that gets hit when the location of a
  # dependency checkout (in the DEPS file) is moved to a path that contains
  # (in a directory fashion) its old path.  E.g., when Blink is moved from
  # Webkit/Source/ to Webkit/.  When this happens, a 'gclient sync -D' will
  # blow away Webkit/Source/ after the sync, since it is no longer in the
  # DEPS file, leaving the Blink checkout missing a Source/ subdirectory.
  #
  # This bug also gets hit the other way around - E.g., if Blink moves from
  # Webkit/ to Webkit/Source/.
  #
  # To work around this, we sync twice, so that any directories deleted by
  # the first sync will be restored in the second.
  #
  # TODO(rcui): Remove this workaround when the bug is fixed in gclient, or
  # replace with a more sophisticated solution that syncs twice only when any
  # paths in the DEPS file cannot be found after initial sync.
  if options.reset:
    sync_fn()
  sync_fn()
  return 0
