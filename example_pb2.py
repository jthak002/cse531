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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rexample.proto\x12\x07\x65xample\"\x7f\n\x0c\x43Transaction\x12\x0f\n\x07\x63ust_id\x18\x01 \x01(\x05\x12\x0f\n\x07tran_id\x18\x02 \x01(\x05\x12\x11\n\tinterface\x18\x03 \x01(\t\x12\r\n\x05money\x18\x04 \x01(\x02\x12\x11\n\tlocaltime\x18\x05 \x01(\x03\x12\x18\n\x10prev_writeset_id\x18\x06 \x01(\t\"j\n\tCResponse\x12\x0f\n\x07\x63ust_id\x18\x01 \x01(\x05\x12\x0f\n\x07tran_id\x18\x02 \x01(\x05\x12\x11\n\tinterface\x18\x03 \x01(\t\x12\x0e\n\x06result\x18\x04 \x01(\t\x12\x18\n\x10\x63urr_writeset_id\x18\x05 \x01(\t\"\x9c\x01\n\x0c\x42Transaction\x12\x0f\n\x07\x63ust_id\x18\x01 \x01(\x05\x12\x0f\n\x07tran_id\x18\x02 \x01(\x05\x12\x15\n\rsrc_branch_id\x18\x03 \x01(\x05\x12\x11\n\tinterface\x18\x04 \x01(\t\x12\r\n\x05money\x18\x05 \x01(\x02\x12\x1c\n\x14src_branch_localtime\x18\x06 \x01(\x03\x12\x13\n\x0bwriteset_id\x18\x07 \x01(\t\"x\n\tBResponse\x12\x0f\n\x07\x63ust_id\x18\x01 \x01(\x05\x12\x0f\n\x07tran_id\x18\x02 \x01(\x05\x12\x11\n\tinterface\x18\x03 \x01(\t\x12\r\n\x05money\x18\x04 \x01(\x02\x12\x0e\n\x06status\x18\x05 \x01(\x08\x12\x17\n\x0f\x61\x63k_writeset_id\x18\x06 \x01(\t\"\x1e\n\nBterminate\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"A\n\x11\x42terminate_Status\x12\x11\n\texit_code\x18\x01 \x01(\x05\x12\x19\n\x11\x65vent_resp_string\x18\x02 \x01(\t2\x81\x03\n\x13\x43ustomerTransaction\x12\x34\n\x05Query\x12\x15.example.CTransaction\x1a\x12.example.CResponse\"\x00\x12\x36\n\x07\x44\x65posit\x12\x15.example.CTransaction\x1a\x12.example.CResponse\"\x00\x12\x37\n\x08Withdraw\x12\x15.example.CTransaction\x1a\x12.example.CResponse\"\x00\x12@\n\x11Propagate_Deposit\x12\x15.example.BTransaction\x1a\x12.example.BResponse\"\x00\x12\x41\n\x12Propagate_Withdraw\x12\x15.example.BTransaction\x1a\x12.example.BResponse\"\x00\x12>\n\tTerminate\x12\x13.example.Bterminate\x1a\x1a.example.Bterminate_Status\"\x00\x42+\n\x18io.grpc.examples.exampleB\x07\x45xampleP\x01\xa2\x02\x03\x45XMb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030io.grpc.examples.exampleB\007ExampleP\001\242\002\003EXM'
  _globals['_CTRANSACTION']._serialized_start=26
  _globals['_CTRANSACTION']._serialized_end=153
  _globals['_CRESPONSE']._serialized_start=155
  _globals['_CRESPONSE']._serialized_end=261
  _globals['_BTRANSACTION']._serialized_start=264
  _globals['_BTRANSACTION']._serialized_end=420
  _globals['_BRESPONSE']._serialized_start=422
  _globals['_BRESPONSE']._serialized_end=542
  _globals['_BTERMINATE']._serialized_start=544
  _globals['_BTERMINATE']._serialized_end=574
  _globals['_BTERMINATE_STATUS']._serialized_start=576
  _globals['_BTERMINATE_STATUS']._serialized_end=641
  _globals['_CUSTOMERTRANSACTION']._serialized_start=644
  _globals['_CUSTOMERTRANSACTION']._serialized_end=1029
# @@protoc_insertion_point(module_scope)
