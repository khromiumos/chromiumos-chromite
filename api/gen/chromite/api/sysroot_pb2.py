# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/sysroot.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2
from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromite/api/sysroot.proto',
  package='chromite.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1a\x63hromite/api/sysroot.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x17\x63hromiumos/common.proto\"F\n\x07Sysroot\x12\x0c\n\x04path\x18\x01 \x01(\t\x12-\n\x0c\x62uild_target\x18\x02 \x01(\x0b\x32\x17.chromiumos.BuildTarget\"\x17\n\x07Profile\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xd8\x01\n\x14SysrootCreateRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x37\n\x05\x66lags\x18\x02 \x01(\x0b\x32(.chromite.api.SysrootCreateRequest.Flags\x12&\n\x07profile\x18\x03 \x01(\x0b\x32\x15.chromite.api.Profile\x1a\x30\n\x05\x46lags\x12\x16\n\x0e\x63hroot_current\x18\x01 \x01(\x08\x12\x0f\n\x07replace\x18\x02 \x01(\x08\"?\n\x15SysrootCreateResponse\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\"\x9e\x01\n\x17InstallToolchainRequest\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12:\n\x05\x66lags\x18\x02 \x01(\x0b\x32+.chromite.api.InstallToolchainRequest.Flags\x1a\x1f\n\x05\x46lags\x12\x16\n\x0e\x63ompile_source\x18\x01 \x01(\x08\"L\n\x18InstallToolchainResponse\x12\x30\n\x0f\x66\x61iled_packages\x18\x01 \x03(\x0b\x32\x17.chromiumos.PackageInfo\"\xdb\x01\n\x16InstallPackagesRequest\x12&\n\x07sysroot\x18\x01 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x39\n\x05\x66lags\x18\x02 \x01(\x0b\x32*.chromite.api.InstallPackagesRequest.Flags\x12)\n\x08packages\x18\x03 \x03(\x0b\x32\x17.chromiumos.PackageInfo\x1a\x33\n\x05\x46lags\x12\x16\n\x0e\x63ompile_source\x18\x01 \x01(\x08\x12\x12\n\nevent_file\x18\x02 \x01(\t\"K\n\x17InstallPackagesResponse\x12\x30\n\x0f\x66\x61iled_packages\x18\x01 \x03(\x0b\x32\x17.chromiumos.PackageInfo2\xb7\x02\n\x0eSysrootService\x12Q\n\x06\x43reate\x12\".chromite.api.SysrootCreateRequest\x1a#.chromite.api.SysrootCreateResponse\x12\x61\n\x10InstallToolchain\x12%.chromite.api.InstallToolchainRequest\x1a&.chromite.api.InstallToolchainResponse\x12^\n\x0fInstallPackages\x12$.chromite.api.InstallPackagesRequest\x1a%.chromite.api.InstallPackagesResponse\x1a\x0f\xc2\xed\x1a\x0b\n\x07sysroot\x10\x01\x62\x06proto3')
  ,
  dependencies=[chromite_dot_api_dot_build__api__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,])




_SYSROOT = _descriptor.Descriptor(
  name='Sysroot',
  full_name='chromite.api.Sysroot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromite.api.Sysroot.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.Sysroot.build_target', index=1,
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
  serialized_start=99,
  serialized_end=169,
)


_PROFILE = _descriptor.Descriptor(
  name='Profile',
  full_name='chromite.api.Profile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromite.api.Profile.name', index=0,
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
  serialized_start=171,
  serialized_end=194,
)


_SYSROOTCREATEREQUEST_FLAGS = _descriptor.Descriptor(
  name='Flags',
  full_name='chromite.api.SysrootCreateRequest.Flags',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chroot_current', full_name='chromite.api.SysrootCreateRequest.Flags.chroot_current', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='replace', full_name='chromite.api.SysrootCreateRequest.Flags.replace', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=365,
  serialized_end=413,
)

_SYSROOTCREATEREQUEST = _descriptor.Descriptor(
  name='SysrootCreateRequest',
  full_name='chromite.api.SysrootCreateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.SysrootCreateRequest.build_target', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='flags', full_name='chromite.api.SysrootCreateRequest.flags', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='profile', full_name='chromite.api.SysrootCreateRequest.profile', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SYSROOTCREATEREQUEST_FLAGS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=197,
  serialized_end=413,
)


_SYSROOTCREATERESPONSE = _descriptor.Descriptor(
  name='SysrootCreateResponse',
  full_name='chromite.api.SysrootCreateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sysroot', full_name='chromite.api.SysrootCreateResponse.sysroot', index=0,
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
  serialized_start=415,
  serialized_end=478,
)


