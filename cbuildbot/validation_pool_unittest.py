#!/usr/bin/python
# Copyright (c) 2011-2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module that contains unittests for validation_pool module."""

from __future__ import print_function

import collections
import contextlib
import copy
import functools
import httplib
import itertools
import mox
import os
import pickle
import sys
import tempfile
import time

import constants
sys.path.insert(0, constants.SOURCE_ROOT)

from chromite.cbuildbot import metadata_lib
from chromite.cbuildbot import repository
from chromite.cbuildbot import tree_status
from chromite.cbuildbot import validation_pool
from chromite.cbuildbot import triage_lib
from chromite.lib import cidb
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import fake_cidb
from chromite.lib import gerrit
from chromite.lib import gob_util
from chromite.lib import gs
from chromite.lib import parallel
from chromite.lib import parallel_unittest
from chromite.lib import partial_mock
from chromite.lib import patch as cros_patch
from chromite.lib import patch_unittest

import mock


_GetNumber = iter(itertools.count()).next


def GetTestJson(change_id=None):
  """Get usable fake Gerrit patch json data

  Args:
    change_id: If given, force this ChangeId
  """
  data = copy.deepcopy(patch_unittest.FAKE_PATCH_JSON)
  if change_id is not None:
    data['id'] = str(change_id)
  return data


class MockManifest(object):
  """Helper class for Mocking Manifest objects."""

  def __init__(self, path, **kwargs):
    self.root = path
    for key, attr in kwargs.iteritems():
      setattr(self, key, attr)


class FakeBuilderRun(object):
  """A lightweight partial implementation of BuilderRun.

  validation_pool.ValidationPool makes use of a BuilderRun to access
  cidb and metadata, but does not need to make use of the extensive
  other BuilderRun features. This lightweight partial reimplementation
  allows unit tests to be much faster.
  """
  def __init__(self, fake_db=None):
    self.fake_db = fake_db
    metadata_dict = {'buildbot-master-name': constants.WATERFALL_INTERNAL}
    FakeAttrs = collections.namedtuple('FakeAttrs', ['metadata'])
    self.attrs = FakeAttrs(metadata=metadata_lib.CBuildbotMetadata(
        metadata_dict=metadata_dict))

  def GetCIDBHandle(self):
    """Get the build_id and cidb handle, if available.

    Returns:
      A (build_id, CIDBConnection) tuple if fake_db is set up and a build_id is
      known in metadata. Otherwise, (None, None).
    """
    try:
      build_id = self.attrs.metadata.GetValue('build_id')
    except KeyError:
      return (None, None)

    if build_id is not None and self.fake_db:
      return (build_id, self.fake_db)

    return (None, None)


# pylint: disable=protected-access
class MoxBase(patch_unittest.MockPatchBase, cros_test_lib.MoxTestCase):
  """Base class for other test suites with numbers mocks patched in."""

  def setUp(self):
    self.build_root = 'fakebuildroot'
    self.manager = parallel.Manager()
    self.mox.StubOutWithMock(validation_pool, '_RunCommand')
    self.PatchObject(gob_util, 'CreateHttpConn',
                     side_effect=AssertionError('Test should not contact GoB'))
    self.PatchObject(tree_status, 'IsTreeOpen', return_value=True)
    self.PatchObject(tree_status, 'WaitForTreeStatus',
                     return_value=constants.TREE_OPEN)
    self.fake_db = fake_cidb.FakeCIDBConnection()
    cidb.CIDBConnectionFactory.SetupMockCidb(self.fake_db)
    # Suppress all gerrit access; having this occur is generally a sign
    # the code is either misbehaving, or that the tests are bad.
    self.mox.StubOutWithMock(gerrit.GerritHelper, 'Query')
    self.PatchObject(gs.GSContext, 'Cat', side_effect=gs.GSNoSuchKey())
    self.PatchObject(gs.GSContext, 'Copy')
    self.PatchObject(gs.GSContext, 'Exists', return_value=False)
    self.PatchObject(gs.GSCounter, 'Increment')

  def tearDown(self):
    cidb.CIDBConnectionFactory.ClearMock()

  def MakeHelper(self, cros_internal=None, cros=None):
    # pylint: disable=W0201
    if cros_internal:
      cros_internal = self.mox.CreateMock(gerrit.GerritHelper)
      cros_internal.version = '2.2'
      cros_internal.remote = constants.INTERNAL_REMOTE
    if cros:
      cros = self.mox.CreateMock(gerrit.GerritHelper)
      cros.remote = constants.EXTERNAL_REMOTE
      cros.version = '2.2'
    return validation_pool.HelperPool(cros_internal=cros_internal,
                                      cros=cros)


