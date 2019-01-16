# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test.proto',
  package='test',
  syntax='proto3',
  serialized_pb=_b('\n\ntest.proto\x12\x04test\x1a\x1bgoogle/protobuf/empty.proto\"\x18\n\x0bGiveRequest\x12\t\n\x01m\x18\x01 \x01(\x03\"\x19\n\x0cTakeResponse\x12\t\n\x01k\x18\x01 \x01(\x03\"+\n\x0b\x45\x63hoRequest\x12\x1c\n\x01r\x18\x01 \x01(\x0b\x32\x11.test.GiveRequest\" \n\x0c\x45\x63hoResponse\x12\x10\n\x08response\x18\x01 \x03(\t2\xa2\x01\n\x04Test\x12\x33\n\x04Give\x12\x11.test.GiveRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x34\n\x04Take\x12\x16.google.protobuf.Empty\x1a\x12.test.TakeResponse\"\x00\x12/\n\x04\x45\x63ho\x12\x11.test.EchoRequest\x1a\x12.test.EchoResponse\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GIVEREQUEST = _descriptor.Descriptor(
  name='GiveRequest',
  full_name='test.GiveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='m', full_name='test.GiveRequest.m', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=73,
)


_TAKERESPONSE = _descriptor.Descriptor(
  name='TakeResponse',
  full_name='test.TakeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='k', full_name='test.TakeResponse.k', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=100,
)


_ECHOREQUEST = _descriptor.Descriptor(
  name='EchoRequest',
  full_name='test.EchoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='r', full_name='test.EchoRequest.r', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=145,
)


_ECHORESPONSE = _descriptor.Descriptor(
  name='EchoResponse',
  full_name='test.EchoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='test.EchoResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=179,
)

_ECHOREQUEST.fields_by_name['r'].message_type = _GIVEREQUEST
DESCRIPTOR.message_types_by_name['GiveRequest'] = _GIVEREQUEST
DESCRIPTOR.message_types_by_name['TakeResponse'] = _TAKERESPONSE
DESCRIPTOR.message_types_by_name['EchoRequest'] = _ECHOREQUEST
DESCRIPTOR.message_types_by_name['EchoResponse'] = _ECHORESPONSE

GiveRequest = _reflection.GeneratedProtocolMessageType('GiveRequest', (_message.Message,), dict(
  DESCRIPTOR = _GIVEREQUEST,
  __module__ = 'test_pb2'
  # @@protoc_insertion_point(class_scope:test.GiveRequest)
  ))
_sym_db.RegisterMessage(GiveRequest)

TakeResponse = _reflection.GeneratedProtocolMessageType('TakeResponse', (_message.Message,), dict(
  DESCRIPTOR = _TAKERESPONSE,
  __module__ = 'test_pb2'
  # @@protoc_insertion_point(class_scope:test.TakeResponse)
  ))
_sym_db.RegisterMessage(TakeResponse)

EchoRequest = _reflection.GeneratedProtocolMessageType('EchoRequest', (_message.Message,), dict(
  DESCRIPTOR = _ECHOREQUEST,
  __module__ = 'test_pb2'
  # @@protoc_insertion_point(class_scope:test.EchoRequest)
  ))
_sym_db.RegisterMessage(EchoRequest)

EchoResponse = _reflection.GeneratedProtocolMessageType('EchoResponse', (_message.Message,), dict(
  DESCRIPTOR = _ECHORESPONSE,
  __module__ = 'test_pb2'
  # @@protoc_insertion_point(class_scope:test.EchoResponse)
  ))
_sym_db.RegisterMessage(EchoResponse)


# @@protoc_insertion_point(module_scope)