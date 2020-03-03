# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: device/config_id.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.device import platform_id_pb2 as device_dot_platform__id__pb2
from chromite.api.gen.device import model_id_pb2 as device_dot_model__id__pb2
from chromite.api.gen.device import brand_id_pb2 as device_dot_brand__id__pb2
from chromite.api.gen.device import variant_id_pb2 as device_dot_variant__id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='device/config_id.proto',
  package='device',
  syntax='proto3',
  serialized_options=_b('Z0go.chromium.org/chromiumos/infra/proto/go/device'),
  serialized_pb=_b('\n\x16\x64\x65vice/config_id.proto\x12\x06\x64\x65vice\x1a\x18\x64\x65vice/platform_id.proto\x1a\x15\x64\x65vice/model_id.proto\x1a\x15\x64\x65vice/brand_id.proto\x1a\x17\x64\x65vice/variant_id.proto\"\xa0\x01\n\x08\x43onfigId\x12\'\n\x0bplatform_id\x18\x01 \x01(\x0b\x32\x12.device.PlatformId\x12!\n\x08model_id\x18\x02 \x01(\x0b\x32\x0f.device.ModelId\x12%\n\nvariant_id\x18\x03 \x01(\x0b\x32\x11.device.VariantId\x12!\n\x08\x62rand_id\x18\x04 \x01(\x0b\x32\x0f.device.BrandIdB2Z0go.chromium.org/chromiumos/infra/proto/go/deviceb\x06proto3')
  ,
  dependencies=[device_dot_platform__id__pb2.DESCRIPTOR,device_dot_model__id__pb2.DESCRIPTOR,device_dot_brand__id__pb2.DESCRIPTOR,device_dot_variant__id__pb2.DESCRIPTOR,])




_CONFIGID = _descriptor.Descriptor(
  name='ConfigId',
  full_name='device.ConfigId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='platform_id', full_name='device.ConfigId.platform_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_id', full_name='device.ConfigId.model_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='variant_id', full_name='device.ConfigId.variant_id', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='brand_id', full_name='device.ConfigId.brand_id', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=132,
  serialized_end=292,
)

_CONFIGID.fields_by_name['platform_id'].message_type = device_dot_platform__id__pb2._PLATFORMID
_CONFIGID.fields_by_name['model_id'].message_type = device_dot_model__id__pb2._MODELID
_CONFIGID.fields_by_name['variant_id'].message_type = device_dot_variant__id__pb2._VARIANTID
_CONFIGID.fields_by_name['brand_id'].message_type = device_dot_brand__id__pb2._BRANDID
DESCRIPTOR.message_types_by_name['ConfigId'] = _CONFIGID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConfigId = _reflection.GeneratedProtocolMessageType('ConfigId', (_message.Message,), dict(
  DESCRIPTOR = _CONFIGID,
  __module__ = 'device.config_id_pb2'
  # @@protoc_insertion_point(class_scope:device.ConfigId)
  ))
_sym_db.RegisterMessage(ConfigId)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)