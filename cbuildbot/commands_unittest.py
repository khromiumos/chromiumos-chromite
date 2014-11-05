#!/usr/bin/python
# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for commands."""

from __future__ import print_function

import base64
import os
import sys

from StringIO import StringIO

import constants
sys.path.insert(0, constants.SOURCE_ROOT)
from chromite.cbuildbot import commands
from chromite.cbuildbot import failures_lib
from chromite.lib import cros_build_lib_unittest
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import gs
from chromite.lib import git
from chromite.lib import gob_util
from chromite.lib import osutils
from chromite.lib import partial_mock
from chromite.scripts import pushimage

# TODO(build): Finish test wrapper (http://crosbug.com/37517).
# Until then, this has to be after the chromite imports.
import mock


# pylint: disable=W0212
class RunBuildScriptTest(cros_test_lib.TempDirTestCase):
  """Test RunBuildScript in a variety of cases."""

  def _assertRunBuildScript(self, in_chroot=False, error=None, raises=None,
                            **kwargs):
    """Test the RunBuildScript function.

    Args:
      in_chroot: Whether to enter the chroot or not.
      error: error result message to simulate.
      raises: If the command should fail, the exception to be raised.
      kwargs: Extra kwargs passed to RunBuildScript.
    """
    # Write specified error message to status file.
    def WriteError(_cmd, extra_env=None, **_kwargs):
      if extra_env is not None and error is not None:
        status_file = extra_env['PARALLEL_EMERGE_STATUS_FILE']
        osutils.WriteFile(status_file, error)

    buildroot = self.tempdir
    osutils.SafeMakedirs(os.path.join(buildroot, '.repo'))
    if error is not None:
      osutils.SafeMakedirs(os.path.join(buildroot, 'chroot', 'tmp'))

    # Run the command, throwing an exception if it fails.
    with cros_build_lib_unittest.RunCommandMock() as m:
      cmd = ['example', 'command']
      sudo_cmd = ['sudo', '--'] + cmd
      returncode = 1 if raises else 0
      m.AddCmdResult(cmd, returncode=returncode, side_effect=WriteError)
      m.AddCmdResult(sudo_cmd, returncode=returncode, side_effect=WriteError)
      with mock.patch.object(git, 'ReinterpretPathForChroot',
                             side_effect=lambda x: x):
        with cros_test_lib.LoggingCapturer():
          # If the script failed, the exception should be raised and printed.
          if raises:
            self.assertRaises(raises, commands.RunBuildScript, buildroot,
                              cmd, enter_chroot=in_chroot, **kwargs)
          else:
            commands.RunBuildScript(buildroot, cmd, enter_chroot=in_chroot,
                                    **kwargs)

  def testSuccessOutsideChroot(self):
    """Test executing a command outside the chroot."""
    self._assertRunBuildScript()

  def testSuccessInsideChrootWithoutTempdir(self):
    """Test executing a command inside a chroot without a tmp dir."""
    self._assertRunBuildScript(in_chroot=True)

  def testSuccessInsideChrootWithTempdir(self):
    """Test executing a command inside a chroot with a tmp dir."""
    self._assertRunBuildScript(in_chroot=True, error='')

  def testFailureOutsideChroot(self):
    """Test a command failure outside the chroot."""
    self._assertRunBuildScript(raises=failures_lib.BuildScriptFailure)

  def testFailureInsideChrootWithoutTempdir(self):
    """Test a command failure inside the chroot without a temp directory."""
    self._assertRunBuildScript(in_chroot=True,
                               raises=failures_lib.BuildScriptFailure)

  def testFailureInsideChrootWithTempdir(self):
    """Test a command failure inside the chroot with a temp directory."""
    self._assertRunBuildScript(in_chroot=True, error='',
                               raises=failures_lib.BuildScriptFailure)

  def testPackageBuildFailure(self):
    """Test detecting a package build failure."""
    self._assertRunBuildScript(in_chroot=True, error=constants.CHROME_CP,
                               raises=failures_lib.PackageBuildFailure)

  def testSuccessWithSudo(self):
    """Test a command run with sudo."""
    self._assertRunBuildScript(in_chroot=False, sudo=True)
    self._assertRunBuildScript(in_chroot=True, sudo=True)


