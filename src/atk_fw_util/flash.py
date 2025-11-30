#!/usr/bin/env python3

import usb.core
import usb.util
from .defs import CHUNK_SIZE, HEADER_SIZE

def calc_crc16(data):
  crc = 0xffff
  for b in data:
      crc ^= b
      for _ in range(8):
          if crc & 1:
              crc = (crc >> 1) ^ 0xa001
          else:
              crc >>= 1
  return crc & 0xffff

def build_packet(device_addr, function, sequence, data):
  if len(data) > CHUNK_SIZE:
    raise ValueError("len(data) must be <= " + CHUNK_SIZE)
  packet = [device_addr, function, sequence, len(data)] + list(data)
  crc = calc_crc16(packet)
  packet += [crc & 0xff, crc >> 8]
  return bytes(packet + [0] * (64 - len(packet)))

TARGET_DEVICE_ADDR = 0xfb
SOURCE_DEVICE_ADDR = 0xfa

FUNCTION_GET_DEVICE_INFO = 0x10
FUNCTION_SET_FIRMWARE_INFO = 0x11
FUNCTION_START_FIRMWARE_DATA = 0x12
FUNCTION_FIRMWARE_DATA = 0x13
FUNCTION_END_FIRMWARE_DATA = 0x14
FUNCTION_JUMP_TO_BOOTLOADER = 0x15

USB_TIMEOUT = 1000 # ms

def parse_packet(packet):
  if len(packet) < 6:
    raise ValueError("len(packet) must be >= 6")
  device_addr = packet[0]
  function = packet[1]
  sequence = packet[2]
  data_length = packet[3]
  data = packet[4:4 + data_length]
  crc = packet[4 + data_length] | (packet[4 + data_length + 1] << 8)
  calculated_crc = calc_crc16([device_addr, function, sequence, data_length] + list(data))
  if crc != calculated_crc:
    raise ValueError(f"wrong crc: {crc} != {calculated_crc}")
  return (device_addr, function, sequence, data)

def do_request_response(eps, device_addr, function, sequence, data):
  request_packet = build_packet(device_addr, function, sequence, data)
  eps[1].write(request_packet, timeout=USB_TIMEOUT)
  raw_response = eps[0].read(64, timeout=USB_TIMEOUT)
  return parse_packet(raw_response)

VID = 0x413D
PID = 0x2107
ENDPOINT_READ = 0x81
ENDPOINT_WRITE = 0x01

def get_usb_endpoints():
  dev = usb.core.find(idVendor=VID, idProduct=PID)
  if dev is None:
    raise ValueError('device not found')

  dev.reset()
  dev.detach_kernel_driver(0)
  dev.set_configuration()
  cfg = dev.get_active_configuration()
  intf = cfg[(0,0)]
  ep_r = usb.util.find_descriptor(intf, custom_match = lambda e: e.bEndpointAddress == ENDPOINT_READ)
  ep_w = usb.util.find_descriptor(intf, custom_match = lambda e: e.bEndpointAddress == ENDPOINT_WRITE)
  endpoints = (ep_r, ep_w)
  return endpoints

def flash(firmware):
  endpoints = get_usb_endpoints()
  header = firmware.read(HEADER_SIZE)

  print(do_request_response(endpoints, TARGET_DEVICE_ADDR, FUNCTION_GET_DEVICE_INFO, 0, []))
  print(do_request_response(endpoints, TARGET_DEVICE_ADDR, FUNCTION_SET_FIRMWARE_INFO, 0, header))
  print(do_request_response(endpoints, TARGET_DEVICE_ADDR, FUNCTION_START_FIRMWARE_DATA, 0, []))

  sequence = 0
  while True:
    chunk = firmware.read(CHUNK_SIZE)
    if not chunk:
      break
    print(do_request_response(endpoints, TARGET_DEVICE_ADDR, FUNCTION_FIRMWARE_DATA, sequence, chunk))
    sequence += 1
    sequence %= 256

  print(do_request_response(endpoints, TARGET_DEVICE_ADDR, FUNCTION_END_FIRMWARE_DATA, 0, []))
