import struct
from dataclasses import dataclass

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

FORMAT = "<16s B B H H H I H B B"

def parse_header(data: bytes) -> FirmwareHeader:
    fields = struct.unpack(FORMAT, data[:struct.calcsize(FORMAT)])
    name = fields[0].split(b"\x00", 1)[0].decode("ascii", errors="ignore")
    return FirmwareHeader(name, *fields[1:])

