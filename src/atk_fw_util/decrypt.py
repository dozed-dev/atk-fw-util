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

def decrypt_firmware(path, decrypted_path):
    with open(path, "rb") as src, open (decrypted_path, "wb") as decrypted:
        header = parse_header(src.read(0x20))
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            c = decrypt_chunk(header.encrypt_pos, chunk)
            decrypted.write(c)

