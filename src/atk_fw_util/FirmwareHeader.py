import struct
from dataclasses import dataclass, astuple

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

HEADER_FORMAT = "<16s B B H H H I H B B"

def parse_header(data: bytes) -> FirmwareHeader:
    fields = struct.unpack(HEADER_FORMAT, data[:struct.calcsize(HEADER_FORMAT)])
    name = fields[0].split(b"\x00", 1)[0].decode("ascii", errors="ignore")
    return FirmwareHeader(name, *fields[1:])

def pack_header(header: FirmwareHeader) -> bytes:
    s = header.name.encode('utf-8')
    return struct.pack(HEADER_FORMAT, s, *(astuple(header)[1:]))