class RunTestSuiteTest(cros_build_lib_unittest.RunCommandTempDirTestCase):
  """Test RunTestSuite functionality."""

  TEST_BOARD = 'x86-generic'
  BUILD_ROOT = '/fake/root'

  def _RunTestSuite(self, test_type):
    commands.RunTestSuite(self.tempdir, self.TEST_BOARD, self.BUILD_ROOT,
                          '/tmp/taco', archive_dir='/fake/root',
                          whitelist_chrome_crashes=False,
                          test_type=test_type)

  def testFull(self):
    """Test running FULL config."""
    self._RunTestSuite(constants.FULL_AU_TEST_TYPE)
    self.assertCommandContains(['--quick'], expected=False)
    self.assertCommandContains(['--only_verify'], expected=False)

  def testSimple(self):
    """Test SIMPLE config."""
    self._RunTestSuite(constants.SIMPLE_AU_TEST_TYPE)
    self.assertCommandContains(['--quick_update'])

  def testSmoke(self):
    """Test SMOKE config."""
    self._RunTestSuite(constants.SMOKE_SUITE_TEST_TYPE)
    self.assertCommandContains(['--only_verify'])


class ChromeSDKTest(cros_build_lib_unittest.RunCommandTempDirTestCase):
  """Basic tests for ChromeSDK commands with RunCommand mocked out."""
  BOARD = 'daisy_foo'
  EXTRA_ARGS = ('--monkey', 'banana')
  EXTRA_ARGS2 = ('--donkey', 'kong')
  CHROME_SRC = 'chrome_src'
  CMD = ['bar', 'baz']
  CWD = 'fooey'

  def setUp(self):
    self.inst = commands.ChromeSDK(self.CWD, self.BOARD)

  def testRunCommand(self):
    """Test that running a command is possible."""
    self.inst.Run(self.CMD)
    self.assertCommandContains([self.BOARD] + self.CMD, cwd=self.CWD)

  def testRunCommandKwargs(self):
    """Exercise optional arguments."""
    custom_inst = commands.ChromeSDK(
        self.CWD, self.BOARD, extra_args=list(self.EXTRA_ARGS),
        chrome_src=self.CHROME_SRC, debug_log=True)
    custom_inst.Run(self.CMD, list(self.EXTRA_ARGS2))
    self.assertCommandContains(['debug', self.BOARD] + list(self.EXTRA_ARGS) +
                               list(self.EXTRA_ARGS2) + self.CMD, cwd=self.CWD)

  def testNinja(self):
    """Test that running ninja is possible."""
    self.inst.Ninja(self.BOARD)
    self.assertCommandContains([self.BOARD], cwd=self.CWD)

