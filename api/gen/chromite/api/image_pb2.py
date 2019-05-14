# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/image.proto

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
  name='chromite/api/image.proto',
  package='chromite.api',
  syntax='proto3',
  serialized_options=_b('Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'),
  serialized_pb=_b('\n\x18\x63hromite/api/image.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x17\x63hromiumos/common.proto\"i\n\x05Image\x12\x0c\n\x04path\x18\x01 \x01(\t\x12#\n\x04type\x18\x02 \x01(\x0e\x32\x15.chromiumos.ImageType\x12-\n\x0c\x62uild_target\x18\x03 \x01(\x0b\x32\x17.chromiumos.BuildTarget\"\xf4\x01\n\x12\x43reateImageRequest\x12-\n\x0c\x62uild_target\x18\x01 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12*\n\x0bimage_types\x18\x02 \x03(\x0e\x32\x15.chromiumos.ImageType\x12#\n\x1b\x64isable_rootfs_verification\x18\x03 \x01(\x08\x12\x0f\n\x07version\x18\x04 \x01(\t\x12\x13\n\x0b\x64isk_layout\x18\x05 \x01(\t\x12\x14\n\x0c\x62uilder_path\x18\x06 \x01(\t\x12\"\n\x06\x63hroot\x18\x07 \x01(\x0b\x32\x12.chromiumos.Chroot\"{\n\x11\x43reateImageResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12#\n\x06images\x18\x02 \x03(\x0b\x32\x13.chromite.api.Image\x12\x30\n\x0f\x66\x61iled_packages\x18\x03 \x03(\x0b\x32\x17.chromiumos.PackageInfo\"Y\n\x0f\x43reateVmRequest\x12\"\n\x05image\x18\x01 \x01(\x0b\x32\x13.chromite.api.Image\x12\"\n\x06\x63hroot\x18\x02 \x01(\x0b\x32\x12.chromiumos.Chroot\"\x17\n\x07VmImage\x12\x0c\n\x04path\x18\x01 \x01(\t\";\n\x10\x43reateVmResponse\x12\'\n\x08vm_image\x18\x01 \x01(\x0b\x32\x15.chromite.api.VmImage\"\xdd\x01\n\x10TestImageRequest\x12\"\n\x05image\x18\x01 \x01(\x0b\x32\x13.chromite.api.Image\x12-\n\x0c\x62uild_target\x18\x02 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x35\n\x06result\x18\x03 \x01(\x0b\x32%.chromite.api.TestImageRequest.Result\x12\"\n\x06\x63hroot\x18\x04 \x01(\x0b\x32\x12.chromiumos.Chroot\x1a\x1b\n\x06Result\x12\x11\n\tdirectory\x18\x01 \x01(\t\"\"\n\x0fTestImageResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x84\x02\n\x0cImageService\x12K\n\x06\x43reate\x12 .chromite.api.CreateImageRequest\x1a\x1f.chromite.api.CreateImageResult\x12Q\n\x08\x43reateVm\x12\x1d.chromite.api.CreateVmRequest\x1a\x1e.chromite.api.CreateVmResponse\"\x06\xc2\xed\x1a\x02\x10\x02\x12\x45\n\x04Test\x12\x1e.chromite.api.TestImageRequest\x1a\x1d.chromite.api.TestImageResult\x1a\r\xc2\xed\x1a\t\n\x05image\x10\x01\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')
  ,
  dependencies=[chromite_dot_api_dot_build__api__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,])




_IMAGE = _descriptor.Descriptor(
  name='Image',
  full_name='chromite.api.Image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromite.api.Image.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='chromite.api.Image.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.Image.build_target', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=97,
  serialized_end=202,
)


