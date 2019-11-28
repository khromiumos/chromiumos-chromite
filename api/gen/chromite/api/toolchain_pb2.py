# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/toolchain.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromite.api import artifacts_pb2 as chromite_dot_api_dot_artifacts__pb2
from chromite.api.gen.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2
from chromite.api.gen.chromite.api import sysroot_pb2 as chromite_dot_api_dot_sysroot__pb2
from chromite.api.gen.chromiumos import builder_config_pb2 as chromiumos_dot_builder__config__pb2
from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromite/api/toolchain.proto',
  package='chromite.api',
  syntax='proto3',
  serialized_options=_b('Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'),
  serialized_pb=_b('\n\x1c\x63hromite/api/toolchain.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/artifacts.proto\x1a\x1c\x63hromite/api/build_api.proto\x1a\x1a\x63hromite/api/sysroot.proto\x1a\x1f\x63hromiumos/builder_config.proto\x1a\x17\x63hromiumos/common.proto\"l\n\x1fPrepareForToolchainBuildRequest\x12I\n\x0e\x61rtifact_types\x18\x01 \x03(\x0e\x32\x31.chromiumos.BuilderConfig.Artifacts.ArtifactTypes\"\xc5\x01\n PrepareForToolchainBuildResponse\x12V\n\x0f\x62uild_relevance\x18\x01 \x01(\x0e\x32=.chromite.api.PrepareForToolchainBuildResponse.BuildRelevance\"I\n\x0e\x42uildRelevance\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06NEEDED\x10\x01\x12\x0b\n\x07UNKNOWN\x10\x02\x12\r\n\tPOINTLESS\x10\x03\"\xc3\x01\n\x16\x42undleToolchainRequest\x12\"\n\x06\x63hroot\x18\x01 \x01(\x0b\x32\x12.chromiumos.Chroot\x12&\n\x07sysroot\x18\x02 \x01(\x0b\x32\x15.chromite.api.Sysroot\x12\x12\n\noutput_dir\x18\x03 \x01(\t\x12I\n\x0e\x61rtifact_types\x18\x04 \x03(\x0e\x32\x31.chromiumos.BuilderConfig.Artifacts.ArtifactTypes\"\xeb\x01\n\x17\x42undleToolchainResponse\x12J\n\x0e\x61rtifacts_info\x18\x01 \x03(\x0b\x32\x32.chromite.api.BundleToolchainResponse.ArtifactInfo\x1a\x83\x01\n\x0c\x41rtifactInfo\x12H\n\rartifact_type\x18\x01 \x01(\x0e\x32\x31.chromiumos.BuilderConfig.Artifacts.ArtifactTypes\x12)\n\tartifacts\x18\x02 \x03(\x0b\x32\x16.chromite.api.Artifact\"\x80\x01\n\x1aVerifyAFDOArtifactsRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x33\n\rartifact_type\x18\x02 \x01(\x0e\x32\x1c.chromiumos.AFDOArtifactType\"-\n\x1bVerifyAFDOArtifactsResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08*f\n\x10\x41\x46\x44OArtifactType\x12\r\n\tNONE_TYPE\x10\x00\x12\r\n\tORDERFILE\x10\x01\x12\x12\n\x0e\x42\x45NCHMARK_AFDO\x10\x02\x12\x0f\n\x0bKERNEL_AFDO\x10\x03\x12\x0f\n\x0b\x43HROME_AFDO\x10\x04\x32\xef\x03\n\x10ToolchainService\x12|\n\x1dUpdateEbuildWithAFDOArtifacts\x12(.chromite.api.VerifyAFDOArtifactsRequest\x1a).chromite.api.VerifyAFDOArtifactsResponse\"\x06\xc2\xed\x1a\x02\x10\x01\x12x\n\x19UploadVettedAFDOArtifacts\x12(.chromite.api.VerifyAFDOArtifactsRequest\x1a).chromite.api.VerifyAFDOArtifactsResponse\"\x06\xc2\xed\x1a\x02\x10\x01\x12p\n\x0fPrepareForBuild\x12-.chromite.api.PrepareForToolchainBuildRequest\x1a..chromite.api.PrepareForToolchainBuildResponse\x12^\n\x0f\x42undleArtifacts\x12$.chromite.api.BundleToolchainRequest\x1a%.chromite.api.BundleToolchainResponse\x1a\x11\xc2\xed\x1a\r\n\ttoolchain\x10\x02\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')
  ,
  dependencies=[chromite_dot_api_dot_artifacts__pb2.DESCRIPTOR,chromite_dot_api_dot_build__api__pb2.DESCRIPTOR,chromite_dot_api_dot_sysroot__pb2.DESCRIPTOR,chromiumos_dot_builder__config__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,])

