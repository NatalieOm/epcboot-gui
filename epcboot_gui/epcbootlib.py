"""Bindings for epcbootlib.dll"""
from ctypes import WinDLL, CDLL, c_char_p, c_int, c_uint
import struct
from platform import system

# Loading library accordingly to system kind
os_kind = system().lower()
if os_kind == "windows":
    if 8 * struct.calcsize("P") == 32:
        epcbootlib = WinDLL("resources\\win32\\epcbootlib.dll")
        print("Detected system is Win32")
    else:
        epcbootlib = WinDLL("resources\\win64\\epcbootlib.dll")
        print("Detected system is Win64")
elif os_kind == "freebsd" or "linux" in os_kind:
    epcbootlib = CDLL("resources/linux/epcbootlib.so")
    print("Detected system is Linux")
else:
    raise RuntimeError("Unexpected OS")


# Binding functions:
# Their returnable results:
# -1  - result_error
#  0  - result_ok

# Arguments of urpc_firmware_update():
#   1. URL: char_p
#   2. firmware: char_p
#   3. firmware length: c_int
# Description: It updates firmware
urpc_firmware_update = epcbootlib.urpc_firmware_update
urpc_firmware_update.restype = c_int
urpc_firmware_update.argtypes = [c_char_p, c_char_p, c_int]

# Arguments of urpc_write_key():
#   1. URL: char_p
#   2. cryptography key: char_p
# Description: It sets cryptography key
urpc_write_key = epcbootlib.urpc_write_key
urpc_write_key.restype = c_int
urpc_write_key.argtypes = [c_char_p, c_char_p]

# Arguments of urpc_write_ident():
#   1. URL: char_p
#   2. cryptography key: char_p
#   3. serial number: c_int
#   4. version: c_char_p
# Description: It sets crypto key, serial number and version
urpc_write_ident = epcbootlib.urpc_write_ident
urpc_write_ident.restype = c_int
urpc_write_ident.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]