class HWLabCommandsTest(cros_build_lib_unittest.RunCommandTestCase):
  """Test commands related to HWLab tests."""

  def setUp(self):
    self._build = 'test-build'
    self._board = 'test-board'
    self._suite = 'test-suite'
    self._pool = 'test-pool'
    self._num = 42
    self._file_bugs = True
    self._wait_for_results = False
    self._priority = 'test-priority'
    self._timeout_mins = 23
    self._retry = False

  def testRunHWTestSuiteMinimal(self):
    """Test RunHWTestSuite without optional arguments."""
    commands.RunHWTestSuite(self._build, self._suite, self._board, debug=False)
    self.assertCommandCalled([
        commands._AUTOTEST_RPC_CLIENT, commands._AUTOTEST_RPC_HOSTNAME,
        'RunSuite', '--build', 'test-build', '--suite_name', 'test-suite',
        '--board', 'test-board'
    ], error_code_ok=True)

  def testRunHWTestSuiteMaximal(self):
    """Test RunHWTestSuite with all arguments."""
    commands.RunHWTestSuite(self._build, self._suite, self._board,
                            self._pool, self._num, self._file_bugs,
                            self._wait_for_results, self._priority,
                            self._timeout_mins, self._retry, debug=False)
    self.assertCommandCalled([
        commands._AUTOTEST_RPC_CLIENT, commands._AUTOTEST_RPC_HOSTNAME,
        'RunSuite', '--build', 'test-build', '--suite_name', 'test-suite',
        '--board', 'test-board', '--pool', 'test-pool', '--num', '42',
        '--file_bugs', 'True', '--no_wait', 'True',
        '--priority', 'test-priority', '--timeout_mins', '23',
        '--retry', 'False',
    ], error_code_ok=True)

  def testRunHWTestSuiteFailure(self):
    """Test RunHWTestSuite when ERROR is returned."""
    self.rc.SetDefaultCmdResult(returncode=1)
    self.assertRaises(commands.TestFailure, commands.RunHWTestSuite,
                      self._build, self._suite, self._board, debug=False)

  def testRunHWTestSuiteTimedOut(self):
    """Test RunHWTestSuite when SUITE_TIMEOUT is returned."""
    self.rc.SetDefaultCmdResult(returncode=4)
    self.assertRaises(commands.SuiteTimedOut, commands.RunHWTestSuite,
                      self._build, self._suite, self._board, debug=False)

  def testRunHWTestSuiteInfraFail(self):
    """Test RunHWTestSuite when INFRA_FAILURE is returned."""
    self.rc.SetDefaultCmdResult(returncode=3)
    self.assertRaises(failures_lib.TestLabFailure, commands.RunHWTestSuite,
                      self._build, self._suite, self._board, debug=False)

  def testRunHWTestBoardNotAvailable(self):
    """Test RunHWTestSuite when BOARD_NOT_AVAILABLE is returned."""
    self.rc.SetDefaultCmdResult(returncode=5)
    self.assertRaises(commands.BoardNotAvailable, commands.RunHWTestSuite,
                      self._build, self._suite, self._board, debug=False)


