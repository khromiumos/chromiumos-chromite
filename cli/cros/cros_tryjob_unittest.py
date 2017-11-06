# -*- coding: utf-8 -*-
# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests the `cros chroot` command."""

from __future__ import print_function

import mock

from chromite.cli import command_unittest
from chromite.lib import config_lib
from chromite.lib import cros_build_lib
from chromite.cli.cros import cros_tryjob
from chromite.lib import cros_test_lib


class MockTryjobCommand(command_unittest.MockCommand):
  """Mock out the `cros tryjob` command."""
  TARGET = 'chromite.cli.cros.cros_tryjob.TryjobCommand'
  TARGET_CLASS = cros_tryjob.TryjobCommand
  COMMAND = 'tryjob'


class TryjobTest(cros_test_lib.MockTestCase):
  """Base class for Tryjob command tests."""

  def setUp(self):
    self.cmd_mock = None

  def SetupCommandMock(self, cmd_args):
    """Sets up the `cros tryjob` command mock."""
    self.cmd_mock = MockTryjobCommand(cmd_args)
    self.StartPatcher(self.cmd_mock)

    return self.cmd_mock.inst.options


class TryjobTestParsing(TryjobTest):
  """Test cros try command line parsing."""

  def setUp(self):
    self.expected = {
        'remote': True,
        'swarming': False,
        'branch': 'master',
        'production': False,
        'yes': False,
        'list': False,
        'list_all': False,
        'gerrit_patches': [],
        'local_patches': [],
        'passthrough': None,
        'passthrough_raw': None,
        'build_configs': ['lumpy-paladin'],
    }

  def testMinimalParsingLocal(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock(['lumpy-paladin'])
    options = self.cmd_mock.inst.options

    self.assertDictContainsSubset(self.expected, vars(options))

  def testComplexParsing(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--local', '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--local-patches', 'chromiumos/chromite:tryjob', '-p', 'other:other',
        '--chrome_version', 'chrome_git_hash',
        '--pass-through=--cbuild-arg', '--pass-through', 'bar',
        '--list', '--all',
        'lumpy-paladin', 'lumpy-release',
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'remote': False,
        'swarming': False,
        'branch': 'master',
        'yes': True,
        'list': True,
        'list_all': True,
        'gerrit_patches': ['123', '*123', '123..456'],
        'local_patches': ['chromiumos/chromite:tryjob', 'other:other'],
        'passthrough': [
            '--latest-toolchain', '--nochromesdk',
            '--hwtest', '--notests', '--novmtests', '--noimagetests',
            '--timeout', '5', '--sanity-check-build',
            '--chrome_version', 'chrome_git_hash',
        ],
        'passthrough_raw': ['--cbuild-arg', 'bar'],
        'build_configs': ['lumpy-paladin', 'lumpy-release'],
    })

    self.assertDictContainsSubset(self.expected, vars(options))

  def testComplexParsingRemote(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--swarming',
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--local-patches', 'chromiumos/chromite:tryjob', '-p', 'other:other',
        '--chrome_version', 'chrome_git_hash',
        '--pass-through=--cbuild-arg', '--pass-through', 'bar',
        '--list', '--all',
        'lumpy-paladin', 'lumpy-release',
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'remote': True,
        'swarming': True,
        'branch': 'master',
        'yes': True,
        'list': True,
        'list_all': True,
        'gerrit_patches': ['123', '*123', '123..456'],
        'local_patches': ['chromiumos/chromite:tryjob', 'other:other'],
        'passthrough': [
            '--latest-toolchain', '--nochromesdk',
            '--hwtest', '--notests', '--novmtests', '--noimagetests',
            '--timeout', '5', '--sanity-check-build',
            '--chrome_version', 'chrome_git_hash',
        ],
        'passthrough_raw': ['--cbuild-arg', 'bar'],
        'build_configs': ['lumpy-paladin', 'lumpy-release'],
    })

    self.assertDictContainsSubset(self.expected, vars(options))

  def testPayloadsParsing(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--version', '9795.0.0', '--channel', 'canary', 'lumpy-payloads'
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'passthrough': ['--version', '9795.0.0', '--channel', 'canary'],
        'build_configs': ['lumpy-payloads'],
    })

    self.assertDictContainsSubset(self.expected, vars(options))


