# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Controller for the build_annotations app.

This controller sits between the django models for cidb tables and the views
that power the app.
Keep non-trivial logic to aggregate data / optimize db access here and test it.
"""

from __future__ import print_function

import collections

from django.db import models
from django.db.models import query

from build_annotations import models as ba_models


class BuildRow(collections.MutableMapping):
  """A database "view" that collects all relevant stats about a build."""

  def __init__(self, build_entry, build_stage_entries,
               cl_action_entries, failure_entries, annotations):
    """Initialize a BuildRow.

    Do not use QuerySets as arguments. All query sets must have been evaluated
    before creating this object. All data manipulation within this object is
    pure python.

    All non-trivial computation on this object should be lazy: Defer it to
    property getters.
    """
    assert not isinstance(build_entry, query.QuerySet)
    assert not isinstance(build_stage_entries, query.QuerySet)
    assert not isinstance(cl_action_entries, query.QuerySet)
    assert not isinstance(failure_entries, query.QuerySet)

    self._data = {}

    self.build_entry = build_entry
    self._build_stage_entries = build_stage_entries
    self._cl_action_entries = cl_action_entries
    self._failure_entries = failure_entries

    # The readonly data is accessible from this object as dict entries.
    self['id'] = self.build_entry.id
    self['build_number'] = self.build_entry.build_number
    self['status'] = self.build_entry.status
    self['summary'] = self.build_entry.summary
    self['start_time'] = self.build_entry.start_time
    if (self.build_entry.finish_time is not None and
        self['start_time'] is not None):
      self['run_time'] = self.build_entry.finish_time - self['start_time']
    else:
      self['run_time'] = None
    if self['start_time'] is not None:
      self['weekday'] = (self['start_time'].date().weekday() != 6)
    else:
      self['weekday'] = None
    self['chromeos_version'] = self.build_entry.full_version
    self['chrome_version'] = self.build_entry.chrome_version
    self['waterfall'] = self.build_entry.waterfall
    self['builder_name'] = self.build_entry.builder_name

    failed_stages = [x.name for x in build_stage_entries if
                     x.status == x.FAIL]
    self['failed_stages'] = ', '.join(failed_stages)
    self['picked_up_count'] = self._CountCLActions(
        ba_models.ClActionTable.PICKED_UP)
    self['submitted_count'] = self._CountCLActions(
        ba_models.ClActionTable.SUBMITTED)
    self['kicked_out_count'] = self._CountCLActions(
        ba_models.ClActionTable.KICKED_OUT)

    # Annotations are treated specially. They are not availabe via the dict API.
    self.annotations = annotations
    self['annotation_summary'] = self._SummaryAnnotations()

  def __getitem__(self, *args, **kwargs):
    return self._data.__getitem__(*args, **kwargs)

  def __iter__(self, *args, **kwargs):
    return self._data.__iter__(*args, **kwargs)

  def __len__(self, *args, **kwargs):
    return self._data.__len__(*args, **kwargs)

  def __setitem__(self, *args, **kwargs):
    return self._data.__setitem__(*args, **kwargs)

  def __delitem__(self, *args, **kwargs):
    return self._data.__delitem__(*args, **kwargs)

  def _CountCLActions(self, cl_action):
    actions = [x for x in self._cl_action_entries if x.action == cl_action]
    return len(actions)

  def _SummaryAnnotations(self):
    if not self.annotations:
      return ''

    result = '%d annotations: ' % len(self.annotations)
    summaries = []
    for annotation in self.annotations:
      summary = annotation.failure_category
      failure_message = annotation.failure_message
      blame_url = annotation.blame_url
      if failure_message:
        summary += '(%s)' % failure_message[:30]
      elif blame_url:
        summary += '(%s)' % blame_url[:30]
      summaries.append(summary)

    result += '; '.join(summaries)
    return result


class BuildRowController(object):
  """The 'controller' class that collates stats for builds.

  More details here.
  Unit-test this class please.
  """

  DEFAULT_NUM_BUILDS = 100

  def __init__(self):
    self._latest_build_id = 0
    self._build_rows_map = {}


  def GetStructuredBuilds(self, latest_build_id=None,
                          num_builds=DEFAULT_NUM_BUILDS, extra_filter_q=None):
    """The primary method to obtain stats for builds

    Args:
      latest_build_id: build_id of the latest build to query.
      num_builds: Number of build to query.
      extra_filter_q: An optional Q object to filter builds. Use GetQ* methods
          provided in this class to form the filter.

    Returns:
      A list of BuildRow entries for the queried builds.
    """
    # If we're not given any latest_build_id, we fetch the latest builds
    if latest_build_id is not None:
      build_qs = ba_models.BuildTable.objects.filter(id__lte=latest_build_id)
    else:
      build_qs = ba_models.BuildTable.objects.all()

    if extra_filter_q is not None:
      build_qs = build_qs.filter(extra_filter_q)
    build_qs = build_qs.order_by('-id')
    build_qs = build_qs[:num_builds]

    # Critical for performance: Prefetch all the join relations we'll need.
    build_qs = build_qs.prefetch_related('buildstagetable_set')
    build_qs = build_qs.prefetch_related('clactiontable_set')
    build_qs = build_qs.prefetch_related(
        'buildstagetable_set__failuretable_set')
    build_qs = build_qs.prefetch_related('annotationstable_set')

    # Now hit the database.
    build_entries = [x for x in build_qs]

    self._build_rows_map = {}
    build_rows = []
    for build_entry in build_entries:
      build_stage_entries = [x for x in build_entry.buildstagetable_set.all()]
      cl_action_entries = [x for x in build_entry.clactiontable_set.all()]
      failure_entries = []
      for entry in build_stage_entries:
        failure_entries += [x for x in entry.failuretable_set.all()]
      # Filter in python, filter'ing the queryset changes the queryset, and we
      # end up hitting the database again.
      annotations = [a for a in build_entry.annotationstable_set.all() if
                     a.deleted == False]

      build_row = BuildRow(build_entry, build_stage_entries, cl_action_entries,
                           failure_entries, annotations)

      self._build_rows_map[build_entry.id] = build_row
      build_rows.append(build_row)

    if build_entries:
      self._latest_build_id = build_entries[0].id

    return build_rows

  ############################################################################
  # GetQ* methods are intended to be used in nifty search expressions to search
  # for builds.
  @classmethod
  def GetQNoAnnotations(cls):
    """Return a Q for builds with no annotations yet."""
    return models.Q(annotationstable__isnull=True)

  @classmethod
  def GetQRestrictToBuildConfig(cls, build_config):
    """Return a Q for builds with the given build_config."""
    return models.Q(build_config=build_config)

  @property
  def num_builds(self):
    return len(self._build_rows_map)

  @property
  def latest_build_id(self):
    return self._latest_build_id
