from .defs import *
from .FirmwareHeader import FirmwareHeader, pack_header
from shutil import copyfileobj

def pack(in_stream, out_stream):
    cur_pos = in_stream.tell()
    size = in_stream.seek(0, 2) - cur_pos
    in_stream.seek(cur_pos)

    header = FirmwareHeader(name="ATK-PTT80P",
                            fw_size=size,
                            encrypt_pos=0xff, # this encrypt pos bypasses encryption completely
                            crc=0, # crc is 0 for now
                            data_len=CHUNK_SIZE,
                            app_addr=1, app_ver=1,  
                            year=2025, month=11, day=30)

    out_stream.write(pack_header(header))
    copyfileobj(in_stream, out_stream)