_CREATEIMAGEREQUEST = _descriptor.Descriptor(
  name='CreateImageRequest',
  full_name='chromite.api.CreateImageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.CreateImageRequest.build_target', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_types', full_name='chromite.api.CreateImageRequest.image_types', index=1,
      number=2, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disable_rootfs_verification', full_name='chromite.api.CreateImageRequest.disable_rootfs_verification', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='chromite.api.CreateImageRequest.version', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_layout', full_name='chromite.api.CreateImageRequest.disk_layout', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='builder_path', full_name='chromite.api.CreateImageRequest.builder_path', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.CreateImageRequest.chroot', index=6,
      number=7, type=11, cpp_type=10, label=1,
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
  serialized_start=205,
  serialized_end=449,
)


_CREATEIMAGERESULT = _descriptor.Descriptor(
  name='CreateImageResult',
  full_name='chromite.api.CreateImageResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='chromite.api.CreateImageResult.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='images', full_name='chromite.api.CreateImageResult.images', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='failed_packages', full_name='chromite.api.CreateImageResult.failed_packages', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=451,
  serialized_end=574,
)


_CREATEVMREQUEST = _descriptor.Descriptor(
  name='CreateVmRequest',
  full_name='chromite.api.CreateVmRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='chromite.api.CreateVmRequest.image', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.CreateVmRequest.chroot', index=1,
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
  serialized_start=576,
  serialized_end=665,
)


_VMIMAGE = _descriptor.Descriptor(
  name='VmImage',
  full_name='chromite.api.VmImage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromite.api.VmImage.path', index=0,
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
  serialized_start=667,
  serialized_end=690,
)


_CREATEVMRESPONSE = _descriptor.Descriptor(
  name='CreateVmResponse',
  full_name='chromite.api.CreateVmResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vm_image', full_name='chromite.api.CreateVmResponse.vm_image', index=0,
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
  serialized_start=692,
  serialized_end=751,
)


_TESTIMAGEREQUEST_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='chromite.api.TestImageRequest.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='directory', full_name='chromite.api.TestImageRequest.Result.directory', index=0,
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
  serialized_start=948,
  serialized_end=975,
)

_TESTIMAGEREQUEST = _descriptor.Descriptor(
  name='TestImageRequest',
  full_name='chromite.api.TestImageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='chromite.api.TestImageRequest.image', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.TestImageRequest.build_target', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='chromite.api.TestImageRequest.result', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.TestImageRequest.chroot', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TESTIMAGEREQUEST_RESULT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=754,
  serialized_end=975,
)


_TESTIMAGERESULT = _descriptor.Descriptor(
  name='TestImageResult',
  full_name='chromite.api.TestImageResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='chromite.api.TestImageResult.success', index=0,
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
  serialized_start=977,
  serialized_end=1011,
)

_IMAGE.fields_by_name['type'].enum_type = chromiumos_dot_common__pb2._IMAGETYPE
_IMAGE.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_CREATEIMAGEREQUEST.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_CREATEIMAGEREQUEST.fields_by_name['image_types'].enum_type = chromiumos_dot_common__pb2._IMAGETYPE
_CREATEIMAGEREQUEST.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
_CREATEIMAGERESULT.fields_by_name['images'].message_type = _IMAGE
_CREATEIMAGERESULT.fields_by_name['failed_packages'].message_type = chromiumos_dot_common__pb2._PACKAGEINFO
_CREATEVMREQUEST.fields_by_name['image'].message_type = _IMAGE
_CREATEVMREQUEST.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
_CREATEVMRESPONSE.fields_by_name['vm_image'].message_type = _VMIMAGE
_TESTIMAGEREQUEST_RESULT.containing_type = _TESTIMAGEREQUEST
_TESTIMAGEREQUEST.fields_by_name['image'].message_type = _IMAGE
_TESTIMAGEREQUEST.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_TESTIMAGEREQUEST.fields_by_name['result'].message_type = _TESTIMAGEREQUEST_RESULT
_TESTIMAGEREQUEST.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
DESCRIPTOR.message_types_by_name['Image'] = _IMAGE
DESCRIPTOR.message_types_by_name['CreateImageRequest'] = _CREATEIMAGEREQUEST
DESCRIPTOR.message_types_by_name['CreateImageResult'] = _CREATEIMAGERESULT
DESCRIPTOR.message_types_by_name['CreateVmRequest'] = _CREATEVMREQUEST
DESCRIPTOR.message_types_by_name['VmImage'] = _VMIMAGE
DESCRIPTOR.message_types_by_name['CreateVmResponse'] = _CREATEVMRESPONSE
DESCRIPTOR.message_types_by_name['TestImageRequest'] = _TESTIMAGEREQUEST
DESCRIPTOR.message_types_by_name['TestImageResult'] = _TESTIMAGERESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Image = _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), dict(
  DESCRIPTOR = _IMAGE,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.Image)
  ))