_AFDOARTIFACTTYPE = _descriptor.EnumDescriptor(
  name='AFDOArtifactType',
  full_name='chromite.api.AFDOArtifactType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE_TYPE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDERFILE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BENCHMARK_AFDO', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KERNEL_AFDO', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHROME_AFDO', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1116,
  serialized_end=1218,
)
_sym_db.RegisterEnumDescriptor(_AFDOARTIFACTTYPE)

AFDOArtifactType = enum_type_wrapper.EnumTypeWrapper(_AFDOARTIFACTTYPE)
NONE_TYPE = 0
ORDERFILE = 1
BENCHMARK_AFDO = 2
KERNEL_AFDO = 3
CHROME_AFDO = 4


_PREPAREFORTOOLCHAINBUILDRESPONSE_BUILDRELEVANCE = _descriptor.EnumDescriptor(
  name='BuildRelevance',
  full_name='chromite.api.PrepareForToolchainBuildResponse.BuildRelevance',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEEDED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POINTLESS', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=427,
  serialized_end=500,
)
_sym_db.RegisterEnumDescriptor(_PREPAREFORTOOLCHAINBUILDRESPONSE_BUILDRELEVANCE)


_PREPAREFORTOOLCHAINBUILDREQUEST = _descriptor.Descriptor(
  name='PrepareForToolchainBuildRequest',
  full_name='chromite.api.PrepareForToolchainBuildRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artifact_types', full_name='chromite.api.PrepareForToolchainBuildRequest.artifact_types', index=0,
      number=1, type=14, cpp_type=8, label=3,
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
  serialized_start=192,
  serialized_end=300,
)


_PREPAREFORTOOLCHAINBUILDRESPONSE = _descriptor.Descriptor(
  name='PrepareForToolchainBuildResponse',
  full_name='chromite.api.PrepareForToolchainBuildResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_relevance', full_name='chromite.api.PrepareForToolchainBuildResponse.build_relevance', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PREPAREFORTOOLCHAINBUILDRESPONSE_BUILDRELEVANCE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=303,
  serialized_end=500,
)


_BUNDLETOOLCHAINREQUEST = _descriptor.Descriptor(
  name='BundleToolchainRequest',
  full_name='chromite.api.BundleToolchainRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.BundleToolchainRequest.chroot', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sysroot', full_name='chromite.api.BundleToolchainRequest.sysroot', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_dir', full_name='chromite.api.BundleToolchainRequest.output_dir', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='artifact_types', full_name='chromite.api.BundleToolchainRequest.artifact_types', index=3,
      number=4, type=14, cpp_type=8, label=3,
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
  serialized_start=503,
  serialized_end=698,
)


_BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO = _descriptor.Descriptor(
  name='ArtifactInfo',
  full_name='chromite.api.BundleToolchainResponse.ArtifactInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artifact_type', full_name='chromite.api.BundleToolchainResponse.ArtifactInfo.artifact_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='artifacts', full_name='chromite.api.BundleToolchainResponse.ArtifactInfo.artifacts', index=1,
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
  serialized_start=805,
  serialized_end=936,
)

_BUNDLETOOLCHAINRESPONSE = _descriptor.Descriptor(
  name='BundleToolchainResponse',
  full_name='chromite.api.BundleToolchainResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artifacts_info', full_name='chromite.api.BundleToolchainResponse.artifacts_info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=701,
  serialized_end=936,
)


