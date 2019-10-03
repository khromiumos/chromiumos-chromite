# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/common.proto',
  package='chromiumos',
  syntax='proto3',
  serialized_options=_b('Z4go.chromium.org/chromiumos/infra/proto/go/chromiumos'),
  serialized_pb=_b('\n\x17\x63hromiumos/common.proto\x12\nchromiumos\"\x1b\n\x0b\x42uildTarget\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xea\x01\n\x06\x43hroot\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x11\n\tcache_dir\x18\x02 \x01(\t\x12)\n\x03\x65nv\x18\x03 \x01(\x0b\x32\x1c.chromiumos.Chroot.ChrootEnv\x12\x12\n\nchrome_dir\x18\x04 \x01(\t\x12$\n\x04goma\x18\x05 \x01(\x0b\x32\x16.chromiumos.GomaConfig\x1aZ\n\tChrootEnv\x12&\n\tuse_flags\x18\x01 \x03(\x0b\x32\x13.chromiumos.UseFlag\x12%\n\x08\x66\x65\x61tures\x18\x02 \x03(\x0b\x32\x13.chromiumos.Feature\"\x1a\n\x07\x46\x65\x61ture\x12\x0f\n\x07\x66\x65\x61ture\x18\x01 \x01(\t\"S\n\nGomaConfig\x12\x10\n\x08goma_dir\x18\x01 \x01(\t\x12\x18\n\x10goma_client_json\x18\x02 \x01(\t\x12\x19\n\x11\x63hromeos_goma_dir\x18\x03 \x01(\t\"F\n\x0bPackageInfo\x12\x14\n\x0cpackage_name\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\"w\n\x04Path\x12\x0c\n\x04path\x18\x01 \x01(\t\x12+\n\x08location\x18\x02 \x01(\x0e\x32\x19.chromiumos.Path.Location\"4\n\x08Location\x12\x0f\n\x0bNO_LOCATION\x10\x00\x12\n\n\x06INSIDE\x10\x01\x12\x0b\n\x07OUTSIDE\x10\x02\",\n\nResultPath\x12\x1e\n\x04path\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path\"\x17\n\x07UseFlag\x12\x0c\n\x04\x66lag\x18\x01 \x01(\t\"&\n\nProtoBytes\x12\x18\n\x10serialized_proto\x18\x01 \x01(\x0c*\x98\x01\n\tImageType\x12\x18\n\x14IMAGE_TYPE_UNDEFINED\x10\x00\x12\x08\n\x04\x42\x41SE\x10\x01\x12\x07\n\x03\x44\x45V\x10\x02\x12\x08\n\x04TEST\x10\x03\x12\x0b\n\x07\x42\x41SE_VM\x10\x04\x12\x0b\n\x07TEST_VM\x10\x05\x12\x0c\n\x08RECOVERY\x10\x06\x12\x0b\n\x07\x46\x41\x43TORY\x10\x07\x12\x0c\n\x08\x46IRMWARE\x10\x08\x12\x11\n\rCR50_FIRMWARE\x10\t*m\n\x07\x43hannel\x12\x17\n\x13\x43HANNEL_UNSPECIFIED\x10\x00\x12\x12\n\x0e\x43HANNEL_STABLE\x10\x01\x12\x10\n\x0c\x43HANNEL_BETA\x10\x02\x12\x0f\n\x0b\x43HANNEL_DEV\x10\x03\x12\x12\n\x0e\x43HANNEL_CANARY\x10\x04\x42\x36Z4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3')
)

_IMAGETYPE = _descriptor.EnumDescriptor(
  name='ImageType',
  full_name='chromiumos.ImageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='IMAGE_TYPE_UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BASE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEV', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEST', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BASE_VM', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEST_VM', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECOVERY', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FACTORY', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIRMWARE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CR50_FIRMWARE', index=9, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=723,
  serialized_end=875,
)
_sym_db.RegisterEnumDescriptor(_IMAGETYPE)

ImageType = enum_type_wrapper.EnumTypeWrapper(_IMAGETYPE)
_CHANNEL = _descriptor.EnumDescriptor(
  name='Channel',
  full_name='chromiumos.Channel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CHANNEL_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHANNEL_STABLE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHANNEL_BETA', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHANNEL_DEV', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHANNEL_CANARY', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=877,
  serialized_end=986,
)
_sym_db.RegisterEnumDescriptor(_CHANNEL)

