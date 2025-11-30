import struct
from dataclasses import dataclass
from .defs import HEADER_FORMAT

@dataclass
class FirmwareHeader:
    name: str
    data_len: int
    encrypt_pos: int
    app_addr: int
    app_ver: int
    crc: int
    fw_size: int
    year: int
    month: int
    day: int

def parse_header(data: bytes) -> FirmwareHeader:
    fields = struct.unpack(HEADER_FORMAT, data[:struct.calcsize(FORMAT)])
    name = fields[0].split(b"\x00", 1)[0].decode("ascii", errors="ignore")
    return FirmwareHeader(name, *fields[1:])