class TryjobTestVerifyOptions(TryjobTest):
  """Test cros_tryjob.VerifyOptions."""

  def setUp(self):
    self.site_config = config_lib.GetConfig()

  def testEmpty(self):
    """Test option verification with no options."""
    self.SetupCommandMock([])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      self.cmd_mock.inst.VerifyOptions(self.site_config)
    self.assertEqual(cm.exception.code, 1)

  def testMinimal(self):
    """Test option verification with simplest normal options."""
    self.SetupCommandMock([
        '-g', '123',
        'amd64-generic-paladin',
    ])
    self.cmd_mock.inst.VerifyOptions(self.site_config)

  def testComplexLocal(self):
    """Test option verification with complex mix of options."""
    self.SetupCommandMock([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--local', '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'lumpy-paladin', 'lumpy-release',
    ])
    self.cmd_mock.inst.VerifyOptions(self.site_config)

  def testComplexRemote(self):
    """Test option verification with complex mix of options."""
    self.SetupCommandMock([
        '--remote', '--swarming',
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'lumpy-paladin', 'lumpy-release',
    ])
    self.cmd_mock.inst.VerifyOptions(self.site_config)

  def testList(self):
    """Test option verification with config list behavior."""
    self.SetupCommandMock([
        '--list',
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      self.cmd_mock.inst.VerifyOptions(self.site_config)
    self.assertEqual(cm.exception.code, 0)

  def testProduction(self):
    """Test option verification with production/no patches."""
    self.SetupCommandMock([
        '--production',
        'lumpy-paladin', 'lumpy-release'
    ])
    self.cmd_mock.inst.VerifyOptions(self.site_config)

  def testProductionPatches(self):
    """Test option verification with production/patches."""
    self.SetupCommandMock([
        '--production',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        'lumpy-paladin', 'lumpy-release'
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      self.cmd_mock.inst.VerifyOptions(self.site_config)
    self.assertEqual(cm.exception.code, 1)

  def testUnknownBuildYes(self):
    """Test option using yes to force accepting an unknown config."""
    self.SetupCommandMock([
        '--yes',
        '-g', '123',
        'unknown-config'
    ])
    self.cmd_mock.inst.VerifyOptions(self.site_config)

  def testNoPatchesYes(self):
    """Test option using yes to force an unknown config, no patches."""
    self.SetupCommandMock([
        '--yes',
        'unknown-config'
    ])
    self.cmd_mock.inst.VerifyOptions(self.site_config)

  def testLocalSwarmingError(self):
    """Test option using yes to force an unknown config, no patches."""
    self.SetupCommandMock([
        '--yes',
        '--local', '--swarming',
        'amd64-generic-paladin',
    ])
    with self.assertRaises(cros_build_lib.DieSystemExit):
      self.cmd_mock.inst.VerifyOptions(self.site_config)


class TryjobTestCbuildbotArgs(TryjobTest):
  """Test cros_tryjob.CbuildbotArgs."""

  def helperOptionsToCbuildbotArgs(self, cmd_line_args):
    """Convert cros tryjob arguments -> cbuildbot arguments.

    Does not do all intermediate steps, only for testing CbuildbotArgs.
    """
    self.SetupCommandMock(cmd_line_args)
    options = self.cmd_mock.inst.options
    return cros_tryjob.CbuildbotArgs(options)

  def testCbuildbotArgsMinimal(self):
    result = self.helperOptionsToCbuildbotArgs([
        'foo-build'])
    self.assertEqual(result, [
        '--remote-trybot', '-b', 'master',
    ])

  def testCbuildbotArgsSimpleRemote(self):
    result = self.helperOptionsToCbuildbotArgs([
        '-g', '123', 'foo-build',
    ])
    self.assertEqual(result, [
        '--remote-trybot', '-b', 'master', '-g', '123',
    ])

  def testCbuildbotArgsSimpleLocal(self):
    result = self.helperOptionsToCbuildbotArgs([
        '--local', '-g', '123', 'foo-build',
    ])
    self.assertEqual(result, [
        '--buildroot', mock.ANY,
        '--no-buildbot-tags', '--debug',
        '-b', 'master',
        '-g', '123',
    ])

  def testCbuildbotArgsComplexRemote(self):
    result = self.helperOptionsToCbuildbotArgs([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--branch', 'source_branch',
        '--version', '1.2.3', '--channel', 'chan',
        '--branch-name', 'test_branch', '--rename-to', 'new_branch',
        '--delete-branch', '--force-create', '--skip-remote-push',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'lumpy-paladin', 'lumpy-release',
    ])
    self.assertEqual(result, [
        '--remote-trybot', '-b', 'source_branch',
        '-g', '123', '-g', '*123', '-g', '123..456',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--chrome_version', 'chrome_git_hash',
        '--version', '1.2.3', '--channel', 'chan',
        '--branch-name', 'test_branch', '--rename-to', 'new_branch',
        '--delete-branch', '--force-create', '--skip-remote-push',
        '--cbuild-arg', 'bar'
    ])

  def testCbuildbotArgsComplexLocal(self):
    result = self.helperOptionsToCbuildbotArgs([
        '--local', '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--branch', 'source_branch',
        '--version', '1.2.3', '--channel', 'chan',
        '--branch-name', 'test_branch', '--rename-to', 'new_branch',
        '--delete-branch', '--force-create', '--skip-remote-push',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'lumpy-paladin', 'lumpy-release',
    ])
    self.assertEqual(result, [
        '--buildroot', '/buildroot', '--no-buildbot-tags', '--debug',
        '-b', 'source_branch',
        '-g', '123', '-g', '*123', '-g', '123..456',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--chrome_version', 'chrome_git_hash',
        '--version', '1.2.3', '--channel', 'chan',
        '--branch-name', 'test_branch', '--rename-to', 'new_branch',
        '--delete-branch', '--force-create', '--skip-remote-push',
        '--cbuild-arg', 'bar'
    ])

  def testCbuildbotArgsProductionRemote(self):
    result = self.helperOptionsToCbuildbotArgs([
        '--production', 'foo-build',
    ])
    self.assertEqual(result, [
        '--buildbot', '-b', 'master',
    ])

  def testCbuildbotArgsProductionLocal(self):
    result = self.helperOptionsToCbuildbotArgs([
        '--local', '--production', 'foo-build',
    ])
    self.assertEqual(result, [
        '--buildroot', mock.ANY, '--no-buildbot-tags', '-b', 'master',
    ])

class TryjobTestDisplayLabel(TryjobTest):
  """Test the helper function DisplayLabel."""

  def FindLabel(self, args):
    site_config = config_lib.GetConfig()
    options = self.SetupCommandMock(args)
    config_name = options.build_configs[-1]
    return cros_tryjob.DisplayLabel(site_config, options, config_name)

  def testMasterTryjob(self):
    label = self.FindLabel(['lumpy-paladin-tryjob'])
    self.assertEqual(label, 'tryjob')

  def testMasterPreCQ(self):
    label = self.FindLabel(['lumpy-pre-cq'])
    self.assertEqual(label, 'pre_cq')

  def testMasterUnknown(self):
    label = self.FindLabel(['bogus-config'])
    self.assertEqual(label, 'tryjob')

  def testMasterKnownProduction(self):
    label = self.FindLabel(['--production', 'lumpy-paladin'])
    self.assertEqual(label, 'cq')

  def testMasterUnknownProduction(self):
    label = self.FindLabel(['--production', 'bogus-config'])
    self.assertEqual(label, 'production_tryjob')

  def testBranchTryjob(self):
    label = self.FindLabel(['--branch=test-branch', 'lumpy-pre-cq'])
    self.assertEqual(label, 'tryjob')

  def testBranchProduction(self):
    label = self.FindLabel(['--production', '--branch=test-branch',
                            'lumpy-pre-cq'])
    self.assertEqual(label, 'production_tryjob')