Channel = enum_type_wrapper.EnumTypeWrapper(_CHANNEL)
IMAGE_TYPE_UNDEFINED = 0
BASE = 1
DEV = 2
TEST = 3
BASE_VM = 4
TEST_VM = 5
RECOVERY = 6
FACTORY = 7
FIRMWARE = 8
CR50_FIRMWARE = 9
CHANNEL_UNSPECIFIED = 0
CHANNEL_STABLE = 1
CHANNEL_BETA = 2
CHANNEL_DEV = 3
CHANNEL_CANARY = 4


_PATH_LOCATION = _descriptor.EnumDescriptor(
  name='Location',
  full_name='chromiumos.Path.Location',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_LOCATION', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INSIDE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OUTSIDE', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=557,
  serialized_end=609,
)
_sym_db.RegisterEnumDescriptor(_PATH_LOCATION)


_BUILDTARGET = _descriptor.Descriptor(
  name='BuildTarget',
  full_name='chromiumos.BuildTarget',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.BuildTarget.name', index=0,
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
  serialized_start=39,
  serialized_end=66,
)


_CHROOT_CHROOTENV = _descriptor.Descriptor(
  name='ChrootEnv',
  full_name='chromiumos.Chroot.ChrootEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='use_flags', full_name='chromiumos.Chroot.ChrootEnv.use_flags', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='features', full_name='chromiumos.Chroot.ChrootEnv.features', index=1,
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
  serialized_start=213,
  serialized_end=303,
)

_CHROOT = _descriptor.Descriptor(
  name='Chroot',
  full_name='chromiumos.Chroot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromiumos.Chroot.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cache_dir', full_name='chromiumos.Chroot.cache_dir', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='env', full_name='chromiumos.Chroot.env', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chrome_dir', full_name='chromiumos.Chroot.chrome_dir', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='goma', full_name='chromiumos.Chroot.goma', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CHROOT_CHROOTENV, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=303,
)


_FEATURE = _descriptor.Descriptor(
  name='Feature',
  full_name='chromiumos.Feature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature', full_name='chromiumos.Feature.feature', index=0,
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
  serialized_start=305,
  serialized_end=331,
)


_GOMACONFIG = _descriptor.Descriptor(
  name='GomaConfig',
  full_name='chromiumos.GomaConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='goma_dir', full_name='chromiumos.GomaConfig.goma_dir', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='goma_client_json', full_name='chromiumos.GomaConfig.goma_client_json', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chromeos_goma_dir', full_name='chromiumos.GomaConfig.chromeos_goma_dir', index=2,
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
  ],
  serialized_start=333,
  serialized_end=416,
)


_PACKAGEINFO = _descriptor.Descriptor(
  name='PackageInfo',
  full_name='chromiumos.PackageInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='package_name', full_name='chromiumos.PackageInfo.package_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='category', full_name='chromiumos.PackageInfo.category', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='chromiumos.PackageInfo.version', index=2,
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
  ],
  serialized_start=418,
  serialized_end=488,
)


_PATH = _descriptor.Descriptor(
  name='Path',
  full_name='chromiumos.Path',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromiumos.Path.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='location', full_name='chromiumos.Path.location', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PATH_LOCATION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=490,
  serialized_end=609,
)


_RESULTPATH = _descriptor.Descriptor(
  name='ResultPath',
  full_name='chromiumos.ResultPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromiumos.ResultPath.path', index=0,
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
  serialized_start=611,
  serialized_end=655,
)


_USEFLAG = _descriptor.Descriptor(
  name='UseFlag',
  full_name='chromiumos.UseFlag',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='flag', full_name='chromiumos.UseFlag.flag', index=0,
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
  serialized_start=657,
  serialized_end=680,
)


_PROTOBYTES = _descriptor.Descriptor(
  name='ProtoBytes',
  full_name='chromiumos.ProtoBytes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serialized_proto', full_name='chromiumos.ProtoBytes.serialized_proto', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=682,
  serialized_end=720,
)

