# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: constants.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='constants.proto',
  package='com.gftchina.common.calcProtocol',
  serialized_pb=_b('\n\x0f\x63onstants.proto\x12 com.gftchina.common.calcProtocol\"\x1e\n\tDirtyType\x12\x11\n\tdirtyType\x18\x01 \x02(\x05')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DIRTYTYPE = _descriptor.Descriptor(
  name='DirtyType',
  full_name='com.gftchina.common.calcProtocol.DirtyType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dirtyType', full_name='com.gftchina.common.calcProtocol.DirtyType.dirtyType', index=0,
      number=1, type=5, cpp_type=1, label=2,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=83,
)

DESCRIPTOR.message_types_by_name['DirtyType'] = _DIRTYTYPE

DirtyType = _reflection.GeneratedProtocolMessageType('DirtyType', (_message.Message,), dict(
  DESCRIPTOR = _DIRTYTYPE,
  __module__ = 'constants_pb2'
  # @@protoc_insertion_point(class_scope:com.gftchina.common.calcProtocol.DirtyType)
  ))
_sym_db.RegisterMessage(DirtyType)


# @@protoc_insertion_point(module_scope)