_VERIFYAFDOARTIFACTSREQUEST = _descriptor.Descriptor(
  name='VerifyAFDOArtifactsRequest',
  full_name='chromite.api.VerifyAFDOArtifactsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.VerifyAFDOArtifactsRequest.build_target', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='artifact_type', full_name='chromite.api.VerifyAFDOArtifactsRequest.artifact_type', index=1,
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
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=939,
  serialized_end=1067,
)


_VERIFYAFDOARTIFACTSRESPONSE = _descriptor.Descriptor(
  name='VerifyAFDOArtifactsResponse',
  full_name='chromite.api.VerifyAFDOArtifactsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='chromite.api.VerifyAFDOArtifactsResponse.status', index=0,
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
  serialized_start=1069,
  serialized_end=1114,
)

_PREPAREFORTOOLCHAINBUILDREQUEST.fields_by_name['artifact_types'].enum_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ARTIFACTS_ARTIFACTTYPES
_PREPAREFORTOOLCHAINBUILDRESPONSE.fields_by_name['build_relevance'].enum_type = _PREPAREFORTOOLCHAINBUILDRESPONSE_BUILDRELEVANCE
_PREPAREFORTOOLCHAINBUILDRESPONSE_BUILDRELEVANCE.containing_type = _PREPAREFORTOOLCHAINBUILDRESPONSE
_BUNDLETOOLCHAINREQUEST.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
_BUNDLETOOLCHAINREQUEST.fields_by_name['sysroot'].message_type = chromite_dot_api_dot_sysroot__pb2._SYSROOT
_BUNDLETOOLCHAINREQUEST.fields_by_name['artifact_types'].enum_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ARTIFACTS_ARTIFACTTYPES
_BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO.fields_by_name['artifact_type'].enum_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ARTIFACTS_ARTIFACTTYPES
_BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO.fields_by_name['artifacts'].message_type = chromite_dot_api_dot_artifacts__pb2._ARTIFACT
_BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO.containing_type = _BUNDLETOOLCHAINRESPONSE
_BUNDLETOOLCHAINRESPONSE.fields_by_name['artifacts_info'].message_type = _BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO
_VERIFYAFDOARTIFACTSREQUEST.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_VERIFYAFDOARTIFACTSREQUEST.fields_by_name['artifact_type'].enum_type = chromiumos_dot_common__pb2._AFDOARTIFACTTYPE
DESCRIPTOR.message_types_by_name['PrepareForToolchainBuildRequest'] = _PREPAREFORTOOLCHAINBUILDREQUEST
DESCRIPTOR.message_types_by_name['PrepareForToolchainBuildResponse'] = _PREPAREFORTOOLCHAINBUILDRESPONSE
DESCRIPTOR.message_types_by_name['BundleToolchainRequest'] = _BUNDLETOOLCHAINREQUEST
DESCRIPTOR.message_types_by_name['BundleToolchainResponse'] = _BUNDLETOOLCHAINRESPONSE
DESCRIPTOR.message_types_by_name['VerifyAFDOArtifactsRequest'] = _VERIFYAFDOARTIFACTSREQUEST
DESCRIPTOR.message_types_by_name['VerifyAFDOArtifactsResponse'] = _VERIFYAFDOARTIFACTSRESPONSE
DESCRIPTOR.enum_types_by_name['AFDOArtifactType'] = _AFDOARTIFACTTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PrepareForToolchainBuildRequest = _reflection.GeneratedProtocolMessageType('PrepareForToolchainBuildRequest', (_message.Message,), dict(
  DESCRIPTOR = _PREPAREFORTOOLCHAINBUILDREQUEST,
  __module__ = 'chromite.api.toolchain_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.PrepareForToolchainBuildRequest)
  ))
_sym_db.RegisterMessage(PrepareForToolchainBuildRequest)

PrepareForToolchainBuildResponse = _reflection.GeneratedProtocolMessageType('PrepareForToolchainBuildResponse', (_message.Message,), dict(
  DESCRIPTOR = _PREPAREFORTOOLCHAINBUILDRESPONSE,
  __module__ = 'chromite.api.toolchain_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.PrepareForToolchainBuildResponse)
  ))
_sym_db.RegisterMessage(PrepareForToolchainBuildResponse)