class TestPatchSeries(MoxBase):
  """Tests resolution and applying logic of validation_pool.ValidationPool."""

  @contextlib.contextmanager
  def _ValidateTransactionCall(self, _changes):
    yield

  def GetPatchSeries(self, helper_pool=None):
    if helper_pool is None:
      helper_pool = self.MakeHelper(cros_internal=True, cros=True)
    series = validation_pool.PatchSeries(self.build_root, helper_pool)

    # Suppress transactions.
    series._Transaction = self._ValidateTransactionCall
    series.GetGitRepoForChange = \
        lambda change, **kwargs: os.path.join(self.build_root, change.project)

    return series

  def assertPath(self, _patch, return_value, path):
    self.assertEqual(path, os.path.join(self.build_root, _patch.project))
    if isinstance(return_value, Exception):
      raise return_value
    return return_value

  def SetPatchDeps(self, patch, parents=(), cq=()):
    """Set the dependencies of |patch|.

    Args:
      patch: The patch to process.
      parents: A set of strings to set as parents of |patch|.
      cq: A set of strings to set as paladin dependencies of |patch|.
    """
    patch.GerritDependencies = (
        lambda: [cros_patch.ParsePatchDep(x) for x in parents])
    patch.PaladinDependencies = functools.partial(
        self.assertPath, patch, [cros_patch.ParsePatchDep(x) for x in cq])
    patch.Fetch = functools.partial(
        self.assertPath, patch, patch.sha1)

  def _ValidatePatchApplyManifest(self, value):
    self.assertTrue(isinstance(value, MockManifest))
    self.assertEqual(value.root, self.build_root)
    return True

  def SetPatchApply(self, patch, trivial=False):
    self.mox.StubOutWithMock(patch, 'ApplyAgainstManifest')
    return patch.ApplyAgainstManifest(
        mox.Func(self._ValidatePatchApplyManifest),
        trivial=trivial)

  def assertResults(self, series, changes, applied=(), failed_tot=(),
                    failed_inflight=(), frozen=True):
    manifest = MockManifest(self.build_root)
    result = series.Apply(changes, frozen=frozen, manifest=manifest)

    _GetIds = lambda seq: [x.id for x in seq]
    _GetFailedIds = lambda seq: _GetIds(x.patch for x in seq)

    applied_result = _GetIds(result[0])
    failed_tot_result, failed_inflight_result = map(_GetFailedIds, result[1:])

    applied = _GetIds(applied)
    failed_tot = _GetIds(failed_tot)
    failed_inflight = _GetIds(failed_inflight)

    self.maxDiff = None
    self.assertEqual(applied, applied_result)
    self.assertItemsEqual(failed_inflight, failed_inflight_result)
    self.assertItemsEqual(failed_tot, failed_tot_result)
    return result

  def testApplyWithDeps(self):
    """Test that we can apply changes correctly and respect deps.

    This tests a simple out-of-order change where change1 depends on change2
    but tries to get applied before change2.  What should happen is that
    we should notice change2 is a dep of change1 and apply it first.
    """
    series = self.GetPatchSeries()

    patch1, patch2 = patches = self.GetPatches(2)

    self.SetPatchDeps(patch2)
    self.SetPatchDeps(patch1, [patch2.id])

    self.SetPatchApply(patch2)
    self.SetPatchApply(patch1)

    self.mox.ReplayAll()
    self.assertResults(series, patches, [patch2, patch1])
    self.mox.VerifyAll()

  def testSha1Deps(self):
    """Test that we can apply changes correctly and respect sha1 deps.

    This tests a simple out-of-order change where change1 depends on change2
    but tries to get applied before change2.  What should happen is that
    we should notice change2 is a dep of change1 and apply it first.
    """
    series = self.GetPatchSeries()

    patch1, patch2, patch3 = patches = self.GetPatches(3)
    patch2.change_id = patch2.id = patch2.sha1
    patch3.change_id = patch3.id = '*' + patch3.sha1
    patch3.remote = constants.INTERNAL_REMOTE

    self.SetPatchDeps(patch1, [patch2.sha1])
    self.SetPatchDeps(patch2, ['*%s' % patch3.sha1])
    self.SetPatchDeps(patch3)

    self.SetPatchApply(patch2)
    self.SetPatchApply(patch3)
    self.SetPatchApply(patch1)

    self.mox.ReplayAll()
    self.assertResults(series, patches, [patch3, patch2, patch1])
    self.mox.VerifyAll()

  def testGerritNumberDeps(self):
    """Test that we can apply changes correctly and respect gerrit number deps.

    This tests a simple out-of-order change where change1 depends on change2
    but tries to get applied before change2.  What should happen is that
    we should notice change2 is a dep of change1 and apply it first.
    """
    series = self.GetPatchSeries()

    patch1, patch2, patch3 = patches = self.GetPatches(3)

    self.SetPatchDeps(patch3, cq=[patch1.gerrit_number])
    self.SetPatchDeps(patch2, cq=[patch3.gerrit_number])
    self.SetPatchDeps(patch1, cq=[patch2.id])

    self.SetPatchApply(patch3)
    self.SetPatchApply(patch2)
    self.SetPatchApply(patch1)

    self.mox.ReplayAll()
    self.assertResults(series, patches, patches)
    self.mox.VerifyAll()

  def testGerritLazyMapping(self):
    """Given a patch lacking a gerrit number, via gerrit, map it to that change.

    Literally, this ensures that local patches pushed up- lacking a gerrit
    number- are mapped back to a changeid via asking gerrit for that number,
    then the local matching patch is used if available.
    """
    series = self.GetPatchSeries()

    patch1 = self.MockPatch()
    self.PatchObject(patch1, 'LookupAliases', return_value=[patch1.id])
    patch2 = self.MockPatch(change_id=int(patch1.change_id[1:]))
    patch3 = self.MockPatch()

    self.SetPatchDeps(patch3, cq=[patch2.gerrit_number])
    self.SetPatchDeps(patch2)
    self.SetPatchDeps(patch1)

    self.SetPatchApply(patch1)
    self.SetPatchApply(patch3)

    self._SetQuery(series, patch2, query=patch2.gerrit_number).AndReturn(patch2)

    self.mox.ReplayAll()
    applied = self.assertResults(series, [patch1, patch3], [patch3, patch1])[0]
    self.assertTrue(applied[0] is patch3)
    self.assertTrue(applied[1] is patch1)
    self.mox.VerifyAll()

  def testCrosGerritDeps(self, cros_internal=True):
    """Test that we can apply changes correctly and respect deps.

    This tests a simple out-of-order change where change1 depends on change3
    but tries to get applied before change2.  What should happen is that
    we should notice change2 is a dep of change1 and apply it first.
    """
    helper_pool = self.MakeHelper(cros_internal=cros_internal, cros=True)
    series = self.GetPatchSeries(helper_pool=helper_pool)

    patch1 = self.MockPatch(remote=constants.EXTERNAL_REMOTE)
    patch2 = self.MockPatch(remote=constants.INTERNAL_REMOTE)
    patch3 = self.MockPatch(remote=constants.EXTERNAL_REMOTE)
    patches = [patch1, patch2, patch3]
    if cros_internal:
      applied_patches = [patch3, patch1, patch2]
    else:
      applied_patches = [patch3, patch1]

    self.SetPatchDeps(patch1, [patch3.id])
    self.SetPatchDeps(patch2)
    self.SetPatchDeps(patch3, cq=[patch2.id])

    if cros_internal:
      self.SetPatchApply(patch2)
    self.SetPatchApply(patch1)
    self.SetPatchApply(patch3)

    self.mox.ReplayAll()
    self.assertResults(series, patches, applied_patches)
    self.mox.VerifyAll()

  def testExternalCrosGerritDeps(self):
    """Test that we exclude internal deps on external trybot."""
    self.testCrosGerritDeps(cros_internal=False)

  @staticmethod
  def _SetQuery(series, change, query=None):
    helper = series._helper_pool.GetHelper(change.remote)
    query = change.id if query is None else query
    return helper.QuerySingleRecord(query, must_match=True)

  def testApplyMissingDep(self):
    """Test that we don't try to apply a change without met dependencies.

    Patch2 is in the validation pool that depends on Patch1 (which is not)
    Nothing should get applied.
    """
    series = self.GetPatchSeries()

    patch1, patch2 = self.GetPatches(2)

    self.SetPatchDeps(patch2, [patch1.id])
    self._SetQuery(series, patch1).AndReturn(patch1)

    self.mox.ReplayAll()
    self.assertResults(series, [patch2],
                       [], [patch2])
    self.mox.VerifyAll()

  def testApplyWithCommittedDeps(self):
    """Test that we apply a change with dependency already committed."""
    series = self.GetPatchSeries()

    # Use for basic commit check.
    patch1 = self.GetPatches(1, is_merged=True)
    patch2 = self.GetPatches(1)

    self.SetPatchDeps(patch2, [patch1.id])
    self._SetQuery(series, patch1).AndReturn(patch1)
    self.SetPatchApply(patch2)

    # Used to ensure that an uncommitted change put in the lookup cache
    # isn't invalidly pulled into the graph...
    patch3, patch4, patch5 = self.GetPatches(3)

    self._SetQuery(series, patch3).AndReturn(patch3)
    self.SetPatchDeps(patch4, [patch3.id])
    self.SetPatchDeps(patch5, [patch3.id])

    self.mox.ReplayAll()
    self.assertResults(series, [patch2, patch4, patch5], [patch2],
                       [patch4, patch5])
    self.mox.VerifyAll()

  def testCyclicalDeps(self):
    """Verify that the machinery handles cycles correctly."""
    series = self.GetPatchSeries()

    patch1, patch2, patch3 = patches = self.GetPatches(3)

    self.SetPatchDeps(patch1, [patch2.id])
    self.SetPatchDeps(patch2, cq=[patch3.id])
    self.SetPatchDeps(patch3, [patch1.id])

    self.SetPatchApply(patch1)
    self.SetPatchApply(patch2)
    self.SetPatchApply(patch3)

    self.mox.ReplayAll()
    self.assertResults(series, patches, [patch2, patch1, patch3])
    self.mox.VerifyAll()

  def testComplexCyclicalDeps(self, fail=False):
    """Verify handling of two interdependent cycles."""
    series = self.GetPatchSeries()

    # Create two cyclically interdependent patch chains.
    # Example: Two patch series A1<-A2<-A3<-A4 and B1<-B2<-B3<-B4. A1 has a
    # CQ-DEPEND on B4 and B1 has a CQ-DEPEND on A4, so all of the patches must
    # be committed together.
    chain1, chain2 = chains = self.GetPatches(4), self.GetPatches(4)
    for chain in chains:
      (other_chain,) = [x for x in chains if x != chain]
      self.SetPatchDeps(chain[0], [], cq=[other_chain[-1].id])
      for i in range(1, len(chain)):
        self.SetPatchDeps(chain[i], [chain[i-1].id])

    # Apply the second-last patch first, so that the last patch in the series
    # will be pulled in via the CQ-DEPEND on the other patch chain.
    to_apply = [chain1[-2]] + [x for x in (chain1 + chain2) if x != chain1[-2]]

    # All of the patches but chain[-1] were applied successfully.
    for patch in chain1[:-1] + chain2:
      self.SetPatchApply(patch)

    if fail:
      # Pretend that chain[-1] failed to apply.
      res = self.SetPatchApply(chain1[-1])
      res.AndRaise(cros_patch.ApplyPatchException(chain1[-1]))
      applied = []
      failed_tot = to_apply
    else:
      # We apply the patches in this order since the last patch in chain1
      # is pulled in via CQ-DEPEND.
      self.SetPatchApply(chain1[-1])
      applied = chain1[:-1] + chain2 + [chain1[-1]]
      failed_tot = []

    self.mox.ReplayAll()
    self.assertResults(series, to_apply, applied=applied, failed_tot=failed_tot)
    self.mox.VerifyAll()

  def testFailingComplexCyclicalDeps(self):
    """Verify handling of failing interlocked cycles."""
    self.testComplexCyclicalDeps(fail=True)

  def testApplyPartialFailures(self):
    """Test that can apply changes correctly when one change fails to apply.

    This tests a simple change order where 1 depends on 2 and 1 fails to apply.
    Only 1 should get tried as 2 will abort once it sees that 1 can't be
    applied.  3 with no dependencies should go through fine.

    Since patch1 fails to apply, we should also get a call to handle the
    failure.
    """
    series = self.GetPatchSeries()

    patch1, patch2, patch3, patch4 = patches = self.GetPatches(4)

    self.SetPatchDeps(patch1)
    self.SetPatchDeps(patch2, [patch1.id])
    self.SetPatchDeps(patch3)
    self.SetPatchDeps(patch4)

    self.SetPatchApply(patch1).AndRaise(
        cros_patch.ApplyPatchException(patch1))

    self.SetPatchApply(patch3)
    self.SetPatchApply(patch4).AndRaise(
        cros_patch.ApplyPatchException(patch1, inflight=True))

    self.mox.ReplayAll()
    self.assertResults(series, patches,
                       [patch3], [patch2, patch1], [patch4])
    self.mox.VerifyAll()

  def testComplexApply(self):
    """More complex deps test.

    This tests a total of 2 change chains where the first change we see
    only has a partial chain with the 3rd change having the whole chain i.e.
    1->2, 3->1->2.  Since we get these in the order 1,2,3,4,5 the order we
    should apply is 2,1,3,4,5.

    This test also checks the patch order to verify that Apply re-orders
    correctly based on the chain.
    """
    series = self.GetPatchSeries()

    patch1, patch2, patch3, patch4, patch5 = patches = self.GetPatches(5)

    self.SetPatchDeps(patch1, [patch2.id])
    self.SetPatchDeps(patch2)
    self.SetPatchDeps(patch3, [patch1.id, patch2.id])
    self.SetPatchDeps(patch4, cq=[patch5.id])
    self.SetPatchDeps(patch5)

    for patch in (patch2, patch1, patch3, patch4, patch5):
      self.SetPatchApply(patch)

    self.mox.ReplayAll()
    self.assertResults(
        series, patches, [patch2, patch1, patch3, patch4, patch5])
    self.mox.VerifyAll()

  def testApplyStandalonePatches(self):
    """Simple apply of two changes with no dependent CL's."""
    series = self.GetPatchSeries()

    patches = self.GetPatches(3)

    for patch in patches:
      self.SetPatchDeps(patch)

    for patch in patches:
      self.SetPatchApply(patch)

    self.mox.ReplayAll()
    self.assertResults(series, patches, patches)
    self.mox.VerifyAll()


