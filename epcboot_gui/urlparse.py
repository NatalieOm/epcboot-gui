"""URL parser

Checks whether an entered URL corresponds the pattern com:\\.\COMxxx,
where xxx is a number
"""
import sys
SYSTEM = sys.platform


def iscorrect(url: str):
    """Returns True if url format is correct"""
    if SYSTEM.startswith("win"):
        if url[0:11] != r"com:\\.\COM":
            return False
        if not url[11:].isdigit():
            return False
    elif SYSTEM.startswith("linux"):
        if url[0:14] != r"com:///dev/tty":
            return False
        if (url[14:17] != "USB") & (url[14:17] != "ACM"):
            return False
        if not url[17:].isdigit():
            return False
    return True