BundleToolchainRequest = _reflection.GeneratedProtocolMessageType('BundleToolchainRequest', (_message.Message,), dict(
  DESCRIPTOR = _BUNDLETOOLCHAINREQUEST,
  __module__ = 'chromite.api.toolchain_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.BundleToolchainRequest)
  ))
_sym_db.RegisterMessage(BundleToolchainRequest)

BundleToolchainResponse = _reflection.GeneratedProtocolMessageType('BundleToolchainResponse', (_message.Message,), dict(

  ArtifactInfo = _reflection.GeneratedProtocolMessageType('ArtifactInfo', (_message.Message,), dict(
    DESCRIPTOR = _BUNDLETOOLCHAINRESPONSE_ARTIFACTINFO,
    __module__ = 'chromite.api.toolchain_pb2'
    # @@protoc_insertion_point(class_scope:chromite.api.BundleToolchainResponse.ArtifactInfo)
    ))
  ,
  DESCRIPTOR = _BUNDLETOOLCHAINRESPONSE,
  __module__ = 'chromite.api.toolchain_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.BundleToolchainResponse)
  ))
_sym_db.RegisterMessage(BundleToolchainResponse)
_sym_db.RegisterMessage(BundleToolchainResponse.ArtifactInfo)

VerifyAFDOArtifactsRequest = _reflection.GeneratedProtocolMessageType('VerifyAFDOArtifactsRequest', (_message.Message,), dict(
  DESCRIPTOR = _VERIFYAFDOARTIFACTSREQUEST,
  __module__ = 'chromite.api.toolchain_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.VerifyAFDOArtifactsRequest)
  ))
_sym_db.RegisterMessage(VerifyAFDOArtifactsRequest)

VerifyAFDOArtifactsResponse = _reflection.GeneratedProtocolMessageType('VerifyAFDOArtifactsResponse', (_message.Message,), dict(
  DESCRIPTOR = _VERIFYAFDOARTIFACTSRESPONSE,
  __module__ = 'chromite.api.toolchain_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.VerifyAFDOArtifactsResponse)
  ))
_sym_db.RegisterMessage(VerifyAFDOArtifactsResponse)


DESCRIPTOR._options = None

_TOOLCHAINSERVICE = _descriptor.ServiceDescriptor(
  name='ToolchainService',
  full_name='chromite.api.ToolchainService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\302\355\032\r\n\ttoolchain\020\002'),
  serialized_start=1221,
  serialized_end=1716,
  methods=[
  _descriptor.MethodDescriptor(
    name='UpdateEbuildWithAFDOArtifacts',
    full_name='chromite.api.ToolchainService.UpdateEbuildWithAFDOArtifacts',
    index=0,
    containing_service=None,
    input_type=_VERIFYAFDOARTIFACTSREQUEST,
    output_type=_VERIFYAFDOARTIFACTSRESPONSE,
    serialized_options=_b('\302\355\032\002\020\001'),
  ),
  _descriptor.MethodDescriptor(
    name='UploadVettedAFDOArtifacts',
    full_name='chromite.api.ToolchainService.UploadVettedAFDOArtifacts',
    index=1,
    containing_service=None,
    input_type=_VERIFYAFDOARTIFACTSREQUEST,
    output_type=_VERIFYAFDOARTIFACTSRESPONSE,
    serialized_options=_b('\302\355\032\002\020\001'),
  ),
  _descriptor.MethodDescriptor(
    name='PrepareForBuild',
    full_name='chromite.api.ToolchainService.PrepareForBuild',
    index=2,
    containing_service=None,
    input_type=_PREPAREFORTOOLCHAINBUILDREQUEST,
    output_type=_PREPAREFORTOOLCHAINBUILDRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='BundleArtifacts',
    full_name='chromite.api.ToolchainService.BundleArtifacts',
    index=3,
    containing_service=None,
    input_type=_BUNDLETOOLCHAINREQUEST,
    output_type=_BUNDLETOOLCHAINRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TOOLCHAINSERVICE)

DESCRIPTOR.services_by_name['ToolchainService'] = _TOOLCHAINSERVICE

# @@protoc_insertion_point(module_scope)
