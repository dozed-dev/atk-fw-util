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
    out = args.output or _default_output(args.input, ".bin")
    with _stream(args.input, "rb") as fin, _stream(out, "wb") as fout:
        decrypt_firmware(fin, fout)

def cmd_pack(args):
    out = args.output or _default_output(args.input, ".atk")
    with _stream(args.input, "rb") as fin, _stream(out, "wb") as fout:
        pack(fin, fout)

def cmd_flash(args):
    with _stream(args.input, "rb") as fin:
        flash(fin)

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    c_dec = sub.add_parser("decrypt")
    c_dec.add_argument("input")
    c_dec.add_argument("output", nargs="?")
    c_dec.set_defaults(func=cmd_decrypt)

    c_pack = sub.add_parser("pack-atk")
    c_pack.add_argument("input")
    c_pack.add_argument("output", nargs="?")
    c_pack.set_defaults(func=cmd_pack)

    c_flash = sub.add_parser("flash")
    c_flash.add_argument("input")
    c_flash.set_defaults(func=cmd_flash)

    args = parser.parse_args()
    args.func(args)