_sym_db.RegisterMessage(Image)

CreateImageRequest = _reflection.GeneratedProtocolMessageType('CreateImageRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEIMAGEREQUEST,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.CreateImageRequest)
  ))
_sym_db.RegisterMessage(CreateImageRequest)

CreateImageResult = _reflection.GeneratedProtocolMessageType('CreateImageResult', (_message.Message,), dict(
  DESCRIPTOR = _CREATEIMAGERESULT,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.CreateImageResult)
  ))
_sym_db.RegisterMessage(CreateImageResult)

CreateVmRequest = _reflection.GeneratedProtocolMessageType('CreateVmRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEVMREQUEST,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.CreateVmRequest)
  ))
_sym_db.RegisterMessage(CreateVmRequest)

VmImage = _reflection.GeneratedProtocolMessageType('VmImage', (_message.Message,), dict(
  DESCRIPTOR = _VMIMAGE,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.VmImage)
  ))
_sym_db.RegisterMessage(VmImage)

CreateVmResponse = _reflection.GeneratedProtocolMessageType('CreateVmResponse', (_message.Message,), dict(
  DESCRIPTOR = _CREATEVMRESPONSE,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.CreateVmResponse)
  ))
_sym_db.RegisterMessage(CreateVmResponse)

TestImageRequest = _reflection.GeneratedProtocolMessageType('TestImageRequest', (_message.Message,), dict(

  Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
    DESCRIPTOR = _TESTIMAGEREQUEST_RESULT,
    __module__ = 'chromite.api.image_pb2'
    # @@protoc_insertion_point(class_scope:chromite.api.TestImageRequest.Result)
    ))
  ,
  DESCRIPTOR = _TESTIMAGEREQUEST,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.TestImageRequest)
  ))
_sym_db.RegisterMessage(TestImageRequest)
_sym_db.RegisterMessage(TestImageRequest.Result)

TestImageResult = _reflection.GeneratedProtocolMessageType('TestImageResult', (_message.Message,), dict(
  DESCRIPTOR = _TESTIMAGERESULT,
  __module__ = 'chromite.api.image_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.TestImageResult)
  ))
_sym_db.RegisterMessage(TestImageResult)


DESCRIPTOR._options = None

_IMAGESERVICE = _descriptor.ServiceDescriptor(
  name='ImageService',
  full_name='chromite.api.ImageService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\302\355\032\t\n\005image\020\001'),
  serialized_start=1014,
  serialized_end=1274,
  methods=[
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='chromite.api.ImageService.Create',
    index=0,
    containing_service=None,
    input_type=_CREATEIMAGEREQUEST,
    output_type=_CREATEIMAGERESULT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CreateVm',
    full_name='chromite.api.ImageService.CreateVm',
    index=1,
    containing_service=None,
    input_type=_CREATEVMREQUEST,
    output_type=_CREATEVMRESPONSE,
    serialized_options=_b('\302\355\032\002\020\002'),
  ),
  _descriptor.MethodDescriptor(
    name='Test',
    full_name='chromite.api.ImageService.Test',
    index=2,
    containing_service=None,
    input_type=_TESTIMAGEREQUEST,
    output_type=_TESTIMAGERESULT,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_IMAGESERVICE)

DESCRIPTOR.services_by_name['ImageService'] = _IMAGESERVICE

# @@protoc_insertion_point(module_scope)