def MakePool(overlays=constants.PUBLIC_OVERLAYS, build_number=1,
             builder_name='foon', is_master=True, dryrun=True,
             fake_db=None, **kwargs):
  """Helper for creating ValidationPool objects for tests."""
  kwargs.setdefault('changes', [])
  build_root = kwargs.pop('build_root', '/fake_root')

  builder_run = FakeBuilderRun(fake_db)
  if fake_db:
    build_id = fake_db.InsertBuild(
        builder_name, constants.WATERFALL_INTERNAL, build_number,
        'build-config', 'bot hostname')
    builder_run.attrs.metadata.UpdateWithDict({'build_id': build_id})


  pool = validation_pool.ValidationPool(
      overlays, build_root, build_number, builder_name, is_master,
      dryrun, builder_run=builder_run, **kwargs)
  return pool


class MockPatchSeries(partial_mock.PartialMock):
  """Mock the PatchSeries functions."""
  TARGET = 'chromite.cbuildbot.validation_pool.PatchSeries'
  ATTRS = ('GetDepsForChange', '_GetGerritPatch', '_LookupHelper')

  def __init__(self):
    partial_mock.PartialMock.__init__(self)
    self.deps = {}
    self.cq_deps = {}

  def SetGerritDependencies(self, patch, deps):
    """Add |deps| to the Gerrit dependencies of |patch|."""
    self.deps[patch] = deps

  def SetCQDependencies(self, patch, deps):
    """Add |deps| to the CQ dependencies of |patch|."""
    self.cq_deps[patch] = deps

  def GetDepsForChange(self, _inst, patch):
    return self.deps.get(patch, []), self.cq_deps.get(patch, [])

  def _GetGerritPatch(self, _inst, dep, **_kwargs):
    return dep

  _LookupHelper = mock.MagicMock()


class TestSubmitChange(MoxBase):
  """Test suite related to submitting changes."""

  def setUp(self):
    self.orig_timeout = validation_pool.SUBMITTED_WAIT_TIMEOUT
    validation_pool.SUBMITTED_WAIT_TIMEOUT = 4

  def tearDown(self):
    validation_pool.SUBMITTED_WAIT_TIMEOUT = self.orig_timeout

  def _TestSubmitChange(self, results, build_id=31337):
    """Test submitting a change with the given results."""
    results = [cros_test_lib.EasyAttr(status=r) for r in results]
    change = self.MockPatch(change_id=12345, patch_number=1)
    pool = self.mox.CreateMock(validation_pool.ValidationPool)
    pool.dryrun = False
    pool._run = FakeBuilderRun(self.fake_db)
    pool._run.attrs.metadata.UpdateWithDict({'build_id': build_id})
    pool._helper_pool = self.mox.CreateMock(validation_pool.HelperPool)
    helper = self.mox.CreateMock(validation_pool.gerrit.GerritHelper)

    self.mox.StubOutWithMock(validation_pool.ValidationPool,
                             '_InsertCLActionToDatabase')

    # Prepare replay script.
    pool._helper_pool.ForChange(change).AndReturn(helper)
    helper.SubmitChange(change, dryrun=False)
    pool._InsertCLActionToDatabase(change, mox.IgnoreArg())
    for result in results:
      helper.QuerySingleRecord(change.gerrit_number).AndReturn(result)
    self.mox.ReplayAll()

    # Verify results.
    retval = validation_pool.ValidationPool._SubmitChange(pool, change)
    self.mox.VerifyAll()
    return retval

  def testSubmitChangeMerged(self):
    """Submit one change to gerrit, status MERGED."""
    self.assertTrue(self._TestSubmitChange(['MERGED']))

  def testSubmitChangeSubmitted(self):
    """Submit one change to gerrit, stuck on SUBMITTED."""
    # The query will be retried 1 more time than query timeout.
    results = ['SUBMITTED' for _i in
               xrange(validation_pool.SUBMITTED_WAIT_TIMEOUT + 1)]
    self.assertTrue(self._TestSubmitChange(results))

  def testSubmitChangeSubmittedToMerged(self):
    """Submit one change to gerrit, status SUBMITTED then MERGED."""
    results = ['SUBMITTED', 'SUBMITTED', 'MERGED']
    self.assertTrue(self._TestSubmitChange(results))

  def testSubmitChangeFailed(self):
    """Submit one change to gerrit, reported back as NEW."""
    self.assertFalse(self._TestSubmitChange(['NEW']))


