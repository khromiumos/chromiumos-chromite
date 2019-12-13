# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/phosphorus/prejob.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.test_platform.phosphorus import common_pb2 as test__platform_dot_phosphorus_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/phosphorus/prejob.proto',
  package='test_platform.phosphorus',
  syntax='proto3',
  serialized_options=_b('ZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorus'),
  serialized_pb=_b('\n%test_platform/phosphorus/prejob.proto\x12\x18test_platform.phosphorus\x1a%test_platform/phosphorus/common.proto\"\xde\x04\n\rPrejobRequest\x12\x30\n\x06\x63onfig\x18\x01 \x01(\x0b\x32 .test_platform.phosphorus.Config\x12\x14\n\x0c\x64ut_hostname\x18\x02 \x01(\t\x12\x62\n\x14provisionable_labels\x18\x03 \x03(\x0b\x32@.test_platform.phosphorus.PrejobRequest.ProvisionableLabelsEntryB\x02\x18\x01\x12m\n\x1c\x64\x65sired_provisionable_labels\x18\x04 \x03(\x0b\x32G.test_platform.phosphorus.PrejobRequest.DesiredProvisionableLabelsEntry\x12o\n\x1d\x65xisting_provisionable_labels\x18\x05 \x03(\x0b\x32H.test_platform.phosphorus.PrejobRequest.ExistingProvisionableLabelsEntry\x1a:\n\x18ProvisionableLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x41\n\x1f\x44\x65siredProvisionableLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x42\n ExistingProvisionableLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x44ZBgo.chromium.org/chromiumos/infra/proto/go/test_platform/phosphorusb\x06proto3')
  ,
  dependencies=[test__platform_dot_phosphorus_dot_common__pb2.DESCRIPTOR,])




_PREJOBREQUEST_PROVISIONABLELABELSENTRY = _descriptor.Descriptor(
  name='ProvisionableLabelsEntry',
  full_name='test_platform.phosphorus.PrejobRequest.ProvisionableLabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='test_platform.phosphorus.PrejobRequest.ProvisionableLabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.phosphorus.PrejobRequest.ProvisionableLabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=520,
  serialized_end=578,
)

_PREJOBREQUEST_DESIREDPROVISIONABLELABELSENTRY = _descriptor.Descriptor(
  name='DesiredProvisionableLabelsEntry',
  full_name='test_platform.phosphorus.PrejobRequest.DesiredProvisionableLabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='test_platform.phosphorus.PrejobRequest.DesiredProvisionableLabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.phosphorus.PrejobRequest.DesiredProvisionableLabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=580,
  serialized_end=645,
)

_PREJOBREQUEST_EXISTINGPROVISIONABLELABELSENTRY = _descriptor.Descriptor(
  name='ExistingProvisionableLabelsEntry',
  full_name='test_platform.phosphorus.PrejobRequest.ExistingProvisionableLabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='test_platform.phosphorus.PrejobRequest.ExistingProvisionableLabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='test_platform.phosphorus.PrejobRequest.ExistingProvisionableLabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=647,
  serialized_end=713,
)

_PREJOBREQUEST = _descriptor.Descriptor(
  name='PrejobRequest',
  full_name='test_platform.phosphorus.PrejobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='test_platform.phosphorus.PrejobRequest.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dut_hostname', full_name='test_platform.phosphorus.PrejobRequest.dut_hostname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='provisionable_labels', full_name='test_platform.phosphorus.PrejobRequest.provisionable_labels', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='desired_provisionable_labels', full_name='test_platform.phosphorus.PrejobRequest.desired_provisionable_labels', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='existing_provisionable_labels', full_name='test_platform.phosphorus.PrejobRequest.existing_provisionable_labels', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PREJOBREQUEST_PROVISIONABLELABELSENTRY, _PREJOBREQUEST_DESIREDPROVISIONABLELABELSENTRY, _PREJOBREQUEST_EXISTINGPROVISIONABLELABELSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=713,
)

_PREJOBREQUEST_PROVISIONABLELABELSENTRY.containing_type = _PREJOBREQUEST
_PREJOBREQUEST_DESIREDPROVISIONABLELABELSENTRY.containing_type = _PREJOBREQUEST
_PREJOBREQUEST_EXISTINGPROVISIONABLELABELSENTRY.containing_type = _PREJOBREQUEST
_PREJOBREQUEST.fields_by_name['config'].message_type = test__platform_dot_phosphorus_dot_common__pb2._CONFIG
_PREJOBREQUEST.fields_by_name['provisionable_labels'].message_type = _PREJOBREQUEST_PROVISIONABLELABELSENTRY
_PREJOBREQUEST.fields_by_name['desired_provisionable_labels'].message_type = _PREJOBREQUEST_DESIREDPROVISIONABLELABELSENTRY
_PREJOBREQUEST.fields_by_name['existing_provisionable_labels'].message_type = _PREJOBREQUEST_EXISTINGPROVISIONABLELABELSENTRY
DESCRIPTOR.message_types_by_name['PrejobRequest'] = _PREJOBREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PrejobRequest = _reflection.GeneratedProtocolMessageType('PrejobRequest', (_message.Message,), dict(

  ProvisionableLabelsEntry = _reflection.GeneratedProtocolMessageType('ProvisionableLabelsEntry', (_message.Message,), dict(
    DESCRIPTOR = _PREJOBREQUEST_PROVISIONABLELABELSENTRY,
    __module__ = 'test_platform.phosphorus.prejob_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.phosphorus.PrejobRequest.ProvisionableLabelsEntry)
    ))
  ,

  DesiredProvisionableLabelsEntry = _reflection.GeneratedProtocolMessageType('DesiredProvisionableLabelsEntry', (_message.Message,), dict(
    DESCRIPTOR = _PREJOBREQUEST_DESIREDPROVISIONABLELABELSENTRY,
    __module__ = 'test_platform.phosphorus.prejob_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.phosphorus.PrejobRequest.DesiredProvisionableLabelsEntry)
    ))
  ,

  ExistingProvisionableLabelsEntry = _reflection.GeneratedProtocolMessageType('ExistingProvisionableLabelsEntry', (_message.Message,), dict(
    DESCRIPTOR = _PREJOBREQUEST_EXISTINGPROVISIONABLELABELSENTRY,
    __module__ = 'test_platform.phosphorus.prejob_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.phosphorus.PrejobRequest.ExistingProvisionableLabelsEntry)
    ))
  ,
  DESCRIPTOR = _PREJOBREQUEST,
  __module__ = 'test_platform.phosphorus.prejob_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.phosphorus.PrejobRequest)
  ))
_sym_db.RegisterMessage(PrejobRequest)
_sym_db.RegisterMessage(PrejobRequest.ProvisionableLabelsEntry)
_sym_db.RegisterMessage(PrejobRequest.DesiredProvisionableLabelsEntry)
_sym_db.RegisterMessage(PrejobRequest.ExistingProvisionableLabelsEntry)


DESCRIPTOR._options = None
_PREJOBREQUEST_PROVISIONABLELABELSENTRY._options = None
_PREJOBREQUEST_DESIREDPROVISIONABLELABELSENTRY._options = None
_PREJOBREQUEST_EXISTINGPROVISIONABLELABELSENTRY._options = None
_PREJOBREQUEST.fields_by_name['provisionable_labels']._options = None
# @@protoc_insertion_point(module_scope)