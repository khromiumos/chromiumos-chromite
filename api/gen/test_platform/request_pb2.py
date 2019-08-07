# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/request.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/request.proto',
  package='test_platform',
  syntax='proto3',
  serialized_options=_b('Z7go.chromium.org/chromiumos/infra/proto/go/test_platform'),
  serialized_pb=_b('\n\x1btest_platform/request.proto\x12\rtest_platform\x1a\x17\x63hromiumos/common.proto\x1a\x1egoogle/protobuf/duration.proto\"\xcc\x0c\n\x07Request\x12-\n\x06params\x18\x01 \x01(\x0b\x32\x1d.test_platform.Request.Params\x12\x32\n\ttest_plan\x18\x05 \x01(\x0b\x32\x1f.test_platform.Request.TestPlan\x1a\x9b\t\n\x06Params\x12M\n\x13hardware_attributes\x18\x01 \x01(\x0b\x32\x30.test_platform.Request.Params.HardwareAttributes\x12M\n\x13software_attributes\x18\x02 \x01(\x0b\x32\x30.test_platform.Request.Params.SoftwareAttributes\x12O\n\x15software_dependencies\x18\x03 \x03(\x0b\x32\x30.test_platform.Request.Params.SoftwareDependency\x12<\n\nscheduling\x18\x04 \x01(\x0b\x32(.test_platform.Request.Params.Scheduling\x12\x32\n\x05retry\x18\x05 \x01(\x0b\x32#.test_platform.Request.Params.Retry\x12\x38\n\x08metadata\x18\x06 \x01(\x0b\x32&.test_platform.Request.Params.Metadata\x12\x30\n\x04time\x18\x07 \x01(\x0b\x32\".test_platform.Request.Params.Time\x1a#\n\x12HardwareAttributes\x12\r\n\x05model\x18\x01 \x01(\t\x1aP\n\x12SoftwareAttributes\x12-\n\x0c\x62uild_target\x18\x02 \x01(\x0b\x32\x17.chromiumos.BuildTargetJ\x04\x08\x01\x10\x02R\x05\x62oard\x1aL\n\x12SoftwareDependency\x12\x18\n\x0e\x63hromeos_build\x18\x03 \x01(\tH\x00\x42\x05\n\x03\x64\x65pJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03R\x04typeR\x03url\x1a\x91\x03\n\nScheduling\x12L\n\x0cmanaged_pool\x18\x01 \x01(\x0e\x32\x34.test_platform.Request.Params.Scheduling.ManagedPoolH\x00\x12\x18\n\x0eunmanaged_pool\x18\x02 \x01(\tH\x00\x12\x17\n\rquota_account\x18\x03 \x01(\tH\x00\"\xf9\x01\n\x0bManagedPool\x12\x1c\n\x18MANAGED_POOL_UNSPECIFIED\x10\x00\x12\x13\n\x0fMANAGED_POOL_CQ\x10\x01\x12\x14\n\x10MANAGED_POOL_BVT\x10\x02\x12\x17\n\x13MANAGED_POOL_SUITES\x10\x03\x12\x14\n\x10MANAGED_POOL_CTS\x10\x04\x12\x1d\n\x19MANAGED_POOL_CTS_PERBUILD\x10\x05\x12\x1b\n\x17MANAGED_POOL_CONTINUOUS\x10\x06\x12\x1e\n\x1aMANAGED_POOL_ARC_PRESUBMIT\x10\x07\x12\x16\n\x12MANAGED_POOL_QUOTA\x10\x08\x42\x06\n\x04pool\x1a\x07\n\x05Retry\x1a%\n\x08Metadata\x12\x19\n\x11test_metadata_url\x18\x01 \x01(\t\x1a;\n\x04Time\x12\x33\n\x10maximum_duration\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration\x1a\x15\n\x05Suite\x12\x0c\n\x04name\x18\x01 \x01(\t\x1a\x97\x01\n\x04Test\x12\x34\n\x07harness\x18\x01 \x01(\x0e\x32#.test_platform.Request.Test.Harness\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\ttest_args\x18\x03 \x03(\t\"8\n\x07Harness\x12\x17\n\x13HARNESS_UNSPECIFIED\x10\x00\x12\x14\n\x10HARNESS_AUTOTEST\x10\x01\x1a\x62\n\x08TestPlan\x12+\n\x05suite\x18\x01 \x03(\x0b\x32\x1c.test_platform.Request.Suite\x12)\n\x04test\x18\x02 \x03(\x0b\x32\x1b.test_platform.Request.TestJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05R\x06suitesR\x05testsR\ntest_plansB9Z7go.chromium.org/chromiumos/infra/proto/go/test_platformb\x06proto3')
  ,
  dependencies=[chromiumos_dot_common__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,])