class ValidationFailureOrTimeout(MoxBase):
  """Tests that HandleValidationFailure and HandleValidationTimeout functions.

  These tests check that HandleValidationTimeout and HandleValidationFailure
  reject (i.e. zero out the CQ field) of the correct number of patches, under
  various circumstances.
  """

  _PATCH_MESSAGE = 'Your patch failed.'
  _BUILD_MESSAGE = 'Your build failed.'

  def setUp(self):
    self._patches = self.GetPatches(3)
    self._pool = MakePool(changes=self._patches, fake_db=self.fake_db)

    self.PatchObject(
        triage_lib.CalculateSuspects, 'FindSuspects',
        return_value=self._patches)
    self.PatchObject(
        validation_pool.ValidationPool, '_CreateValidationFailureMessage',
        return_value=self._PATCH_MESSAGE)
    self.PatchObject(validation_pool.ValidationPool, 'SendNotification')
    self.PatchObject(validation_pool.ValidationPool, 'RemoveReady')
    self.PatchObject(validation_pool.ValidationPool, 'ReloadChanges',
                     return_value=self._patches)
    self.PatchObject(triage_lib.CalculateSuspects, 'OnlyLabFailures',
                     return_value=False)
    self.PatchObject(triage_lib.CalculateSuspects, 'OnlyInfraFailures',
                     return_value=False)
    self.StartPatcher(parallel_unittest.ParallelMock())

  def testPatchesWereRejectedByFailure(self):
    """Tests that all patches are rejected by failure."""
    self._pool.HandleValidationFailure([self._BUILD_MESSAGE])
    self.assertEqual(len(self._patches), self._pool.RemoveReady.call_count)

  def testPatchesWereRejectedByTimeout(self):
    self._pool.HandleValidationTimeout()
    self.assertEqual(len(self._patches), self._pool.RemoveReady.call_count)

  def testNoSuspectsWithFailure(self):
    """Tests no change is blamed when there is no suspect."""
    self.PatchObject(triage_lib.CalculateSuspects, 'FindSuspects',
                     return_value=[])
    self._pool.HandleValidationFailure([self._BUILD_MESSAGE])
    self.assertEqual(0, self._pool.RemoveReady.call_count)

  def testPreCQ(self):
    for change in self._patches:
      self._pool.UpdateCLPreCQStatus(change, constants.CL_STATUS_PASSED)
    self._pool.pre_cq = True
    self._pool.HandleValidationFailure([self._BUILD_MESSAGE])
    self.assertEqual(0, self._pool.RemoveReady.call_count)

  def testPatchesWereNotRejectedByInsaneFailure(self):
    self._pool.HandleValidationFailure([self._BUILD_MESSAGE], sanity=False)
    self.assertEqual(0, self._pool.RemoveReady.call_count)