_INSTALLTOOLCHAINREQUEST_FLAGS = _descriptor.Descriptor(
  name='Flags',
  full_name='chromite.api.InstallToolchainRequest.Flags',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='compile_source', full_name='chromite.api.InstallToolchainRequest.Flags.compile_source', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=608,
  serialized_end=639,
)

_INSTALLTOOLCHAINREQUEST = _descriptor.Descriptor(
  name='InstallToolchainRequest',
  full_name='chromite.api.InstallToolchainRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sysroot', full_name='chromite.api.InstallToolchainRequest.sysroot', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='flags', full_name='chromite.api.InstallToolchainRequest.flags', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_INSTALLTOOLCHAINREQUEST_FLAGS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=481,
  serialized_end=639,
)


_INSTALLTOOLCHAINRESPONSE = _descriptor.Descriptor(
  name='InstallToolchainResponse',
  full_name='chromite.api.InstallToolchainResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='failed_packages', full_name='chromite.api.InstallToolchainResponse.failed_packages', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=641,
  serialized_end=717,
)


_INSTALLPACKAGESREQUEST_FLAGS = _descriptor.Descriptor(
  name='Flags',
  full_name='chromite.api.InstallPackagesRequest.Flags',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='compile_source', full_name='chromite.api.InstallPackagesRequest.Flags.compile_source', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='event_file', full_name='chromite.api.InstallPackagesRequest.Flags.event_file', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=888,
  serialized_end=939,
)

_INSTALLPACKAGESREQUEST = _descriptor.Descriptor(
  name='InstallPackagesRequest',
  full_name='chromite.api.InstallPackagesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sysroot', full_name='chromite.api.InstallPackagesRequest.sysroot', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='flags', full_name='chromite.api.InstallPackagesRequest.flags', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='packages', full_name='chromite.api.InstallPackagesRequest.packages', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_INSTALLPACKAGESREQUEST_FLAGS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=720,
  serialized_end=939,
)


_INSTALLPACKAGESRESPONSE = _descriptor.Descriptor(
  name='InstallPackagesResponse',
  full_name='chromite.api.InstallPackagesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='failed_packages', full_name='chromite.api.InstallPackagesResponse.failed_packages', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=941,
  serialized_end=1016,
)

_SYSROOT.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_SYSROOTCREATEREQUEST_FLAGS.containing_type = _SYSROOTCREATEREQUEST
_SYSROOTCREATEREQUEST.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_SYSROOTCREATEREQUEST.fields_by_name['flags'].message_type = _SYSROOTCREATEREQUEST_FLAGS
_SYSROOTCREATEREQUEST.fields_by_name['profile'].message_type = _PROFILE
_SYSROOTCREATERESPONSE.fields_by_name['sysroot'].message_type = _SYSROOT
_INSTALLTOOLCHAINREQUEST_FLAGS.containing_type = _INSTALLTOOLCHAINREQUEST
_INSTALLTOOLCHAINREQUEST.fields_by_name['sysroot'].message_type = _SYSROOT
_INSTALLTOOLCHAINREQUEST.fields_by_name['flags'].message_type = _INSTALLTOOLCHAINREQUEST_FLAGS
_INSTALLTOOLCHAINRESPONSE.fields_by_name['failed_packages'].message_type = chromiumos_dot_common__pb2._PACKAGEINFO
_INSTALLPACKAGESREQUEST_FLAGS.containing_type = _INSTALLPACKAGESREQUEST
_INSTALLPACKAGESREQUEST.fields_by_name['sysroot'].message_type = _SYSROOT
_INSTALLPACKAGESREQUEST.fields_by_name['flags'].message_type = _INSTALLPACKAGESREQUEST_FLAGS
_INSTALLPACKAGESREQUEST.fields_by_name['packages'].message_type = chromiumos_dot_common__pb2._PACKAGEINFO
_INSTALLPACKAGESRESPONSE.fields_by_name['failed_packages'].message_type = chromiumos_dot_common__pb2._PACKAGEINFO
DESCRIPTOR.message_types_by_name['Sysroot'] = _SYSROOT
DESCRIPTOR.message_types_by_name['Profile'] = _PROFILE
DESCRIPTOR.message_types_by_name['SysrootCreateRequest'] = _SYSROOTCREATEREQUEST
DESCRIPTOR.message_types_by_name['SysrootCreateResponse'] = _SYSROOTCREATERESPONSE
DESCRIPTOR.message_types_by_name['InstallToolchainRequest'] = _INSTALLTOOLCHAINREQUEST
DESCRIPTOR.message_types_by_name['InstallToolchainResponse'] = _INSTALLTOOLCHAINRESPONSE
DESCRIPTOR.message_types_by_name['InstallPackagesRequest'] = _INSTALLPACKAGESREQUEST
DESCRIPTOR.message_types_by_name['InstallPackagesResponse'] = _INSTALLPACKAGESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Sysroot = _reflection.GeneratedProtocolMessageType('Sysroot', (_message.Message,), dict(
  DESCRIPTOR = _SYSROOT,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.Sysroot)
  ))