_REQUEST_PARAMS_SCHEDULING_MANAGEDPOOL = _descriptor.EnumDescriptor(
  name='ManagedPool',
  full_name='test_platform.Request.Params.Scheduling.ManagedPool',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_CQ', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_BVT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_SUITES', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_CTS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_CTS_PERBUILD', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_CONTINUOUS', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_ARC_PRESUBMIT', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGED_POOL_QUOTA', index=8, number=8,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1028,
  serialized_end=1277,
)
_sym_db.RegisterEnumDescriptor(_REQUEST_PARAMS_SCHEDULING_MANAGEDPOOL)

_REQUEST_TEST_HARNESS = _descriptor.EnumDescriptor(
  name='Harness',
  full_name='test_platform.Request.Test.Harness',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HARNESS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARNESS_AUTOTEST', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1515,
  serialized_end=1571,
)
_sym_db.RegisterEnumDescriptor(_REQUEST_TEST_HARNESS)


_REQUEST_PARAMS_HARDWAREATTRIBUTES = _descriptor.Descriptor(
  name='HardwareAttributes',
  full_name='test_platform.Request.Params.HardwareAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='test_platform.Request.Params.HardwareAttributes.model', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=686,
  serialized_end=721,
)

_REQUEST_PARAMS_SOFTWAREATTRIBUTES = _descriptor.Descriptor(
  name='SoftwareAttributes',
  full_name='test_platform.Request.Params.SoftwareAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_target', full_name='test_platform.Request.Params.SoftwareAttributes.build_target', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=723,
  serialized_end=803,
)

_REQUEST_PARAMS_SOFTWAREDEPENDENCY = _descriptor.Descriptor(
  name='SoftwareDependency',
  full_name='test_platform.Request.Params.SoftwareDependency',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chromeos_build', full_name='test_platform.Request.Params.SoftwareDependency.chromeos_build', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='dep', full_name='test_platform.Request.Params.SoftwareDependency.dep',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=805,
  serialized_end=881,
)

_REQUEST_PARAMS_SCHEDULING = _descriptor.Descriptor(
  name='Scheduling',
  full_name='test_platform.Request.Params.Scheduling',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='managed_pool', full_name='test_platform.Request.Params.Scheduling.managed_pool', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unmanaged_pool', full_name='test_platform.Request.Params.Scheduling.unmanaged_pool', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quota_account', full_name='test_platform.Request.Params.Scheduling.quota_account', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REQUEST_PARAMS_SCHEDULING_MANAGEDPOOL,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='pool', full_name='test_platform.Request.Params.Scheduling.pool',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=884,
  serialized_end=1285,
)

_REQUEST_PARAMS_RETRY = _descriptor.Descriptor(
  name='Retry',
  full_name='test_platform.Request.Params.Retry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1287,
  serialized_end=1294,
)

_REQUEST_PARAMS_METADATA = _descriptor.Descriptor(
  name='Metadata',
  full_name='test_platform.Request.Params.Metadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test_metadata_url', full_name='test_platform.Request.Params.Metadata.test_metadata_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1296,
  serialized_end=1333,
)

_REQUEST_PARAMS_TIME = _descriptor.Descriptor(
  name='Time',
  full_name='test_platform.Request.Params.Time',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='maximum_duration', full_name='test_platform.Request.Params.Time.maximum_duration', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1335,
  serialized_end=1394,
)

_REQUEST_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='test_platform.Request.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hardware_attributes', full_name='test_platform.Request.Params.hardware_attributes', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='software_attributes', full_name='test_platform.Request.Params.software_attributes', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='software_dependencies', full_name='test_platform.Request.Params.software_dependencies', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheduling', full_name='test_platform.Request.Params.scheduling', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='retry', full_name='test_platform.Request.Params.retry', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='test_platform.Request.Params.metadata', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='test_platform.Request.Params.time', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_REQUEST_PARAMS_HARDWAREATTRIBUTES, _REQUEST_PARAMS_SOFTWAREATTRIBUTES, _REQUEST_PARAMS_SOFTWAREDEPENDENCY, _REQUEST_PARAMS_SCHEDULING, _REQUEST_PARAMS_RETRY, _REQUEST_PARAMS_METADATA, _REQUEST_PARAMS_TIME, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=215,
  serialized_end=1394,
)