class TestCoreLogic(MoxBase):
  """Tests resolution and applying logic of validation_pool.ValidationPool."""

  def setUp(self):
    self.mox.StubOutWithMock(validation_pool.PatchSeries, 'Apply')
    self.mox.StubOutWithMock(validation_pool.PatchSeries, 'ApplyChange')
    self.patch_mock = self.StartPatcher(MockPatchSeries())
    funcs = ['SendNotification', '_SubmitChange']
    for func in funcs:
      self.mox.StubOutWithMock(validation_pool.ValidationPool, func)
    self.PatchObject(validation_pool.ValidationPool, 'ReloadChanges',
                     side_effect=lambda x: x)
    self.StartPatcher(parallel_unittest.ParallelMock())

  def MakePool(self, *args, **kwargs):
    """Helper for creating ValidationPool objects for Mox tests."""
    handlers = kwargs.pop('handlers', False)
    kwargs['build_root'] = self.build_root
    pool = MakePool(*args, **kwargs)
    funcs = ['HandleApplySuccess', '_HandleApplyFailure',
             '_HandleCouldNotApply', '_HandleCouldNotSubmit',
             '_HandleFailedToApplyDueToInflightConflict']
    if handlers:
      for func in funcs:
        self.mox.StubOutWithMock(pool, func)
    return pool

  def MakeFailure(self, patch, inflight=True):
    return cros_patch.ApplyPatchException(patch, inflight=inflight)

  def GetPool(self, changes, applied=(), tot=(), inflight=(), **kwargs):
    pool = self.MakePool(changes=changes, fake_db=self.fake_db, **kwargs)
    applied = list(applied)
    tot = [self.MakeFailure(x, inflight=False) for x in tot]
    inflight = [self.MakeFailure(x, inflight=True) for x in inflight]
    # pylint: disable=E1120,E1123
    validation_pool.PatchSeries.Apply(
        changes, manifest=mox.IgnoreArg()
        ).AndReturn((applied, tot, inflight))

    for patch in applied:
      pool.HandleApplySuccess(patch, mox.IgnoreArg()).AndReturn(None)

    if tot:
      pool._HandleApplyFailure(tot).AndReturn(None)

    for failure in inflight:
      pool._HandleFailedToApplyDueToInflightConflict(
          failure.patch).AndReturn(None)

    # We stash this on the pool object so we can reuse it during validation.
    # We could stash this in the test instances, but that would break
    # for any tests that do multiple pool instances.

    pool._test_data = (changes, applied, tot, inflight)

    return pool

  def testApplySlavePool(self):
    """Verifies that slave calls ApplyChange() directly for each patch."""
    slave_pool = self.MakePool(is_master=False)
    patches = self.GetPatches(3)
    slave_pool.changes = patches
    for patch in patches:
      # pylint: disable=E1120, E1123
      validation_pool.PatchSeries.ApplyChange(patch, manifest=mox.IgnoreArg())

    self.mox.ReplayAll()
    self.assertEqual(True, slave_pool.ApplyPoolIntoRepo())
    self.mox.VerifyAll()

  def runApply(self, pool, result):
    self.assertEqual(result, pool.ApplyPoolIntoRepo())
    self.assertEqual(pool.changes, pool._test_data[1])
    failed_inflight = pool.changes_that_failed_to_apply_earlier
    expected_inflight = set(pool._test_data[3])
    # Intersect the results, since it's possible there were results failed
    # results that weren't related to the ApplyPoolIntoRepo call.
    self.assertEqual(set(failed_inflight).intersection(expected_inflight),
                     expected_inflight)

    self.assertEqual(pool.changes, pool._test_data[1])

  def testPatchSeriesInteraction(self):
    """Verify the interaction between PatchSeries and ValidationPool.

    Effectively, this validates data going into PatchSeries, and coming back
    out; verifies the hand off to _Handle* functions, but no deeper.
    """
    patches = self.GetPatches(3)

    apply_pool = self.GetPool(patches, applied=patches, handlers=True)
    all_inflight = self.GetPool(patches, inflight=patches, handlers=True)
    all_tot = self.GetPool(patches, tot=patches, handlers=True)
    mixed = self.GetPool(patches, tot=patches[0:1], inflight=patches[1:2],
                         applied=patches[2:3], handlers=True)

    self.mox.ReplayAll()
    self.runApply(apply_pool, True)
    self.runApply(all_inflight, False)
    self.runApply(all_tot, False)
    self.runApply(mixed, True)
    self.mox.VerifyAll()

  def testHandleApplySuccess(self):
    """Validate steps taken for successfull application."""
    patch = self.GetPatches(1)
    pool = self.MakePool(fake_db=self.fake_db)
    pool.SendNotification(patch, mox.StrContains('has picked up your change'),
                          build_log=mox.IgnoreArg())
    self.mox.ReplayAll()
    pool.HandleApplySuccess(patch, build_log=mox.IgnoreArg())
    self.mox.VerifyAll()

  def testHandleApplyFailure(self):
    failures = [cros_patch.ApplyPatchException(x) for x in self.GetPatches(4)]

    notified_patches = failures[:2]
    unnotified_patches = failures[2:]
    master_pool = self.MakePool(dryrun=False)
    slave_pool = self.MakePool(is_master=False)

    self.mox.StubOutWithMock(gerrit.GerritHelper, 'RemoveReady')

    for failure in notified_patches:
      master_pool.SendNotification(
          failure.patch,
          mox.StrContains('failed to apply your change'),
          failure=mox.IgnoreArg())
      # This pylint suppressin shouldn't be necessary, but pylint is invalidly
      # thinking that the first arg isn't passed in; we suppress it to suppress
      # the pylnt bug.
      # pylint: disable=E1120
      gerrit.GerritHelper.RemoveReady(failure.patch, dryrun=False)

    self.mox.ReplayAll()
    master_pool._HandleApplyFailure(notified_patches)
    slave_pool._HandleApplyFailure(unnotified_patches)
    self.mox.VerifyAll()

  def _setUpSubmit(self):
    pool = self.MakePool(dryrun=False, handlers=True)
    patches = self.GetPatches(3)
    failed = self.GetPatches(3)
    pool.changes = patches[:]
    # While we don't do anything w/ these patches, that's
    # intentional; we're verifying that it isn't submitted
    # if there is a failure.
    pool.changes_that_failed_to_apply_earlier = failed[:]

    return (pool, patches, failed)

  def testSubmitPoolFailures(self):
    """Tests that a fatal exception is raised."""
    pool, patches, _failed = self._setUpSubmit()
    patch1, patch2, patch3 = patches

    pool._SubmitChange(patch1).AndReturn(True)
    pool._SubmitChange(patch2).AndReturn(False)

    pool._HandleCouldNotSubmit(patch2, mox.IgnoreArg()).InAnyOrder()
    pool._HandleCouldNotSubmit(patch3, mox.IgnoreArg()).InAnyOrder()

    self.mox.ReplayAll()
    self.assertRaises(validation_pool.FailedToSubmitAllChangesException,
                      pool.SubmitPool)
    self.mox.VerifyAll()

  def testSubmitPool(self):
    """Tests that we can submit a pool of patches."""
    pool, patches, failed = self._setUpSubmit()

    for patch in patches:
      pool._SubmitChange(patch).AndReturn(True)

    pool._HandleApplyFailure(failed)

    self.mox.ReplayAll()
    pool.SubmitPool()
    self.mox.VerifyAll()

  def testSubmitNonManifestChanges(self):
    """Simple test to make sure we can submit non-manifest changes."""
    pool, patches, _failed = self._setUpSubmit()
    pool.non_manifest_changes = patches[:]

    for patch in patches:
      pool._SubmitChange(patch).AndReturn(True)

    self.mox.ReplayAll()
    pool.SubmitNonManifestChanges()
    self.mox.VerifyAll()

  def testUnhandledExceptions(self):
    """Test that CQ doesn't loop due to unhandled Exceptions."""
    pool, patches, _failed = self._setUpSubmit()

    class MyException(Exception):
      """"Unique Exception used for testing."""

    def VerifyCQError(patch, error):
      cq_error = validation_pool.InternalCQError(patch, error.message)
      return str(error) == str(cq_error)

    # pylint: disable=E1120,E1123
    validation_pool.PatchSeries.Apply(
        patches, manifest=mox.IgnoreArg()).AndRaise(MyException)
    errors = [mox.Func(functools.partial(VerifyCQError, x)) for x in patches]
    pool._HandleApplyFailure(errors).AndReturn(None)

    self.mox.ReplayAll()
    self.assertRaises(MyException, pool.ApplyPoolIntoRepo)
    self.mox.VerifyAll()

  def testFilterDependencyErrors(self):
    """Verify that dependency errors are correctly filtered out."""
    failures = [cros_patch.ApplyPatchException(x) for x in self.GetPatches(2)]
    failures += [cros_patch.DependencyError(x, y) for x, y in
                 zip(self.GetPatches(2), failures)]
    failures[0].patch.approval_timestamp = time.time()
    failures[-1].patch.approval_timestamp = time.time()
    self.mox.ReplayAll()
    result = validation_pool.ValidationPool._FilterDependencyErrors(failures)
    self.assertEquals(set(failures[:-1]), set(result))
    self.mox.VerifyAll()

  def testFilterSpeculativeErrors(self):
    """Filter out dependency errors for speculative patches."""
    failures = [cros_patch.ApplyPatchException(x) for x in self.GetPatches(2)]
    failures += [cros_patch.DependencyError(x, y) for x, y in
                 zip(self.GetPatches(2), failures)]
    self.PatchObject(failures[-1].patch, 'HasReadyFlag', return_value=False)
    self.mox.ReplayAll()
    result = validation_pool.ValidationPool._FilterDependencyErrors(failures)
    self.assertEquals(set(failures[:-1]), set(result))
    self.mox.VerifyAll()

  def testFilterNonCrosProjects(self):
    """Runs through a filter of own manifest and fake changes.

    This test should filter out the tacos/chromite project as its not real.
    """
    base_func = itertools.cycle(['chromiumos', 'chromeos']).next
    patches = self.GetPatches(10)
    for patch in patches:
      patch.project = '%s/%i' % (base_func(), _GetNumber())
      patch.tracking_branch = str(_GetNumber())

    non_cros_patches = self.GetPatches(2)
    for patch in non_cros_patches:
      patch.project = str(_GetNumber())

    filtered_patches = patches[:4]
    allowed_patches = []
    projects = {}
    for idx, patch in enumerate(patches[4:]):
      fails = bool(idx % 2)
      # Vary the revision so we can validate that it checks the branch.
      revision = ('monkeys' if fails
                  else 'refs/heads/%s' % patch.tracking_branch)
      if fails:
        filtered_patches.append(patch)
      else:
        allowed_patches.append(patch)
      projects.setdefault(patch.project, {})['revision'] = revision

    manifest = MockManifest(self.build_root, projects=projects)
    for patch in allowed_patches:
      patch.GetCheckout = lambda *_args, **_kwargs: True
    for patch in filtered_patches:
      patch.GetCheckout = lambda *_args, **_kwargs: False

    # Mark the last two patches as not commit ready.
    for p in patches[-2:]:
      p.IsMergeable = lambda *_args, **_kwargs: False

    # Non-manifest patches that aren't commit ready should be skipped.
    filtered_patches = filtered_patches[:-1]

    self.mox.ReplayAll()
    results = validation_pool.ValidationPool._FilterNonCrosProjects(
        patches + non_cros_patches, manifest)

    def compare(list1, list2):
      mangle = lambda c: (c.id, c.project, c.tracking_branch)
      self.assertEqual(
          list1, list2,
          msg=('Comparison failed:\n list1: %r\n list2: %r'
               % (map(mangle, list1), map(mangle, list2))))

    compare(results[0], allowed_patches)
    compare(results[1], filtered_patches)


