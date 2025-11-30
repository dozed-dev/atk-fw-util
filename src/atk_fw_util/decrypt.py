from .FirmwareHeader import parse_header
from .defs import CHUNK_SIZE

def decrypt_chunk(encrypt_pos, bs):
    bs = bytearray(bs)
    if encrypt_pos > len(bs):
        return bytes(bs)
    encrypt_byte = bs[encrypt_pos]
    while encrypt_byte >= len(bs):
        encrypt_byte = encrypt_byte >> 1
    xor_byte = bs[encrypt_byte]
    #print(f"encrypt_pos = {hex(encrypt_pos)}; encrypt_byte = {hex(encrypt_byte)}; xor_byte = {hex(xor_byte)}")
    for i in range(len(bs)):
        if i != encrypt_pos and i != encrypt_byte:
            bs[i] = ((bs[i] ^ xor_byte) - bs[encrypt_pos]) & 0xff # wrap around 8 bit
    return bytes(bs)

def decrypt_firmware(in_stream, out_stream):
    header = parse_header(in_stream.read(0x20))
    while True:
        chunk = in_stream.read(CHUNK_SIZE)
        if not chunk:
            break
        c = decrypt_chunk(header.encrypt_pos, chunk)
        out_stream.write(c)

