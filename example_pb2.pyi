from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CTransaction(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "money", "localtime", "prev_writeset_id"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    LOCALTIME_FIELD_NUMBER: _ClassVar[int]
    PREV_WRITESET_ID_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    money: float
    localtime: int
    prev_writeset_id: str
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[float] = ..., localtime: _Optional[int] = ..., prev_writeset_id: _Optional[str] = ...) -> None: ...

class CResponse(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "result", "curr_writeset_id"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CURR_WRITESET_ID_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    result: str
    curr_writeset_id: str
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., result: _Optional[str] = ..., curr_writeset_id: _Optional[str] = ...) -> None: ...

class BTransaction(_message.Message):
    __slots__ = ["cust_id", "tran_id", "src_branch_id", "interface", "money", "src_branch_localtime", "writeset_id"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    SRC_BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    SRC_BRANCH_LOCALTIME_FIELD_NUMBER: _ClassVar[int]
    WRITESET_ID_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    src_branch_id: int
    interface: str
    money: float
    src_branch_localtime: int
    writeset_id: str
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., src_branch_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[float] = ..., src_branch_localtime: _Optional[int] = ..., writeset_id: _Optional[str] = ...) -> None: ...

class BResponse(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "money", "status", "ack_writeset_id"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ACK_WRITESET_ID_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    money: float
    status: bool
    ack_writeset_id: str
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[float] = ..., status: bool = ..., ack_writeset_id: _Optional[str] = ...) -> None: ...

class Bterminate(_message.Message):
    __slots__ = ["filename"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class Bterminate_Status(_message.Message):
    __slots__ = ["exit_code", "event_resp_string"]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    EVENT_RESP_STRING_FIELD_NUMBER: _ClassVar[int]
    exit_code: int
    event_resp_string: str
    def __init__(self, exit_code: _Optional[int] = ..., event_resp_string: _Optional[str] = ...) -> None: ...