class TestPickling(cros_test_lib.TempDirTestCase):
  """Tests to validate pickling of ValidationPool, covering CQ's needs"""

  def testSelfCompatibility(self):
    """Verify compatibility of current git HEAD against itself."""
    self._CheckTestData(self._GetTestData())

  @cros_test_lib.NetworkTest()
  def testToTCompatibility(self):
    """Validate that ToT can use our pickles, and that we can use ToT's data."""
    repo = os.path.join(self.tempdir, 'chromite')
    reference = os.path.abspath(__file__)
    reference = os.path.normpath(os.path.join(reference, '../../'))

    repository.CloneGitRepo(
        repo,
        '%s/chromiumos/chromite' % constants.EXTERNAL_GOB_URL,
        reference=reference)

    code = """
import sys
from chromite.cbuildbot import validation_pool_unittest
if not hasattr(validation_pool_unittest, 'TestPickling'):
  sys.exit(0)
sys.stdout.write(validation_pool_unittest.TestPickling.%s)
"""

    # Verify ToT can take our pickle.
    cros_build_lib.RunCommand(
        ['python', '-c', code % '_CheckTestData(sys.stdin.read())'],
        cwd=self.tempdir, print_cmd=False, capture_output=True,
        input=self._GetTestData())

    # Verify we can handle ToT's pickle.
    ret = cros_build_lib.RunCommand(
        ['python', '-c', code % '_GetTestData()'],
        cwd=self.tempdir, print_cmd=False, capture_output=True)

    self._CheckTestData(ret.output)

  @staticmethod
  def _GetCrosInternalPatch(patch_info):
    return cros_patch.GerritPatch(
        patch_info,
        constants.INTERNAL_REMOTE,
        constants.INTERNAL_GERRIT_URL)

  @staticmethod
  def _GetCrosPatch(patch_info):
    return cros_patch.GerritPatch(
        patch_info,
        constants.EXTERNAL_REMOTE,
        constants.EXTERNAL_GERRIT_URL)

  @classmethod
  def _GetTestData(cls):
    ids = [cros_patch.MakeChangeId() for _ in xrange(3)]
    changes = [cls._GetCrosInternalPatch(GetTestJson(ids[0]))]
    non_os = [cls._GetCrosPatch(GetTestJson(ids[1]))]
    conflicting = [cls._GetCrosInternalPatch(GetTestJson(ids[2]))]
    conflicting = [cros_patch.PatchException(x)for x in conflicting]
    pool = validation_pool.ValidationPool(
        constants.PUBLIC_OVERLAYS,
        '/fake/pathway', 1,
        'testing', True, True,
        changes=changes, non_os_changes=non_os,
        conflicting_changes=conflicting)
    return pickle.dumps([pool, changes, non_os, conflicting])

  @staticmethod
  def _CheckTestData(data):
    results = pickle.loads(data)
    pool, changes, non_os, conflicting = results
    def _f(source, value, getter=None):
      if getter is None:
        getter = lambda x: x
      assert len(source) == len(value)
      for s_item, v_item in zip(source, value):
        assert getter(s_item).id == getter(v_item).id
        assert getter(s_item).remote == getter(v_item).remote
    _f(pool.changes, changes)
    _f(pool.non_manifest_changes, non_os)
    _f(pool.changes_that_failed_to_apply_earlier, conflicting,
       getter=lambda s: getattr(s, 'patch', s))
    return ''


class TestPrintLinks(MoxBase):
  """Tests that change links can be printed."""
  def testPrintLinks(self):
    changes = self.GetPatches(3)
    with parallel_unittest.ParallelMock():
      validation_pool.ValidationPool.PrintLinksToChanges(changes)


class TestCreateValidationFailureMessage(MoxBase):
  """Tests validation_pool.ValidationPool._CreateValidationFailureMessage"""

  def _AssertMessage(self, change, suspects, messages, sanity=True,
                     infra_fail=False, lab_fail=False, no_stat=None):
    """Call the _CreateValidationFailureMessage method.

    Args:
      change: The change we are commenting on.
      suspects: List of suspected changes.
      messages: List of messages should appear in the failure message.
      sanity: Bool indicating sanity of build, default: True.
      infra_fail: True if build failed due to infrastructure issues.
      lab_fail: True if build failed due to lab infrastructure issues.
      no_stat: List of builders that did not start.
    """
    msg = validation_pool.ValidationPool._CreateValidationFailureMessage(
        False, change, set(suspects), [], sanity=sanity,
        infra_fail=infra_fail, lab_fail=lab_fail, no_stat=no_stat)
    for x in messages:
      self.assertTrue(x in msg)
    return msg

  def testSuspectChange(self):
    """Test case where 1 is the only change and is suspect."""
    patch = self.GetPatches(1)
    self._AssertMessage(patch, [patch], ['probably caused by your change'])

  def testInnocentChange(self):
    """Test case where 1 is innocent."""
    patch1, patch2 = self.GetPatches(2)
    self._AssertMessage(patch1, [patch2],
                        ['This failure was probably caused by',
                         'retry your change automatically'])

  def testSuspectChanges(self):
    """Test case where 1 is suspected, but so is 2."""
    patches = self.GetPatches(2)
    self._AssertMessage(patches[0], patches,
                        ['may have caused this failure'])

  def testInnocentChangeWithMultipleSuspects(self):
    """Test case where 2 and 3 are suspected."""
    patches = self.GetPatches(3)
    self._AssertMessage(patches[0], patches[1:],
                        ['One of the following changes is probably'])

  def testNoMessages(self):
    """Test case where there are no messages."""
    patch1 = self.GetPatches(1)
    self._AssertMessage(patch1, [patch1], [])

  def testInsaneBuild(self):
    """Test case where the build was not sane."""
    patches = self.GetPatches(3)
    self._AssertMessage(
        patches[0], patches, ['The build was consider not sane',
                              'retry your change automatically'],
        sanity=False)

  def testLabFailMessage(self):
    """Test case where the build failed due to lab failures."""
    patches = self.GetPatches(3)
    self._AssertMessage(
        patches[0], patches, ['Lab infrastructure',
                              'retry your change automatically'],
        lab_fail=True)

  def testInfraFailMessage(self):
    """Test case where the build failed due to infrastructure failures."""
    patches = self.GetPatches(2)
    self._AssertMessage(
        patches[0], [patches[0]],
        ['may have been caused by infrastructure',
         'This failure was probably caused by your change'],
        infra_fail=True)
    self._AssertMessage(
        patches[1], [patches[0]], ['may have been caused by infrastructure',
                                   'retry your change automatically'],
        infra_fail=True)


