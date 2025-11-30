#!/usr/bin/env python3
from .decrypt import decrypt_chunk, decrypt_firmware
from .flash import flash
from .cli import main

#def main():
    #decrypt_firmware('./T80P_v303_app_ch.atk', './T80P_v303_app_ch.bin')
    #flash('./T80P_v303_app_ch.atk')

if __name__ == "__main__":
    main()
    
