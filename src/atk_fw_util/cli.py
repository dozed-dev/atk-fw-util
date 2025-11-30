import sys
import argparse
from pathlib import Path

from .decrypt import decrypt_firmware
from .flash import flash
from .pack import pack

def _stream(path, mode):
    if path == "-":
        return sys.stdin.buffer if "r" in mode else sys.stdout.buffer
    return open(path, mode)

def _default_output(input_path, new_ext):
    p = Path(input_path)
    return str(p.with_suffix(new_ext))

def cmd_decrypt(args):
    out = args.output or _default_output(args.atk_firmware, ".bin")
    with _stream(args.atk_firmware, "rb") as fin, _stream(out, "wb") as fout:
        decrypt_firmware(fin, fout)

def cmd_pack(args):
    out = args.atk_output or _default_output(args.raw_binary, ".atk")
    with _stream(args.raw_binary, "rb") as fin, _stream(out, "wb") as fout:
        pack(fin, fout)

def cmd_flash(args):
    with _stream(args.firmware_file, "rb") as fin:
        flash(fin)

def main():
    parser = argparse.ArgumentParser(
        prog='atk-fw-util',
        description='A collection of utils for working with Alientek firmware')

    sub = parser.add_subparsers(dest="cmd", required=True)

    c_dec = sub.add_parser("decrypt", help="Decrypt .atk firmware")
    c_dec.add_argument("atk_firmware", help="Path to atk firmware to decrypt")
    c_dec.add_argument("output", nargs="?", help="Path to output file")
    c_dec.set_defaults(func=cmd_decrypt)

    c_pack = sub.add_parser("pack-atk", help="Convert raw binary to .atk file for flashing over usb")
    c_pack.add_argument("raw_binary", help="Path to raw binary to convert to .atk")
    c_pack.add_argument("atk_output", nargs="?")
    c_pack.set_defaults(func=cmd_pack)

    c_flash = sub.add_parser("flash", help="Flash .atk over usb")
    c_flash.add_argument("firmware_file", help="Path to firmware to flash")
    c_flash.set_defaults(func=cmd_flash)

    args = parser.parse_args()
    args.func(args)