class TestCreateDisjointTransactions(MoxBase):
  """Test the CreateDisjointTransactions function."""

  def setUp(self):
    self.patch_mock = self.StartPatcher(MockPatchSeries())

  def GetPatches(self, how_many, **kwargs):
    return super(TestCreateDisjointTransactions, self).GetPatches(
        how_many, always_use_list=True, **kwargs)

  def verifyTransactions(self, txns, max_txn_length=None, circular=False):
    """Verify the specified list of transactions are processed correctly.

    Args:
      txns: List of transactions to process.
      max_txn_length: Maximum length of any given transaction. This is passed
        to the CreateDisjointTransactions function.
      circular: Whether the transactions contain circular dependencies.
    """
    remove = self.PatchObject(gerrit.GerritHelper, 'RemoveReady')
    patches = list(itertools.chain.from_iterable(txns))
    expected_plans = txns
    if max_txn_length is not None:
      # When max_txn_length is specified, transactions should be truncated to
      # the specified length, ignoring any remaining patches.
      expected_plans = [txn[:max_txn_length] for txn in txns]

    pool = MakePool(changes=patches)
    plans = pool.CreateDisjointTransactions(None, pool.changes,
                                            max_txn_length=max_txn_length)

    # If the dependencies are circular, the order of the patches is not
    # guaranteed, so compare them in sorted order.
    if circular:
      plans = [sorted(plan) for plan in plans]
      expected_plans = [sorted(plan) for plan in expected_plans]

    # Verify the plans match, and that no changes were rejected.
    self.assertEqual(set(map(str, plans)), set(map(str, expected_plans)))
    self.assertEqual(0, remove.call_count)

  def testPlans(self, max_txn_length=None):
    """Verify that independent sets are distinguished."""
    for num in range(0, 5):
      txns = [self.GetPatches(num) for _ in range(0, num)]
      self.verifyTransactions(txns, max_txn_length=max_txn_length)

  def runUnresolvedPlan(self, changes, max_txn_length=None):
    """Helper for testing unresolved plans."""
    notify = self.PatchObject(validation_pool.ValidationPool,
                              'SendNotification')
    remove = self.PatchObject(gerrit.GerritHelper, 'RemoveReady')
    pool = MakePool(changes=changes)
    plans = pool.CreateDisjointTransactions(None, changes,
                                            max_txn_length=max_txn_length)
    self.assertEqual(plans, [])
    self.assertEqual(remove.call_count, notify.call_count)
    return remove.call_count

  def testUnresolvedPlan(self):
    """Test plan with old approval_timestamp."""
    changes = self.GetPatches(5)[1:]
    with cros_test_lib.LoggingCapturer():
      call_count = self.runUnresolvedPlan(changes)
    self.assertEqual(4, call_count)

  def testRecentUnresolvedPlan(self):
    """Test plan with recent approval_timestamp."""
    changes = self.GetPatches(5)[1:]
    for change in changes:
      change.approval_timestamp = time.time()
    with cros_test_lib.LoggingCapturer():
      call_count = self.runUnresolvedPlan(changes)
    self.assertEqual(0, call_count)

  def testTruncatedPlan(self):
    """Test that plans can be truncated correctly."""
    # Long lists of patches should be truncated, and we should not see any
    # errors when this happens.
    self.testPlans(max_txn_length=3)

  def testCircularPlans(self):
    """Verify that circular plans are handled correctly."""
    patches = self.GetPatches(5)
    self.patch_mock.SetGerritDependencies(patches[0], [patches[-1]])

    # Verify that all patches can be submitted normally.
    self.verifyTransactions([patches], circular=True)

    # It is not possible to truncate a circular plan. Verify that an error
    # is reported in this case.
    with cros_test_lib.LoggingCapturer():
      call_count = self.runUnresolvedPlan(patches, max_txn_length=3)
    self.assertEqual(5, call_count)


class MockValidationPool(partial_mock.PartialMock):
  """Mock out a ValidationPool instance."""

  TARGET = 'chromite.cbuildbot.validation_pool.ValidationPool'
  ATTRS = ('ReloadChanges', 'RemoveReady', '_SubmitChange', 'SendNotification')

  def __init__(self, manager):
    partial_mock.PartialMock.__init__(self)
    self.submit_results = {}
    self.max_submits = manager.Value('i', -1)
    self.submitted = manager.list()
    self.notification_calls = manager.list()

  def GetSubmittedChanges(self):
    return list(self.submitted)

  def _SubmitChange(self, _inst, change):
    result = self.submit_results.get(change, True)
    self.submitted.append(change)
    if isinstance(result, Exception):
      raise result
    if result and self.max_submits.value != -1:
      if self.max_submits.value <= 0:
        return False
      self.max_submits.value -= 1
    return result

  def SendNotification(self, *args, **kwargs):
    self.notification_calls.append((args, kwargs))

  @classmethod
  def ReloadChanges(cls, changes):
    return changes

  RemoveReady = None


class BaseSubmitPoolTestCase(MoxBase):
  """Test full ability to submit and reject CL pools."""

  # Whether all slave builds passed. This would affect the submission
  # logic.
  ALL_BUILDS_PASSED = True

  def setUp(self):
    self.pool_mock = self.StartPatcher(MockValidationPool(self.manager))
    self.patch_mock = self.StartPatcher(MockPatchSeries())
    self.PatchObject(gerrit.GerritHelper, 'QuerySingleRecord')
    self.patches = self.GetPatches(2)

  def SetUpPatchPool(self, failed_to_apply=False):
    pool = MakePool(changes=self.patches, dryrun=False)
    if failed_to_apply:
      # Create some phony errors and add them to the pool.
      errors = []
      for patch in self.GetPatches(2):
        errors.append(validation_pool.InternalCQError(patch, str('foo')))
      pool.changes_that_failed_to_apply_earlier = errors[:]
    return pool

  def SubmitPool(self, submitted=(), rejected=(), **kwargs):
    """Helper function for testing that we can submit a pool successfully.

    Args:
      submitted: List of changes that we expect to be submitted.
      rejected: List of changes that we expect to be rejected.
      **kwargs: Keyword arguments for SetUpPatchPool.
    """
    # Set up our pool and submit the patches.
    pool = self.SetUpPatchPool(**kwargs)
    if not self.ALL_BUILDS_PASSED:
      actually_rejected = sorted(pool.SubmitPartialPool(
          pool.changes, mock.ANY, dict(), [], [], []))
    else:
      _, actually_rejected = pool.SubmitChanges(self.patches)

    # Check that the right patches were submitted and rejected.
    self.assertItemsEqual(list(rejected), list(actually_rejected))
    actually_submitted = self.pool_mock.GetSubmittedChanges()
    self.assertEqual(list(submitted), actually_submitted)

  def GetNotifyArg(self, change, key):
    """Look up a call to notify about |change| and grab |key| from it.

    Args:
      change: The change to look up.
      key: The key to look up. If this is an integer, look up a positional
        argument by index. Otherwise, look up a keyword argument.
    """
    names = []
    for call in self.pool_mock.notification_calls:
      call_args, call_kwargs = call
      if change == call_args[1]:
        if isinstance(key, int):
          return call_args[key]
        return call_kwargs[key]
      names.append(call_args[1])

    # Verify that |change| is present at all. This should always fail.
    self.assertIn(change, names)

  def assertEqualNotifyArg(self, value, change, idx):
    """Verify that |value| equals self.GetNotifyArg(|change|, |idx|)."""
    self.assertEqual(str(value), str(self.GetNotifyArg(change, idx)))


