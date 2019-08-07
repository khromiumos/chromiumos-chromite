# -*- coding: utf-8 -*-
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for device.py"""

from __future__ import print_function

from chromite.lib import cros_test_lib
from chromite.lib import device
from chromite.lib import vm


class DeviceTester(cros_test_lib.RunCommandTestCase):
  """Test device.Device."""

  def setUp(self):
    """Common set up method for all tests."""
    opts = device.Device.GetParser().parse_args([])
    self._device = device.Device(opts)

  def CreateDevice(self, device_name, is_vm):
    """Creates a device.

    Args:
      device_name: Name of the device.
      is_vm: If True, then created device should be a VM.
    """
    self._device.device = device_name
    created_device = device.Device.Create(
        vm.VM.GetParser().parse_args(['--device', device_name]))
    self.assertEqual(isinstance(created_device, vm.VM), is_vm)
    self.assertEqual(self._device.is_vm, is_vm)

  def testRunCmd(self):
    """Verify that a command is run via RunCommand."""
    self._device.RunCommand(['/usr/local/autotest/bin/vm_sanity'])
    self.assertCommandContains(['sudo'], expected=False)
    self.assertCommandCalled(['/usr/local/autotest/bin/vm_sanity'])

  def testRunCmdDryRun(self):
    """Verify that a command is run while dry running for debugging."""
    self._device.dry_run = True
    # Look for dry run command in output.
    with cros_test_lib.LoggingCapturer() as logs:
      self._device.RunCommand(['echo', 'Hello'])
    self.assertTrue(logs.LogsContain('[DRY RUN] echo Hello'))

  def testRunCmdSudo(self):
    """Verify that a command is run via sudo."""
    self._device.use_sudo = True
    self._device.RunCommand(['mount', '-o', 'remount,rw', '/'])
    self.assertCommandCalled(['sudo', '--', 'mount', '-o', 'remount,rw', '/'])

  def testCreate(self):
    """Verify Device/VM creation."""
    # Verify a VM is created by default.
    self.CreateDevice(None, True)
    # Verify a VM is created when IP is localhost.
    self.CreateDevice('localhost', True)
    # Verify a Device is created when an IP is specified.
    self.CreateDevice('190.0.2.130', False)