class CBuildBotTest(cros_build_lib_unittest.RunCommandTempDirTestCase):
  """Test general cbuildbot command methods."""

  def setUp(self):
    self._board = 'test-board'
    self._buildroot = self.tempdir
    self._overlays = ['%s/src/third_party/chromiumos-overlay' % self._buildroot]
    self._chroot = os.path.join(self._buildroot, 'chroot')
    os.makedirs(os.path.join(self._buildroot, '.repo'))

  def testGenerateStackTraces(self):
    """Test if we can generate stack traces for minidumps."""
    os.makedirs(os.path.join(self._chroot, 'tmp'))
    dump_file = os.path.join(self._chroot, 'tmp', 'test.dmp')
    dump_file_dir, dump_file_name = os.path.split(dump_file)
    ret = [(dump_file_dir, [''], [dump_file_name])]
    with mock.patch('os.walk', return_value=ret):
      test_results_dir = os.path.join(self.tempdir, 'test_results')
      commands.GenerateStackTraces(self._buildroot, self._board,
                                   test_results_dir, self.tempdir, True)
      self.assertCommandContains(['minidump_stackwalk'])

  def testUprevAllPackages(self):
    """Test if we get None in revisions.pfq indicating Full Builds."""
    commands.UprevPackages(self._buildroot, [self._board], self._overlays)
    self.assertCommandContains(['--boards=%s' % self._board, 'commit'])

  def testVerifyBinpkgMissing(self):
    """Test case where binpkg is missing."""
    self.rc.AddCmdResult(partial_mock.ListRegex(r'emerge'),
        output='\n[ebuild] %s' % constants.CHROME_CP)
    self.assertRaises(commands.MissingBinpkg, commands.VerifyBinpkg,
        self._buildroot, self._board, constants.CHROME_CP, packages=())

  def testVerifyBinpkgPresent(self):
    """Test case where binpkg is present."""
    self.rc.AddCmdResult(partial_mock.ListRegex(r'emerge'),
        output='\n[binary] %s' % constants.CHROME_CP)
    commands.VerifyBinpkg(self._buildroot, self._board, constants.CHROME_CP,
                          packages=())

  def testVerifyChromeNotInstalled(self):
    """Test case where Chrome is not installed at all."""
    commands.VerifyBinpkg(self._buildroot, self._board, constants.CHROME_CP,
                          packages=())

  def testBuild(self, default=False, **kwargs):
    """Base case where Build is called with minimal options."""
    kwargs.setdefault('build_autotest', default)
    kwargs.setdefault('usepkg', default)
    kwargs.setdefault('chrome_binhost_only', default)
    kwargs.setdefault('skip_chroot_upgrade', default)
    commands.Build(buildroot=self._buildroot, board='x86-generic', **kwargs)
    self.assertCommandContains(['./build_packages'])

  def testGetFirmwareVersions(self):
    self.rc.SetDefaultCmdResult(output='''

flashrom(8): a273d7fd6663c665176159496bc014ff */build/nyan/usr/sbin/flashrom
             ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, for GNU/Linux 2.6.16, BuildID[sha1]=61d8a9676e433414fb0e22fa819b55be86329e44, stripped


BIOS image:   4aba4c07a65b7bf82d72d8ed892f5dc5 */build/nyan/tmp/portage/chromeos-base/chromeos-firmware-nyan-0.0.1-r20/work/chromeos-firmware-nyan-0.0.1/.dist/nyan_fw_5771.10.0.tbz2/image.bin
BIOS version: Google_Nyan.5771.10.0
EC image:     7b6bb5035fa8101b41c954bce5250dae */build/nyan/tmp/portage/chromeos-base/chromeos-firmware-nyan-0.0.1-r20/work/chromeos-firmware-nyan-0.0.1/.dist/nyan_ec_5771.10.0.tbz2/ec.bin
EC version:   nyan_v1.1.1782-23f1337

Package Content:
d7124c9a2680ff57f1c7d6521ac5ef8c *./mosys
ad9520c70add670d8f2770a2a3c4115a *./gbb_utility
7b6bb5035fa8101b41c954bce5250dae *./ec.bin
a273d7fd6663c665176159496bc014ff *./flashrom
d149f6413749ca6a0edddd52926f95ca *./dump_fmap
5bfe13d9b7fef1dfd9d3dac185f94994 *./crossystem
3c3a99346d1ca1273cbcd86c104851ff *./shflags
4aba4c07a65b7bf82d72d8ed892f5dc5 *./bios.bin
2a484f3e107bf27a4d1068e03e74803c *./common.sh
995a97518f90541d37c3f57a336d37db *./vpd
b9270e726180af1ed59077d1ab2fc688 *./crosfw.sh
f6b0b80d5f2d9a2fb41ebb6e2cee7ad8 *./updater4.sh
4363fcfd6849b2ab1a7320b1c98a11f2 *./crosutil.sh
''')
    build_sbin = os.path.join(self._buildroot, constants.DEFAULT_CHROOT_DIR,
                              'build', self._board, 'usr', 'sbin')
    osutils.Touch(os.path.join(build_sbin, 'chromeos-firmwareupdate'),
                  makedirs=True)
    result = commands.GetFirmwareVersions(self._buildroot, self._board)
    versions = ('Google_Nyan.5771.10.0', 'nyan_v1.1.1782-23f1337')
    self.assertEquals(result, versions)

  def testBuildMaximum(self):
    """Base case where Build is called with all options (except extra_env)."""
    self.testBuild(default=True)

  def testBuildWithEnv(self):
    """Case where Build is called with a custom environment."""
    extra_env = {'A': 'Av', 'B': 'Bv'}
    self.testBuild(extra_env=extra_env)
    self.assertCommandContains(['./build_packages'], extra_env=extra_env)

  def testGenerateSymbols(self):
    """Test GenerateBreakpadSymbols Command."""
    commands.GenerateBreakpadSymbols(self.tempdir, self._board, False)
    self.assertCommandContains(['--board=%s' % self._board])

  @mock.patch('chromite.scripts.upload_symbols.UploadSymbols')
  def testUploadSymbols(self, sym_mock, official=False, cnt=None):
    """Test UploadSymbols Command."""
    sym_mock.side_effect = [0]
    commands.UploadSymbols(self.tempdir, self._board, official, cnt, None)
    self.assertEquals(sym_mock.call_count, 1)
    _, kwargs = sym_mock.call_args
    self.assertEquals(kwargs['official'], official)
    self.assertEquals(kwargs['upload_limit'], cnt)

  def testOfficialUploadSymbols(self):
    """Test uploading symbols for official builds"""
    # Seems pylint can't grasp the @mock.patch decorator.
    # pylint: disable=E1120
    self.testUploadSymbols(official=True)

  def testLimitUploadSymbols(self):
    """Test uploading a limited number of symbols"""
    # Seems pylint can't grasp the @mock.patch decorator.
    # pylint: disable=E1120
    self.testUploadSymbols(cnt=10)

  def testPushImages(self):
    """Test PushImages Command."""
    m = self.PatchObject(pushimage, 'PushImage')
    commands.PushImages(self._board, 'gs://foo/R34-1234.0.0', False, None)
    self.assertEqual(m.call_count, 1)

  def testBuildImage(self):
    """Test Basic BuildImage Command."""
    commands.BuildImage(self._buildroot, self._board, None)
    self.assertCommandContains(['./build_image'])

  def testGenerateAuZip(self):
    """Test Basic generate_au_zip Command."""
    with mock.patch.object(git, 'ReinterpretPathForChroot',
                           side_effect=lambda x: x):
      commands.GenerateAuZip(self._buildroot, '/tmp/taco', None)
    self.assertCommandContains(['./build_library/generate_au_zip.py'])

  def testTestAuZip(self):
    """Test Basic generate_au_zip Command."""
    commands.TestAuZip(self._buildroot, '/tmp/taco', None)
    self.assertCommandContains(['./build_library/test_au_zip.py'])

  def testCompleteBuildImage(self):
    """Test Complete BuildImage Command."""
    images_to_build = ['bob', 'carol', 'ted', 'alice']
    commands.BuildImage(self._buildroot, self._board, images_to_build,
        rootfs_verification=False, extra_env={'LOVE': 'free'},
        disk_layout='2+2', version='1969')
    self.assertCommandContains(['./build_image'])

  def _TestChromeLKGM(self, chrome_revision):
    """Helper method for testing the GetChromeLKGM method."""
    chrome_lkgm = '3322.0.0'
    url = '%s/+/%s/%s?format=text' % (
        constants.CHROMIUM_SRC_PROJECT,
        chrome_revision or 'refs/heads/master',
        constants.PATH_TO_CHROME_LKGM)
    with mock.patch.object(
        gob_util, 'FetchUrl',
        return_value=StringIO(base64.b64encode(chrome_lkgm))) as patcher:
      self.assertEqual(chrome_lkgm, commands.GetChromeLKGM(chrome_revision))
      patcher.assert_called_with(constants.EXTERNAL_GOB_HOST, url)

  def testChromeLKGM(self):
    """Verifies that we can get the chrome lkgm without a chrome revision."""
    self._TestChromeLKGM(None)

  def testChromeLKGMWithRevision(self):
    """Verifies that we can get the chrome lkgm with a chrome revision."""
    self._TestChromeLKGM('deadbeef' * 5)

  def testAbortCQHWTests(self):
    commands.AbortCQHWTests('my-version', debug=False)
    self.assertCommandContains(['cp'])
    self.assertCommandContains(['-i', 'paladin/my-version'])

  def testHWTestsAborted(self, aborted=True):
    self.PatchObject(gs.GSContext, 'Exists', return_value=aborted)
    self.assertEqual(commands.HaveCQHWTestsBeenAborted('my-version'), aborted)

  def testHWTestsNotAborted(self):
    self.testHWTestsAborted(aborted=False)


