# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rexample.proto\x12\x07\x65xample\"R\n\x0c\x43Transaction\x12\x0f\n\x07\x63ust_id\x18\x01 \x01(\x05\x12\x0f\n\x07tran_id\x18\x02 \x01(\x05\x12\x11\n\tinterface\x18\x03 \x01(\t\x12\r\n\x05money\x18\x04 \x01(\x02\"P\n\tCResponse\x12\x0f\n\x07\x63ust_id\x18\x01 \x01(\x05\x12\x0f\n\x07tran_id\x18\x02 \x01(\x05\x12\x11\n\tinterface\x18\x03 \x01(\t\x12\x0e\n\x06result\x18\x04 \x01(\t2`\n\x13\x43ustomerTransaction\x12I\n\x1aPerformCustomerTransaction\x12\x15.example.CTransaction\x1a\x12.example.CResponse\"\x00\x42+\n\x18io.grpc.examples.exampleB\x07\x45xampleP\x01\xa2\x02\x03\x45XMb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030io.grpc.examples.exampleB\007ExampleP\001\242\002\003EXM'
  _globals['_CTRANSACTION']._serialized_start=26
  _globals['_CTRANSACTION']._serialized_end=108
  _globals['_CRESPONSE']._serialized_start=110
  _globals['_CRESPONSE']._serialized_end=190
  _globals['_CUSTOMERTRANSACTION']._serialized_start=192
  _globals['_CUSTOMERTRANSACTION']._serialized_end=288
# @@protoc_insertion_point(module_scope)