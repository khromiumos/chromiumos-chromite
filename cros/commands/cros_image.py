# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Build an image."""

from __future__ import print_function

import os

from chromite.cbuildbot import constants
from chromite.lib import cros_build_lib
from chromite import cros


IMAGE_TYPES = ['base', 'dev', 'test', 'factory_test', 'factory_install', []]


@cros.CommandDecorator('image')
class ImageCommand(cros.CrosCommand):
  """Create an image

  Creates an image from the specified board.
  """
  @classmethod
  def AddParser(cls, parser):
    super(ImageCommand, cls).AddParser(parser)
    parser.set_defaults(usage='Create an image')
    parser.add_argument('--adjust_part', help="Adjustments to apply to "
                        "partition table (LABEL:[+-=]SIZE) e.g. ROOT-A:+1G.")
    parser.add_argument('--board', help="The board to build an image for.")
    parser.add_argument('--boot_args', help="Additional boot arguments to pass "
                        "to the commandline")
    parser.add_argument('--enable_bootcache', default=False, type='bool',
                        help="Default all bootloaders to use boot cache.")
    parser.add_argument('--enable_rootfs_verification', default=True,
                        type='bool', help="Default all bootloaders to use "
                        "kernel-based root fs integrity checking.")
    parser.add_argument('--output_root', type='path', help="Directory in which "
                        "to place image result directories (named by version)")
    parser.add_argument('--disk_layout',
                        help="The disk layout type to use for this image.")
    parser.add_argument('--enable_serial', help="Enable serial port for "
                        "printk() calls. Example values: ttyS0")
    parser.add_argument('--kernel_log_level', default=7, type=int,
                        help="The log level to add to the kernel command line.")
    parser.add_argument('image_types', nargs='*', choices=IMAGE_TYPES,
                        default=None, help="The image types to build.")

  def Run(self):
    self.options.Freeze()

    cmd = [os.path.join(constants.CROSUTILS_DIR, 'build_image')]

    if self.options.board:
      cmd.append('--board=%s' % self.options.board)

    if self.options.adjust_part:
      cmd.append('--adjust_part=%s' % self.options.adjust_part)

    if self.options.boot_args:
      cmd.append('--boot_args=%s' % self.options.boot_args)

    if self.options.enable_bootcache:
      cmd.append('--enable_bootcache')
    else:
      cmd.append('--noenable_bootcache')

    if self.options.enable_rootfs_verification:
      cmd.append('--enable_rootfs_verification')
    else:
      cmd.append('--noenable_rootfs_verification')

    if self.options.output_root:
      cmd.append('--output_root=%s' % self.options.output_root)

    if self.options.disk_layout:
      cmd.append('--disk_layout=%s' % self.options.disk_layout)

    if self.options.enable_serial:
      cmd.append('--enable_serial=%s' % self.options.enable_serial)

    if self.options.kernel_log_level:
      cmd.append('--loglevel=%s' % self.options.kernel_log_level)

    if self.options.image_types:
      cmd.extend(self.options.image_types)

    cros_build_lib.RunCommand(cmd)