_CHROOT_CHROOTENV.fields_by_name['use_flags'].message_type = _USEFLAG
_CHROOT_CHROOTENV.fields_by_name['features'].message_type = _FEATURE
_CHROOT_CHROOTENV.containing_type = _CHROOT
_CHROOT.fields_by_name['env'].message_type = _CHROOT_CHROOTENV
_CHROOT.fields_by_name['goma'].message_type = _GOMACONFIG
_PATH.fields_by_name['location'].enum_type = _PATH_LOCATION
_PATH_LOCATION.containing_type = _PATH
_RESULTPATH.fields_by_name['path'].message_type = _PATH
DESCRIPTOR.message_types_by_name['BuildTarget'] = _BUILDTARGET
DESCRIPTOR.message_types_by_name['Chroot'] = _CHROOT
DESCRIPTOR.message_types_by_name['Feature'] = _FEATURE
DESCRIPTOR.message_types_by_name['GomaConfig'] = _GOMACONFIG
DESCRIPTOR.message_types_by_name['PackageInfo'] = _PACKAGEINFO
DESCRIPTOR.message_types_by_name['Path'] = _PATH
DESCRIPTOR.message_types_by_name['ResultPath'] = _RESULTPATH
DESCRIPTOR.message_types_by_name['UseFlag'] = _USEFLAG
DESCRIPTOR.message_types_by_name['ProtoBytes'] = _PROTOBYTES
DESCRIPTOR.enum_types_by_name['ImageType'] = _IMAGETYPE
DESCRIPTOR.enum_types_by_name['Channel'] = _CHANNEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BuildTarget = _reflection.GeneratedProtocolMessageType('BuildTarget', (_message.Message,), dict(
  DESCRIPTOR = _BUILDTARGET,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.BuildTarget)
  ))
_sym_db.RegisterMessage(BuildTarget)

Chroot = _reflection.GeneratedProtocolMessageType('Chroot', (_message.Message,), dict(

  ChrootEnv = _reflection.GeneratedProtocolMessageType('ChrootEnv', (_message.Message,), dict(
    DESCRIPTOR = _CHROOT_CHROOTENV,
    __module__ = 'chromiumos.common_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.Chroot.ChrootEnv)
    ))
  ,
  DESCRIPTOR = _CHROOT,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.Chroot)
  ))
_sym_db.RegisterMessage(Chroot)
_sym_db.RegisterMessage(Chroot.ChrootEnv)

Feature = _reflection.GeneratedProtocolMessageType('Feature', (_message.Message,), dict(
  DESCRIPTOR = _FEATURE,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.Feature)
  ))
_sym_db.RegisterMessage(Feature)

GomaConfig = _reflection.GeneratedProtocolMessageType('GomaConfig', (_message.Message,), dict(
  DESCRIPTOR = _GOMACONFIG,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.GomaConfig)
  ))
_sym_db.RegisterMessage(GomaConfig)

PackageInfo = _reflection.GeneratedProtocolMessageType('PackageInfo', (_message.Message,), dict(
  DESCRIPTOR = _PACKAGEINFO,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.PackageInfo)
  ))
_sym_db.RegisterMessage(PackageInfo)

Path = _reflection.GeneratedProtocolMessageType('Path', (_message.Message,), dict(
  DESCRIPTOR = _PATH,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.Path)
  ))
_sym_db.RegisterMessage(Path)

ResultPath = _reflection.GeneratedProtocolMessageType('ResultPath', (_message.Message,), dict(
  DESCRIPTOR = _RESULTPATH,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.ResultPath)
  ))
_sym_db.RegisterMessage(ResultPath)

UseFlag = _reflection.GeneratedProtocolMessageType('UseFlag', (_message.Message,), dict(
  DESCRIPTOR = _USEFLAG,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.UseFlag)
  ))
_sym_db.RegisterMessage(UseFlag)

ProtoBytes = _reflection.GeneratedProtocolMessageType('ProtoBytes', (_message.Message,), dict(
  DESCRIPTOR = _PROTOBYTES,
  __module__ = 'chromiumos.common_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.ProtoBytes)
  ))
_sym_db.RegisterMessage(ProtoBytes)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
