# -*- coding: utf-8 -*-
# Copyright 2019 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test controller.

Handles all testing related functionality, it is not itself a test.
"""

from __future__ import print_function

import os

from chromite.api import controller
from chromite.api.controller import controller_util
from chromite.api.gen.chromite.api import test_pb2
from chromite.lib import build_target_util
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import image_lib
from chromite.lib import osutils
from chromite.lib import sysroot_lib
from chromite.scripts import cros_set_lsb_release
from chromite.service import test


def DebugInfoTest(input_proto, _output_proto):
  """Run the debug info tests."""
  sysroot_path = input_proto.sysroot.path
  target_name = input_proto.sysroot.build_target.name

  if not sysroot_path:
    if target_name:
      sysroot_path = cros_build_lib.GetSysroot(target_name)
    else:
      cros_build_lib.Die("The sysroot path or the sysroot's build target name "
                         'must be provided.')

  # We could get away with out this, but it's a cheap check.
  sysroot = sysroot_lib.Sysroot(sysroot_path)
  if not sysroot.Exists():
    cros_build_lib.Die('The provided sysroot does not exist.')

  if test.DebugInfoTest(sysroot_path):
    return controller.RETURN_CODE_SUCCESS
  else:
    return controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY


def BuildTargetUnitTest(input_proto, output_proto):
  """Run a build target's ebuild unit tests."""
  # Required args.
  board = input_proto.build_target.name
  result_path = input_proto.result_path

  if not board:
    cros_build_lib.Die('build_target.name is required.')
  if not result_path:
    cros_build_lib.Die('result_path is required.')

  # Method flags.
  # An empty sysroot means build packages was not run. This is used for
  # certain boards that need to use prebuilts (e.g. grunt's unittest-only).
  was_built = not input_proto.flags.empty_sysroot

  # Skipped tests.
  blacklisted_package_info = input_proto.package_blacklist
  blacklist = []
  for package_info in blacklisted_package_info:
    blacklist.append(controller_util.PackageInfoToString(package_info))

  build_target = build_target_util.BuildTarget(board)
  chroot = controller_util.ParseChroot(input_proto.chroot)

  result = test.BuildTargetUnitTest(build_target, chroot, blacklist=blacklist,
                                    was_built=was_built)

  if not result.success:
    # Failed to run tests or some tests failed.
    # Record all failed packages.
    for cpv in result.failed_cpvs:
      package_info = output_proto.failed_packages.add()
      controller_util.CPVToPackageInfo(cpv, package_info)
    if result.failed_cpvs:
      return controller.RETURN_CODE_UNSUCCESSFUL_RESPONSE_AVAILABLE
    else:
      return controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY

  sysroot = sysroot_lib.Sysroot(build_target.root)
  tarball = test.BuildTargetUnitTestTarball(chroot, sysroot, result_path)
  if tarball:
    output_proto.tarball_path = tarball


def ChromiteUnitTest(_input_proto, _output_proto):
  """Run the chromite unit tests."""
  cmd = [os.path.join(constants.CHROMITE_DIR, 'scripts', 'run_tests')]
  result = cros_build_lib.RunCommand(cmd, error_code_ok=True,
                                     combine_stdout_stderr=True)
  if result.returncode == 0:
    return controller.RETURN_CODE_SUCCESS
  else:
    return controller.RETURN_CODE_COMPLETED_UNSUCCESSFULLY


def VmTest(input_proto, _output_proto):
  """Run VM tests."""
  if not input_proto.HasField('build_target'):
    cros_build_lib.Die('build_target is required')
  build_target = input_proto.build_target

  vm_path = input_proto.vm_path
  if not vm_path.path:
    cros_build_lib.Die('vm_path.path is required.')

  test_harness = input_proto.test_harness
  if test_harness == test_pb2.VmTestRequest.UNSPECIFIED:
    cros_build_lib.Die('test_harness is required')

  vm_tests = input_proto.vm_tests
  if not vm_tests:
    cros_build_lib.Die('vm_tests must contain at least one element')

  cmd = ['cros_run_test', '--debug', '--no-display', '--copy-on-write',
         '--board', build_target.name, '--image-path', vm_path.path,
         '--%s' % test_pb2.VmTestRequest.TestHarness.Name(test_harness).lower()]
  cmd.extend(vm_test.pattern for vm_test in vm_tests)

  if input_proto.ssh_options.port:
    cmd.extend(['--ssh-port', str(input_proto.ssh_options.port)])

  if input_proto.ssh_options.private_key_path:
    cmd.extend(['--private-key', input_proto.ssh_options.private_key_path.path])

  # TODO(evanhernandez): Find a nice way to pass test_that-args through
  # the build API. Or obviate them.
  if test_harness == test_pb2.VmTestRequest.AUTOTEST:
    cmd.append('--test_that-args=--whitelist-chrome-crashes')

  with osutils.TempDir(prefix='vm-test-results.') as results_dir:
    cmd.extend(['--results-dir', results_dir])
    cros_build_lib.RunCommand(cmd, kill_timeout=10 * 60)


def MoblabVmTest(input_proto, _output_proto):
  """Run Moblab VM tests."""
  chroot = controller_util.ParseChroot(input_proto.chroot)
  image_payload_dir = input_proto.image_payload.path.path
  cache_payload_dirs = [cp.path.path for cp in input_proto.cache_payloads]

  # Autotest and Moblab depend on the builder path, so we must read it from
  # the image.
  image_file = os.path.join(image_payload_dir, constants.TEST_IMAGE_BIN)
  with osutils.TempDir() as mount_dir:
    with image_lib.LoopbackPartitions(image_file, destination=mount_dir) as lp:
      # The file we want is /etc/lsb-release, which lives in the ROOT-A
      # disk partition.
      partition_paths = lp.Mount([constants.PART_ROOT_A])
      assert len(partition_paths) == 1, (
          'expected one partition path, got: %r' % partition_paths)
      partition_path = partition_paths[0]
      lsb_release_file = os.path.join(partition_path,
                                      constants.LSB_RELEASE_PATH.strip('/'))
      lsb_release_kvs = cros_build_lib.LoadKeyValueFile(lsb_release_file)
      builder = lsb_release_kvs.get(cros_set_lsb_release.LSB_KEY_BUILDER_PATH)

  if not builder:
    cros_build_lib.Die('Image did not contain key %s in %s',
                       cros_set_lsb_release.LSB_KEY_BUILDER_PATH,
                       constants.LSB_RELEASE_PATH)

  # Now we can run the tests.
  with chroot.tempdir() as workspace_dir, chroot.tempdir() as results_dir:
    vms = test.CreateMoblabVm(workspace_dir, image_payload_dir)
    cache_dir = test.PrepareMoblabVmImageCache(vms, builder, cache_payload_dirs)
    test.RunMoblabVmTest(chroot, vms, builder, cache_dir, results_dir)
    test.ValidateMoblabVmTest(results_dir)