_REQUEST_SUITE = _descriptor.Descriptor(
  name='Suite',
  full_name='test_platform.Request.Suite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='test_platform.Request.Suite.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1396,
  serialized_end=1417,
)

_REQUEST_TEST = _descriptor.Descriptor(
  name='Test',
  full_name='test_platform.Request.Test',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='harness', full_name='test_platform.Request.Test.harness', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='test_platform.Request.Test.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_args', full_name='test_platform.Request.Test.test_args', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REQUEST_TEST_HARNESS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1420,
  serialized_end=1571,
)

_REQUEST_TESTPLAN = _descriptor.Descriptor(
  name='TestPlan',
  full_name='test_platform.Request.TestPlan',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='suite', full_name='test_platform.Request.TestPlan.suite', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test', full_name='test_platform.Request.TestPlan.test', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1573,
  serialized_end=1671,
)

_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='test_platform.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='params', full_name='test_platform.Request.params', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_plan', full_name='test_platform.Request.test_plan', index=1,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_REQUEST_PARAMS, _REQUEST_SUITE, _REQUEST_TEST, _REQUEST_TESTPLAN, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=104,
  serialized_end=1716,
)

_REQUEST_PARAMS_HARDWAREATTRIBUTES.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS_SOFTWAREATTRIBUTES.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_REQUEST_PARAMS_SOFTWAREATTRIBUTES.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS_SOFTWAREDEPENDENCY.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS_SOFTWAREDEPENDENCY.oneofs_by_name['dep'].fields.append(
  _REQUEST_PARAMS_SOFTWAREDEPENDENCY.fields_by_name['chromeos_build'])
_REQUEST_PARAMS_SOFTWAREDEPENDENCY.fields_by_name['chromeos_build'].containing_oneof = _REQUEST_PARAMS_SOFTWAREDEPENDENCY.oneofs_by_name['dep']
_REQUEST_PARAMS_SCHEDULING.fields_by_name['managed_pool'].enum_type = _REQUEST_PARAMS_SCHEDULING_MANAGEDPOOL
_REQUEST_PARAMS_SCHEDULING.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS_SCHEDULING_MANAGEDPOOL.containing_type = _REQUEST_PARAMS_SCHEDULING
_REQUEST_PARAMS_SCHEDULING.oneofs_by_name['pool'].fields.append(
  _REQUEST_PARAMS_SCHEDULING.fields_by_name['managed_pool'])
_REQUEST_PARAMS_SCHEDULING.fields_by_name['managed_pool'].containing_oneof = _REQUEST_PARAMS_SCHEDULING.oneofs_by_name['pool']
_REQUEST_PARAMS_SCHEDULING.oneofs_by_name['pool'].fields.append(
  _REQUEST_PARAMS_SCHEDULING.fields_by_name['unmanaged_pool'])
_REQUEST_PARAMS_SCHEDULING.fields_by_name['unmanaged_pool'].containing_oneof = _REQUEST_PARAMS_SCHEDULING.oneofs_by_name['pool']
_REQUEST_PARAMS_SCHEDULING.oneofs_by_name['pool'].fields.append(
  _REQUEST_PARAMS_SCHEDULING.fields_by_name['quota_account'])