class SubmitPoolTest(BaseSubmitPoolTestCase):
  """Test suite related to the Submit Pool."""

  def testSubmitPool(self):
    """Test that we can submit a pool successfully."""
    self.SubmitPool(submitted=self.patches)

  def testRejectCLs(self):
    """Test that we can reject a CL successfully."""
    self.SubmitPool(submitted=self.patches, failed_to_apply=True)

  def testSubmitCycle(self):
    """Submit a cyclic set of dependencies"""
    self.patch_mock.SetCQDependencies(self.patches[0], [self.patches[1]])
    self.SubmitPool(submitted=self.patches)

  def testSubmitReverseCycle(self):
    """Submit a cyclic set of dependencies, specified in reverse order."""
    self.patch_mock.SetCQDependencies(self.patches[1], [self.patches[0]])
    self.patch_mock.SetGerritDependencies(self.patches[1], [])
    self.patch_mock.SetGerritDependencies(self.patches[0], [self.patches[1]])
    self.SubmitPool(submitted=self.patches[::-1])

  def testRedundantCQDepend(self):
    """Submit a cycle with redundant CQ-DEPEND specifications."""
    self.patches = self.GetPatches(4)
    self.patch_mock.SetCQDependencies(self.patches[0], [self.patches[-1]])
    self.patch_mock.SetCQDependencies(self.patches[1], [self.patches[-1]])
    self.SubmitPool(submitted=self.patches)

  def testSubmitPartialCycle(self):
    """Submit a failed cyclic set of dependencies"""
    self.pool_mock.max_submits.value = 1
    self.patch_mock.SetCQDependencies(self.patches[0], [self.patches[1]])
    self.SubmitPool(submitted=self.patches, rejected=[self.patches[1]])
    (submitted, rejected) = self.pool_mock.GetSubmittedChanges()
    failed_submit = validation_pool.PatchFailedToSubmit(
        rejected, validation_pool.ValidationPool.INCONSISTENT_SUBMIT_MSG)
    bad_submit = validation_pool.PatchSubmittedWithoutDeps(
        submitted, failed_submit)
    self.assertEqualNotifyArg(failed_submit, rejected, 'error')
    self.assertEqualNotifyArg(bad_submit, submitted, 'failure')

  def testSubmitFailedCycle(self):
    """Submit a failed cyclic set of dependencies"""
    self.pool_mock.max_submits.value = 0
    self.patch_mock.SetCQDependencies(self.patches[0], [self.patches[1]])
    self.SubmitPool(submitted=[self.patches[0]], rejected=self.patches)
    (attempted,) = self.pool_mock.GetSubmittedChanges()
    (rejected,) = [x for x in self.patches if x.id != attempted.id]
    failed_submit = validation_pool.PatchFailedToSubmit(
        attempted, validation_pool.ValidationPool.INCONSISTENT_SUBMIT_MSG)
    dep_failed = cros_patch.DependencyError(rejected, failed_submit)
    self.assertEqualNotifyArg(failed_submit, attempted, 'error')
    self.assertEqualNotifyArg(dep_failed, rejected, 'error')

  def testConflict(self):
    """Submit a change that conflicts with TOT."""
    error = gob_util.GOBError(httplib.CONFLICT, 'Conflict')
    self.pool_mock.submit_results[self.patches[0]] = error
    self.SubmitPool(submitted=[self.patches[0]], rejected=self.patches[::-1])
    notify_error = validation_pool.PatchConflict(self.patches[0])
    self.assertEqualNotifyArg(notify_error, self.patches[0], 'error')

  def testServerError(self):
    """Test case where GOB returns a server error."""
    error = gerrit.GerritException('Internal server error')
    self.pool_mock.submit_results[self.patches[0]] = error
    self.SubmitPool(submitted=[self.patches[0]], rejected=self.patches[::-1])
    notify_error = validation_pool.PatchFailedToSubmit(self.patches[0], error)
    self.assertEqualNotifyArg(notify_error, self.patches[0], 'error')

  def testNotCommitReady(self):
    """Test that a CL is rejected if its approvals were pulled."""
    def _ReloadPatches(patches):
      reloaded = copy.deepcopy(patches)
      self.PatchObject(reloaded[1], 'HasApproval', return_value=False)
      return reloaded
    self.PatchObject(validation_pool.ValidationPool, 'ReloadChanges',
                     side_effect=_ReloadPatches)
    self.SubmitPool(submitted=self.patches[:1], rejected=self.patches[1:])
    error = validation_pool.PatchNotCommitReady(self.patches[1])
    self.assertEqualNotifyArg(error, self.patches[1], 'error')

  def testAlreadyMerged(self):
    """Test that a CL that was chumped during the run was not rejected."""
    self.PatchObject(self.patches[0], 'IsAlreadyMerged', return_value=True)
    self.SubmitPool(submitted=self.patches[1:], rejected=[])

  def testModified(self):
    """Test that a CL that was modified during the run is rejected."""
    def _ReloadPatches(patches):
      reloaded = copy.deepcopy(patches)
      reloaded[1].patch_number += 1
      return reloaded
    self.PatchObject(validation_pool.ValidationPool, 'ReloadChanges',
                     side_effect=_ReloadPatches)
    self.SubmitPool(submitted=self.patches[:1], rejected=self.patches[1:])
    error = validation_pool.PatchModified(self.patches[1])
    self.assertEqualNotifyArg(error, self.patches[1], 'error')


class SubmitPartialPoolTest(BaseSubmitPoolTestCase):
  """Test the SubmitPartialPool function."""

  # Whether all slave builds passed. This would affect the submission
  # logic.
  ALL_BUILDS_PASSED = False

  def setUp(self):
    # Set up each patch to be in its own project, so that we can easily
    # request to ignore failures for the specified patch.
    for patch in self.patches:
      patch.project = str(patch)

    self.verified_mock = self.PatchObject(
        triage_lib.CalculateSuspects, 'GetFullyVerifiedChanges',
        return_value=[])
    self.PatchObject(validation_pool.ValidationPool, '_GetShouldSubmitChanges')

  def _MarkPatchesVerified(self, patches):
    """Set up to mark |patches| as verified."""
    self.verified_mock.return_value = patches

  def testSubmitNone(self):
    """Submit no changes."""
    self.SubmitPool(submitted=(), rejected=self.patches)

  def testSubmitAll(self):
    """Submit all changes."""
    self._MarkPatchesVerified(self.patches[:2])
    self.SubmitPool(submitted=self.patches, rejected=[])

  def testSubmitFirst(self):
    """Submit the first change in a series."""
    self._MarkPatchesVerified([self.patches[0]])
    self.SubmitPool(submitted=[self.patches[0]], rejected=[self.patches[1]])
    self.assertEqual(len(self.pool_mock.notification_calls), 0)

  def testSubmitSecond(self):
    """Attempt to submit the second change in a series."""
    self._MarkPatchesVerified([self.patches[1]])
    self.SubmitPool(submitted=[], rejected=[self.patches[0]])
    error = validation_pool.PatchRejected(self.patches[0])
    dep_error = cros_patch.DependencyError(self.patches[1], error)
    self.assertEqualNotifyArg(dep_error, self.patches[1], 'error')
    self.assertEqual(len(self.pool_mock.notification_calls), 1)


class LoadManifestTest(cros_test_lib.TempDirTestCase):
  """Tests loading the manifest."""

  manifest_content = (
      '<?xml version="1.0" ?><manifest>'
      '<pending_commit branch="master" '
      'change_id="Ieeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee1" '
      'commit="1ddddddddddddddddddddddddddddddddddddddd" '
      'fail_count="2" gerrit_number="17000" owner_email="foo@chromium.org" '
      'pass_count="0" patch_number="2" project="chromiumos/taco/bar" '
      'project_url="https://base_url/chromiumos/taco/bar" '
      'ref="refs/changes/51/17000/2" remote="cros" total_fail_count="3"/>'
      '</manifest>')

  def setUp(self):
    """Sets up a pool."""
    self.pool = MakePool()

  def testAddPendingCommitsIntoPool(self):
    """Test reading the pending commits and add them into the pool."""
    with tempfile.NamedTemporaryFile() as f:
      f.write(self.manifest_content)
      f.flush()
      self.pool.AddPendingCommitsIntoPool(f.name)

    self.assertEqual(self.pool.changes[0].owner_email, 'foo@chromium.org')
    self.assertEqual(self.pool.changes[0].tracking_branch, 'master')
    self.assertEqual(self.pool.changes[0].remote, 'cros')
    self.assertEqual(self.pool.changes[0].gerrit_number, '17000')
    self.assertEqual(self.pool.changes[0].project, 'chromiumos/taco/bar')
    self.assertEqual(self.pool.changes[0].project_url,
                     'https://base_url/chromiumos/taco/bar')
    self.assertEqual(self.pool.changes[0].change_id,
                     'Ieeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee1')
    self.assertEqual(self.pool.changes[0].commit,
                     '1ddddddddddddddddddddddddddddddddddddddd')
    self.assertEqual(self.pool.changes[0].fail_count, 2)
    self.assertEqual(self.pool.changes[0].pass_count, 0)
    self.assertEqual(self.pool.changes[0].total_fail_count, 3)


if __name__ == '__main__':
  cros_test_lib.main()