_sym_db.RegisterMessage(Sysroot)

Profile = _reflection.GeneratedProtocolMessageType('Profile', (_message.Message,), dict(
  DESCRIPTOR = _PROFILE,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.Profile)
  ))
_sym_db.RegisterMessage(Profile)

SysrootCreateRequest = _reflection.GeneratedProtocolMessageType('SysrootCreateRequest', (_message.Message,), dict(

  Flags = _reflection.GeneratedProtocolMessageType('Flags', (_message.Message,), dict(
    DESCRIPTOR = _SYSROOTCREATEREQUEST_FLAGS,
    __module__ = 'chromite.api.sysroot_pb2'
    # @@protoc_insertion_point(class_scope:chromite.api.SysrootCreateRequest.Flags)
    ))
  ,
  DESCRIPTOR = _SYSROOTCREATEREQUEST,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.SysrootCreateRequest)
  ))
_sym_db.RegisterMessage(SysrootCreateRequest)
_sym_db.RegisterMessage(SysrootCreateRequest.Flags)

SysrootCreateResponse = _reflection.GeneratedProtocolMessageType('SysrootCreateResponse', (_message.Message,), dict(
  DESCRIPTOR = _SYSROOTCREATERESPONSE,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.SysrootCreateResponse)
  ))
_sym_db.RegisterMessage(SysrootCreateResponse)

InstallToolchainRequest = _reflection.GeneratedProtocolMessageType('InstallToolchainRequest', (_message.Message,), dict(

  Flags = _reflection.GeneratedProtocolMessageType('Flags', (_message.Message,), dict(
    DESCRIPTOR = _INSTALLTOOLCHAINREQUEST_FLAGS,
    __module__ = 'chromite.api.sysroot_pb2'
    # @@protoc_insertion_point(class_scope:chromite.api.InstallToolchainRequest.Flags)
    ))
  ,
  DESCRIPTOR = _INSTALLTOOLCHAINREQUEST,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.InstallToolchainRequest)
  ))
_sym_db.RegisterMessage(InstallToolchainRequest)
_sym_db.RegisterMessage(InstallToolchainRequest.Flags)

InstallToolchainResponse = _reflection.GeneratedProtocolMessageType('InstallToolchainResponse', (_message.Message,), dict(
  DESCRIPTOR = _INSTALLTOOLCHAINRESPONSE,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.InstallToolchainResponse)
  ))
_sym_db.RegisterMessage(InstallToolchainResponse)

InstallPackagesRequest = _reflection.GeneratedProtocolMessageType('InstallPackagesRequest', (_message.Message,), dict(

  Flags = _reflection.GeneratedProtocolMessageType('Flags', (_message.Message,), dict(
    DESCRIPTOR = _INSTALLPACKAGESREQUEST_FLAGS,
    __module__ = 'chromite.api.sysroot_pb2'
    # @@protoc_insertion_point(class_scope:chromite.api.InstallPackagesRequest.Flags)
    ))
  ,
  DESCRIPTOR = _INSTALLPACKAGESREQUEST,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.InstallPackagesRequest)
  ))
_sym_db.RegisterMessage(InstallPackagesRequest)
_sym_db.RegisterMessage(InstallPackagesRequest.Flags)

InstallPackagesResponse = _reflection.GeneratedProtocolMessageType('InstallPackagesResponse', (_message.Message,), dict(
  DESCRIPTOR = _INSTALLPACKAGESRESPONSE,
  __module__ = 'chromite.api.sysroot_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.InstallPackagesResponse)
  ))
_sym_db.RegisterMessage(InstallPackagesResponse)



_SYSROOTSERVICE = _descriptor.ServiceDescriptor(
  name='SysrootService',
  full_name='chromite.api.SysrootService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\302\355\032\013\n\007sysroot\020\001'),
  serialized_start=1019,
  serialized_end=1330,
  methods=[
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='chromite.api.SysrootService.Create',
    index=0,
    containing_service=None,
    input_type=_SYSROOTCREATEREQUEST,
    output_type=_SYSROOTCREATERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='InstallToolchain',
    full_name='chromite.api.SysrootService.InstallToolchain',
    index=1,
    containing_service=None,
    input_type=_INSTALLTOOLCHAINREQUEST,
    output_type=_INSTALLTOOLCHAINRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='InstallPackages',
    full_name='chromite.api.SysrootService.InstallPackages',
    index=2,
    containing_service=None,
    input_type=_INSTALLPACKAGESREQUEST,
    output_type=_INSTALLPACKAGESRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SYSROOTSERVICE)

DESCRIPTOR.services_by_name['SysrootService'] = _SYSROOTSERVICE

# @@protoc_insertion_point(module_scope)