_REQUEST_PARAMS_SCHEDULING.fields_by_name['quota_account'].containing_oneof = _REQUEST_PARAMS_SCHEDULING.oneofs_by_name['pool']
_REQUEST_PARAMS_RETRY.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS_METADATA.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS_TIME.fields_by_name['maximum_duration'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_REQUEST_PARAMS_TIME.containing_type = _REQUEST_PARAMS
_REQUEST_PARAMS.fields_by_name['hardware_attributes'].message_type = _REQUEST_PARAMS_HARDWAREATTRIBUTES
_REQUEST_PARAMS.fields_by_name['software_attributes'].message_type = _REQUEST_PARAMS_SOFTWAREATTRIBUTES
_REQUEST_PARAMS.fields_by_name['software_dependencies'].message_type = _REQUEST_PARAMS_SOFTWAREDEPENDENCY
_REQUEST_PARAMS.fields_by_name['scheduling'].message_type = _REQUEST_PARAMS_SCHEDULING
_REQUEST_PARAMS.fields_by_name['retry'].message_type = _REQUEST_PARAMS_RETRY
_REQUEST_PARAMS.fields_by_name['metadata'].message_type = _REQUEST_PARAMS_METADATA
_REQUEST_PARAMS.fields_by_name['time'].message_type = _REQUEST_PARAMS_TIME
_REQUEST_PARAMS.containing_type = _REQUEST
_REQUEST_SUITE.containing_type = _REQUEST
_REQUEST_TEST.fields_by_name['harness'].enum_type = _REQUEST_TEST_HARNESS
_REQUEST_TEST.containing_type = _REQUEST
_REQUEST_TEST_HARNESS.containing_type = _REQUEST_TEST
_REQUEST_TESTPLAN.fields_by_name['suite'].message_type = _REQUEST_SUITE
_REQUEST_TESTPLAN.fields_by_name['test'].message_type = _REQUEST_TEST
_REQUEST_TESTPLAN.containing_type = _REQUEST
_REQUEST.fields_by_name['params'].message_type = _REQUEST_PARAMS
_REQUEST.fields_by_name['test_plan'].message_type = _REQUEST_TESTPLAN
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(

  Params = _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), dict(

    HardwareAttributes = _reflection.GeneratedProtocolMessageType('HardwareAttributes', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_HARDWAREATTRIBUTES,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.HardwareAttributes)
      ))
    ,

    SoftwareAttributes = _reflection.GeneratedProtocolMessageType('SoftwareAttributes', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_SOFTWAREATTRIBUTES,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.SoftwareAttributes)
      ))
    ,

    SoftwareDependency = _reflection.GeneratedProtocolMessageType('SoftwareDependency', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_SOFTWAREDEPENDENCY,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.SoftwareDependency)
      ))
    ,

    Scheduling = _reflection.GeneratedProtocolMessageType('Scheduling', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_SCHEDULING,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.Scheduling)
      ))
    ,

    Retry = _reflection.GeneratedProtocolMessageType('Retry', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_RETRY,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.Retry)
      ))
    ,

    Metadata = _reflection.GeneratedProtocolMessageType('Metadata', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_METADATA,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.Metadata)
      ))
    ,

    Time = _reflection.GeneratedProtocolMessageType('Time', (_message.Message,), dict(
      DESCRIPTOR = _REQUEST_PARAMS_TIME,
      __module__ = 'test_platform.request_pb2'
      # @@protoc_insertion_point(class_scope:test_platform.Request.Params.Time)
      ))
    ,
    DESCRIPTOR = _REQUEST_PARAMS,
    __module__ = 'test_platform.request_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.Request.Params)
    ))
  ,

  Suite = _reflection.GeneratedProtocolMessageType('Suite', (_message.Message,), dict(
    DESCRIPTOR = _REQUEST_SUITE,
    __module__ = 'test_platform.request_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.Request.Suite)
    ))
  ,

  Test = _reflection.GeneratedProtocolMessageType('Test', (_message.Message,), dict(
    DESCRIPTOR = _REQUEST_TEST,
    __module__ = 'test_platform.request_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.Request.Test)
    ))
  ,

  TestPlan = _reflection.GeneratedProtocolMessageType('TestPlan', (_message.Message,), dict(
    DESCRIPTOR = _REQUEST_TESTPLAN,
    __module__ = 'test_platform.request_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.Request.TestPlan)
    ))
  ,
  DESCRIPTOR = _REQUEST,
  __module__ = 'test_platform.request_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.Request)
  ))
_sym_db.RegisterMessage(Request)
_sym_db.RegisterMessage(Request.Params)
_sym_db.RegisterMessage(Request.Params.HardwareAttributes)
_sym_db.RegisterMessage(Request.Params.SoftwareAttributes)
_sym_db.RegisterMessage(Request.Params.SoftwareDependency)
_sym_db.RegisterMessage(Request.Params.Scheduling)
_sym_db.RegisterMessage(Request.Params.Retry)
_sym_db.RegisterMessage(Request.Params.Metadata)
_sym_db.RegisterMessage(Request.Params.Time)
_sym_db.RegisterMessage(Request.Suite)
_sym_db.RegisterMessage(Request.Test)
_sym_db.RegisterMessage(Request.TestPlan)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)