class BuildTarballTests(cros_build_lib_unittest.RunCommandTempDirTestCase):
  """Tests related to BuildAUTestTarball."""

  def setUp(self):
    self._buildroot = os.path.join(self.tempdir, 'buildroot')
    os.makedirs(self._buildroot)
    self._board = 'test-board'

  def testBuildAUTestTarball(self):
    """Tests that our call to generate an au test tarball is correct."""
    tarball_dir = self.tempdir
    archive_url = 'gs://mytest/path/version'
    with mock.patch.object(commands, 'BuildTarball') as m:
      tarball_path = commands.BuildAUTestTarball(
          self._buildroot, self._board, tarball_dir, 'R26-3928.0.0',
          archive_url)
      m.assert_called_once_with(self._buildroot, ['autotest/au_control_files'],
                                os.path.join(tarball_dir, 'au_control.tar.bz2'),
                                cwd=tarball_dir)

      self.assertEquals(os.path.join(tarball_dir, 'au_control.tar.bz2'),
                        tarball_path)

    # Full release test with partial args defined.
    self.assertCommandContains(['site_utils/autoupdate/full_release_test.py',
                                '--archive_url', archive_url, '3928.0.0',
                                self._board])


class UnmockedTests(cros_test_lib.TempDirTestCase):
  """Test cases which really run tests, instead of using mocks."""

  def testListFaliedTests(self):
    """Tests if we can list failed tests."""
    test_report_1 = """
/tmp/taco/taste_tests/all/results-01-has_salsa              [  PASSED  ]
/tmp/taco/taste_tests/all/results-01-has_salsa/has_salsa    [  PASSED  ]
/tmp/taco/taste_tests/all/results-02-has_cheese             [  FAILED  ]
/tmp/taco/taste_tests/all/results-02-has_cheese/has_cheese  [  FAILED  ]
/tmp/taco/taste_tests/all/results-02-has_cheese/has_cheese   FAIL: No cheese.
"""
    test_report_2 = """
/tmp/taco/verify_tests/all/results-01-has_salsa              [  PASSED  ]
/tmp/taco/verify_tests/all/results-01-has_salsa/has_salsa    [  PASSED  ]
/tmp/taco/verify_tests/all/results-02-has_cheese             [  PASSED  ]
/tmp/taco/verify_tests/all/results-02-has_cheese/has_cheese  [  PASSED  ]
"""
    results_path = os.path.join(self.tempdir, 'tmp/taco')
    os.makedirs(results_path)
    # Create two reports with the same content to test that we don't
    # list the same test twice.
    osutils.WriteFile(
        os.path.join(results_path, 'taste_tests', 'all', 'test_report.log'),
        test_report_1, makedirs=True)
    osutils.WriteFile(
        os.path.join(results_path, 'taste_tests', 'failed', 'test_report.log'),
        test_report_1, makedirs=True)
    osutils.WriteFile(
        os.path.join(results_path, 'verify_tests', 'all', 'test_report.log'),
        test_report_2, makedirs=True)

    self.assertEquals(
        commands.ListFailedTests(results_path),
        [('has_cheese', 'taste_tests/all/results-02-has_cheese')])

  def testArchiveTestResults(self):
    """Test if we can archive a test results dir."""
    test_results_dir = 'tmp/taco'
    results_path = os.path.join(self.tempdir, 'chroot', test_results_dir)
    archive_dir = os.path.join(self.tempdir, 'archived_taco')
    os.makedirs(results_path)
    os.makedirs(archive_dir)
    # File that should be archived.
    osutils.Touch(os.path.join(results_path, 'foo.txt'))
    # Flies that should be ignored.
    osutils.Touch(os.path.join(results_path,
                               'chromiumos_qemu_disk.bin.foo'))
    os.symlink('/src/foo', os.path.join(results_path, 'taco_link'))
    commands.ArchiveTestResults(results_path, archive_dir)
    self.assertExists(os.path.join(archive_dir, 'foo.txt'))
    self.assertNotExists(
        os.path.join(archive_dir, 'chromiumos_qemu_disk.bin.foo'))
    self.assertNotExists(os.path.join(archive_dir, 'taco_link'))

  def testBuildFirmwareArchive(self):
    """Verifies that firmware archiver includes proper files"""
    # Assorted set of file names, some of which are supposed to be included in
    # the archive.
    fw_files = (
      'dts/emeraldlake2.dts',
      'image-link.rw.bin',
      'nv_image-link.bin',
      'pci8086,0166.rom',
      'seabios.cbfs',
      'u-boot.elf',
      'u-boot_netboot.bin',
      'updater-link.rw.sh',
      'x86-memtest')
    # Files which should be included in the archive.
    fw_archived_files = fw_files + ('dts/',)
    board = 'link'
    fw_test_root = os.path.join(self.tempdir, os.path.basename(__file__))
    fw_files_root = os.path.join(fw_test_root,
                                 'chroot/build/%s/firmware' % board)
    # Generate a representative set of files produced by a typical build.
    cros_test_lib.CreateOnDiskHierarchy(fw_files_root, fw_files)
    # Create an archive from the simulated firmware directory
    tarball = os.path.join(
        fw_test_root,
        commands.BuildFirmwareArchive(fw_test_root, board, fw_test_root))
    # Verify the tarball contents.
    cros_test_lib.VerifyTarball(tarball, fw_archived_files)

  def testGenerateHtmlIndexTuple(self):
    """Verifies GenerateHtmlIndex gives us something sane (input: tuple)"""
    index = os.path.join(self.tempdir, 'index.html')
    files = ('file1', 'monkey tree', 'flying phone',)
    commands.GenerateHtmlIndex(index, files)
    html = osutils.ReadFile(index)
    for f in files:
      # TODO(build): Use assertIn w/python-2.7.
      self.assertTrue('>%s</a>' % f in html)

  def testGenerateHtmlIndexTupleDupe(self):
    """Verifies GenerateHtmlIndex gives us something unique (input: tuple)"""
    index = os.path.join(self.tempdir, 'index.html')
    files = ('file1', 'file1', 'file1',)
    commands.GenerateHtmlIndex(index, files)
    html = osutils.ReadFile(index)
    self.assertEqual(html.count('>file1</a>'), 1)

  def testGenerateHtmlIndexTuplePretty(self):
    """Verifies GenerateHtmlIndex gives us something pretty (input: tuple)"""
    index = os.path.join(self.tempdir, 'index.html')
    files = ('..|up', 'f.txt|MY FILE', 'm.log|MONKEY', 'b.bin|Yander',)
    commands.GenerateHtmlIndex(index, files)
    html = osutils.ReadFile(index)
    for f in files:
      a = f.split('|')
      # TODO(build): Use assertIn w/python-2.7.
      self.assertTrue('href="%s"' % a[0] in html)
      self.assertTrue('>%s</a>' % a[1] in html)

  def testGenerateHtmlIndexDir(self):
    """Verifies GenerateHtmlIndex gives us something sane (input: dir)"""
    index = os.path.join(self.tempdir, 'index.html')
    files = ('a', 'b b b', 'c', 'dalsdkjfasdlkf',)
    simple_dir = os.path.join(self.tempdir, 'dir')
    for f in files:
      osutils.Touch(os.path.join(simple_dir, f), makedirs=True)
    commands.GenerateHtmlIndex(index, files)
    html = osutils.ReadFile(index)
    for f in files:
      # TODO(build): Use assertIn w/python-2.7.
      self.assertTrue('>%s</a>' % f in html)

  def testGenerateHtmlIndexFile(self):
    """Verifies GenerateHtmlIndex gives us something sane (input: file)"""
    index = os.path.join(self.tempdir, 'index.html')
    files = ('a.tgz', 'b b b.txt', 'c', 'dalsdkjfasdlkf',)
    filelist = os.path.join(self.tempdir, 'listing')
    osutils.WriteFile(filelist, '\n'.join(files))
    commands.GenerateHtmlIndex(index, filelist)
    html = osutils.ReadFile(index)
    for f in files:
      # TODO(build): Use assertIn w/python-2.7.
      self.assertTrue('>%s</a>' % f in html)

  def testArchiveGeneration(self):
    """Verifies BuildStandaloneImageArchive produces correct archives"""
    image_dir = os.path.join(self.tempdir, 'inputs')
    archive_dir = os.path.join(self.tempdir, 'outputs')
    files = ('a.bin', 'aa', 'b b b', 'c', 'dalsdkjfasdlkf',)
    osutils.SafeMakedirs(image_dir)
    osutils.SafeMakedirs(archive_dir)
    for f in files:
      osutils.Touch(os.path.join(image_dir, f))

    # Check specifying tar functionality.
    artifact = {'paths': ['a.bin'], 'output': 'a.tar.gz', 'archive': 'tar',
                'compress':'gz'}
    path = commands.BuildStandaloneArchive(archive_dir, image_dir, artifact)
    self.assertEquals(path, ['a.tar.gz'])
    cros_test_lib.VerifyTarball(os.path.join(archive_dir, path[0]),
                                ['a.bin'])

    # Check multiple input files.
    artifact = {'paths': ['a.bin', 'aa'], 'output': 'aa.tar.gz',
                'archive': 'tar', 'compress': 'gz'}
    path = commands.BuildStandaloneArchive(archive_dir, image_dir, artifact)
    self.assertEquals(path, ['aa.tar.gz'])
    cros_test_lib.VerifyTarball(os.path.join(archive_dir, path[0]),
                                ['a.bin', 'aa'])

    # Check zip functionality.
    artifact = {'paths': ['a.bin'], 'archive': 'zip'}
    path = commands.BuildStandaloneArchive(archive_dir, image_dir, artifact)
    self.assertEquals(path, ['a.zip'])
    self.assertExists(os.path.join(archive_dir, path[0]))


class ImageTestCommandsTest(cros_build_lib_unittest.RunCommandTestCase):
  """Test commands related to ImageTest tests."""

  def setUp(self):
    self._build = 'test-build'
    self._board = 'test-board'
    self._image_dir = 'image-dir'
    self._result_dir = 'result-dir'
    self.PatchObject(git, 'ReinterpretPathForChroot',
                     side_effect=lambda x: x)

  def testRunTestImage(self):
    """Verifies RunTestImage calls into test-image script properly."""
    commands.RunTestImage(self._build, self._board, self._image_dir,
                          self._result_dir)
    self.assertCommandContains(
        [
          'sudo', '--',
          os.path.join(self._build, 'chromite', 'bin', 'test_image'),
          '--board', self._board,
          '--test_results_root',
          cros_build_lib.ToChrootPath(self._result_dir),
          cros_build_lib.ToChrootPath(self._image_dir),
        ],
        enter_chroot=True,
    )


if __name__ == '__main__':
  cros_test_lib.main()
