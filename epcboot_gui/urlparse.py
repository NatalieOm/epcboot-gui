"""
URL parser.
Checks whether an entered URL corresponds one of the patterns:
com:\\.\\COMx (for Windows);
com:///dev/ttyUSBx, com:///dev/ttyACMx, com:///dev/ttySx (for Linux);
where x is a number.
"""

import re
import sys
import serial.tools.list_ports


def validate(url: str) -> str:
    """
    Function returns True if url format is correct.
    :param url: url format.
    return: True if url format is correct.
    """

    system = sys.platform
    if system.startswith("win"):
        if not re.match(r"^com:\\\\\.\\COM\d+$", url):
            return 'Incorrect URL format. Must be "com:\\\\.\\COMx"\n'
        com = re.search(r"COM\d+$", url).group(0)
        if com not in [comport.device for comport in
                       serial.tools.list_ports.comports()]:
            return "Not available port\n"
        return ""
    if system.startswith("linux"):
        if not re.match(r"^com:///dev/tty(USB|ACM|S)\d+$", url):
            return ('Incorrect URL format. Must be one of:\n '
                    '"com:///dev/ttyUSBx"\n'
                    ' "com:///dev/ttyACMx"\n'
                    ' "com:///dev/ttySx"\n')
        com = re.search(r"/dev/tty(USB|ACM|S)\d+$", url).group(0)
        if com not in [comport.device for comport in
                       serial.tools.list_ports.comports()]:
            return "Not available port\n"
        return ""
    return "Unknown operating system"
