from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CTransaction(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "money"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    money: float
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[float] = ...) -> None: ...

class CResponse(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "result"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    result: str
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., result: _Optional[str] = ...) -> None: ...

class BTransaction(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "money"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    money: float
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[float] = ...) -> None: ...

class BResponse(_message.Message):
    __slots__ = ["cust_id", "tran_id", "interface", "money", "status"]
    CUST_ID_FIELD_NUMBER: _ClassVar[int]
    TRAN_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cust_id: int
    tran_id: int
    interface: str
    money: float
    status: bool
    def __init__(self, cust_id: _Optional[int] = ..., tran_id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[float] = ..., status: bool = ...) -> None: ...
