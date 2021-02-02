"""This .py file offers GUI for EPCboot

It allows:
    * browse firmware on PC and load it to controller
    * browse key file (*.txt) and load it to controller (developer only)
    * update serial and version (developer only)
"""
from tkinter import scrolledtext
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import ctypes
import epcbootlib
import urlparse
import argparse
import sys
import ntpath


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--method",
                    choices=("dev", "cust"),
                    help="Choosing method: dev or cust "
                         "(developer or customer)")
args = parser.parse_args()


# event handlers
def com_chosen(event):
    """Sets URL for Windows"""
    import serial
    global URL
    try:
        test_port = serial.Serial(port=URL.get())
        test_port.close()
    except serial.SerialException:
        log.insert(tk.END, "Something is wrong! If you use Linux, open epcboot_gui"
                   " with root.\n"
                   "In case of using Windows, make sure that the device is not"
                   " used by another program.\n")
    system = sys.platform
    if system.startswith("win"):
        URL.set(r"com:\\.\{}".format(URL.get()))
    elif system.startswith("linux"):
        URL.set(r"com://{}".format(URL.get()))
    if upd_button.state() == ():
        # in case of enabled upd_button, method .state() returns empty tuple
        upd_button.focus()
    else:
        firmware_browse_button.focus()
    log.insert(tk.END, "{} is chosen!\n".format(combox.get()))


def _upd_combox():
    """Updates COM list"""
    combox.config(values=[comport.device
                          for comport in serial.tools.list_ports.comports()])
def clean_log():
    """Cleans log"""
    log.delete('1.0', tk.END)

def firmware_browse():
    """Opens file dialog

    We going to read binary files (.cod). So .encode() isn't needed
    """
    global URL
    global FIRM_PATH
    global FIRMWARE
    main_win.firmware = filedialog.askopenfile(
        mode="rb",
        initialdir="/",
        title="Select firmware",
        filetypes=(("C/C++ Code Listing", "*.cod"), ("all files", "*.*")))
    if not isinstance(main_win.firmware, type(None)):
        # file was opened
        FIRM_PATH.set(main_win.firmware.name)
        FIRMWARE = main_win.firmware.read()
        upd_button.config(state=tk.NORMAL)
    else:
        # file wasn't open
        # probably you open dialog and close it without choosing any file
        pass
    if URL.get() == "":
        # in case of enabled upd_button method .state() returns empty tuple
        combox.focus()
    else:
        upd_button.focus()
    main_win.firmware.close()


def firmware_upd():
    """Updates firmware"""
    global URL
    global FIRMWARE
    global FIRM_PATH
    if URL.get() == "":
        log.insert(tk.END, "You must specify device URL.\n")
        return
    if FIRMWARE == "":
        log.insert(tk.END, "You must specify firmware file.\n")
        return
    if not urlparse.iscorrect(URL.get()):
        log.insert(tk.END, r"Incorrect URL format. Must be one of:" + "\n"
                           r' "com:\\.\COMx"' + "\n"
                           r' "com:///dev/ttyUSBx"' + "\n"
                           r' "com:///dev/ttyACMx"' + "\n")
        return
    # the statement below is necessary to work with url as C char*
    url = ctypes.create_string_buffer(URL.get().encode())
    log.insert(tk.END, "Starting firmware update. Port: {}. Firmware file: {}\n".format(URL.get(), ntpath.basename(FIRM_PATH.get())))
    log.insert(tk.END, "Please wait\n")
    main_win.update()
    res = epcbootlib.urpc_firmware_update(url, FIRMWARE, len(FIRMWARE))
    if res == 0:
        log.insert(tk.END, "Ok\n")
    else:
        log.insert(tk.END, "Fail\n")


def key_browse():
    """Opens file dialog

    Key must be .txt file
    """
    global KEY
    main_win.key_file = filedialog.askopenfile(
        mode="r",
        initialdir="/",
        title="Select key",
        filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    if not isinstance(main_win.key_file, type(None)):
        # file was opened
        KEY.set(main_win.key_file.read().rstrip())
    else:
        # file wasn't open
        # probably you open dialog and close it without choosing any file
        pass
    main_win.key_file.close()


def key_set():
    """Sets cryptographic key"""
    global URL
    global KEY
    if URL.get() == "":
        log.insert(tk.END, "You must specify device URL.\n")
        return
    if KEY.get() == "":
        log.insert(tk.END, "You must specify key.\n")
        return
    if not urlparse.iscorrect(URL.get()):
        log.insert(tk.END, r"Incorrect URL format. Must be one of:" + "\n"
                           r' "com:\\.\COMX"' + "\n"
                           r' "com:///dev/tty/ttyUSBX"' + "\n"
                           r' "com:///dev/tty/ttyACMX"' + "\n")
        return
    if not (URL.get() in ["com:\\\\.\\" + comport.device
                          for comport in serial.tools.list_ports.comports()]):
        log.insert(tk.END, "Not available port\n")
        return
    # the statement below is necessary to work with url as C char*
    url = ctypes.create_string_buffer(URL.get().encode())
    # the statement below is necessary to work with key as C char*
    key = ctypes.create_string_buffer(KEY.get().encode())
    log.insert(tk.END, "Starting key setting. Port: {}\n".format(URL.get()))
    log.insert(tk.END, "Please wait\n")
    main_win.update()
    res = epcbootlib.urpc_write_key(url, key)
    if res == 0:
        log.insert(tk.END, "Ok\n")
    else:
        log.insert(tk.END, "Fail\n")


def ident_and_key_set():
    """Sets serial number, hardware version and key"""
    global URL
    global KEY
    if URL.get() == "":
        log.insert(tk.END, "You must specify device URL.\n")
        return
    if KEY.get() == "":
        log.insert(tk.END, "You must specify key.\n")
        return
    if serial_entry.get() == "xxx":
        log.insert(tk.END, "You must specify serial number.\n")
        return
    if version_entry.get() == "x.x.x":
        log.insert(tk.END, "You must specify version.\n")
        return
    if not urlparse.iscorrect(URL.get()):
        log.insert(tk.END, r"Incorrect URL format. Must be one of:" + "\n"
                           r' "com:\\.\COMX"' + "\n"
                           r' "com:///dev/ttyUSBX"' + "\n"
                           r' "com:///dev/ttyACMX"' + "\n")
        return
    # Checking serial and version format
    if not serial_entry.validate():
        return
    if not version_entry.validate():
        return
    # the statement below is necessary to work with url as C char*
    url = ctypes.create_string_buffer(URL.get().encode())
    key = ctypes.create_string_buffer(KEY.get().encode())
    version = ctypes.create_string_buffer(version_entry.get().encode())
    log.insert(tk.END, "Starting identificator and key setting."
                       " Port: {}\n Serial number: {}\n Hardware version: {}\n".format(URL.get(), serial_entry.get(), version_entry.get()))
    log.insert(tk.END, "Please wait\n")
    main_win.update()
    res = epcbootlib.urpc_write_ident(url, key,
                                      int(serial_entry.get()), version)
    if res == 0:
        log.insert(tk.END, "Ok\n")
    else:
        log.insert(tk.END, "Fail\n")


def _serial_validation(content, trigger_type):
    if content == "xxx" and trigger_type == "focusin":
        # clears the hint
        serial_entry.delete(0, tk.END)
        return tk.TRUE
    if content == "xxx" and trigger_type == "focusout":
        # just leave the entry
        return tk.TRUE
    if content == "":
        serial_entry.config(font=("Calibri Italic", 10),
                            foreground="grey")
        if trigger_type == "focusout":
            serial_entry.delete(0, tk.END)
            serial_entry.insert(tk.END, "xxx")
        return tk.TRUE
    if not content.isdigit():
        log.insert(tk.END, "Serial number must be a number!\n")
        return tk.FALSE
    if int(content) > 512:
        log.insert(tk.END, "Serial number must be less than 512!\n")
        return tk.FALSE
    serial_entry.config(font=("Calibri", 10), foreground="green")
    return tk.TRUE


def _version_validation(content, trigger_type="focusout"):
    """Returns tk.TRUE if version format is correct"""
    if content == "x.x.x" and trigger_type == "focusin":
        # clears the hint
        version_entry.delete(0, tk.END)
        return tk.TRUE
    if content != "x.x.x" and trigger_type == "focusin":
        # just enter the entry
        return tk.TRUE
    print(content)
    if content == "":
        if trigger_type == "focusout":
            # sets the hint
            version_entry.config(font=("Calibri Italic", 10), foreground="grey")
            version_entry.insert(tk.END, "x.x.x")
        return tk.TRUE
    # the .find(".", x) returns -1 if "." is not found
    first_dot_index = content.find(".", 0)
    second_dot_index = content.find(".", first_dot_index + 1)
    third_dot_index = content.find(".", second_dot_index + 1)

    # Consider -1 as dot absence
    if first_dot_index == -1:                                 #
        second_dot_index, third_dot_index = -1, -1            # dot indices
    if second_dot_index == -1:                                # correction
        third_dot_index = -1                                  #

    if third_dot_index != -1:
        # there cannot be three or more dots
        return tk.FALSE

    major = content[0:first_dot_index]
    minor = content[first_dot_index + 1:second_dot_index]
    patch = content[second_dot_index + 1:]

    if second_dot_index == -1:                                  #
        patch = ""                                              #
        minor = content[first_dot_index + 1:]                   # minor correction
    if first_dot_index == -1:                                   #
        patch = ""                                              #
        minor = ""                                              #
        major = content[second_dot_index + 1:]                  # major correction

    if not major.isdigit():
        log.insert(tk.END, "MAJOR should be a number!\n")
        return tk.FALSE
    if not minor.isdigit():
        if (minor == "" and second_dot_index == -1 and
           trigger_type != "focusout"):
            version_entry.config(font=("Calibri", 10), foreground="green")
            return tk.TRUE
        log.insert(tk.END, "MINOR should be a number!\n")
        return tk.FALSE
    if patch != "" and not patch.isdigit():
        log.insert(tk.END, "PATCH should be a number!\n")
        return tk.FALSE
    version_entry.config(font=("Calibri", 10), foreground="green")
    return tk.TRUE


def validation_command(widget_name, content, trigger_type):
    """Checks entry format and changes font

    If format is ok: green Calibri 10
    If format uncorrect: red Calibri 10
    If empty: sets hint, grey Calibri Italic 10
    """
    instance = main_win.nametowidget(widget_name)  # getting certain entry

    if instance is serial_entry:
        if _serial_validation(content, trigger_type):
            return tk.TRUE
    if instance is version_entry:
        if _version_validation(content, trigger_type):
            return tk.TRUE
    return tk.FALSE


def invalid_command(widget_name, content):
    """Starts if validation commands return False"""
    instance = main_win.nametowidget(widget_name)  # getting certain entry
    instance.delete(0, tk.END)
    instance.insert(tk.END, content)
    instance.config(foreground="red")


# Creating main window
main_win = tk.Tk()
# Setting window geometry and title
win_geometry = ("500", "383")  # <- SHOULD CHANGE IT!!!
linux_geometry = ("640", "412")
if sys.platform.startswith("win"):
    main_win.geometry(win_geometry[0] + "x" + win_geometry[1])
elif sys.platform.startswith("linux"):
    main_win.geometry(linux_geometry[0] + "x" + linux_geometry[1])
else:
    print("Unknown system!")
main_win.title("EPCboot")
main_win.resizable(tk.FALSE, tk.FALSE)  # disabling resizability

FIRMWARE = ""            # string containing firmware
URL = tk.StringVar()        # URL of port
FIRM_PATH = tk.StringVar()  # path to firmware
# Used special tk.StringVar type to supply opportunity to link
# 1. URL        and  combox
# 2. FIRM_PATH  and  firmware_entry
# (see below)

# log_frame
log_frame = ttk.Labelframe(main_win, text="Log")
log = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
log.edit_modified(0)
log_button_frame = ttk.LabelFrame(log_frame)
log_button = ttk.Button(log_button_frame, text="Clean log", command=clean_log)
log_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
log_frame.pack(expand=tk.TRUE, side=tk.BOTTOM, fill=tk.BOTH)
log.pack(expand=tk.TRUE, side=tk.BOTTOM, fill=tk.BOTH)
log_button.pack(side=tk.RIGHT)

def on_modification(event=None):
    log.see(tk.END)
    log.edit_modified(0)

log.bind("<<Modified>>", on_modification)

firmware_tab = ttk.Frame(main_win)  # ttk.Frame(notebook)
developer_tab = ttk.Frame(main_win)  # ttk.Frame(notebook)

# firmware tab:
com_frame = ttk.Labelframe(firmware_tab, text="COM settings")
com_label = ttk.Label(com_frame, text="COM port:")
combox = ttk.Combobox(com_frame, postcommand=_upd_combox, width=15, textvariable=URL)
combox.bind("<<ComboboxSelected>>", com_chosen)
com_hint = ttk.Label(com_frame, font=("Calibri Italic", 10))
if sys.platform.startswith("win"):
    com_hint.config(text=r"Input format:  com:\\.\COMx", foreground="grey")
else:
    com_hint.config(text=r"Input format:  com://dev/ttyACMx or "
                         r"com://dev/ttyCOMx", foreground="grey")
firmware_frame = ttk.Labelframe(firmware_tab, text="Firmware update")
firmware_label = ttk.Label(firmware_frame, text="Firmware:")
firmware_entry = ttk.Entry(firmware_frame, textvariable=FIRM_PATH, width=17)
firmware_browse_button = ttk.Button(firmware_frame, text="Browse...", width=10, command=firmware_browse)
upd_button = ttk.Button(firmware_tab, text="Update firmware", state=tk.DISABLED, width=20, command=firmware_upd)

com_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3, ipady=6)
firmware_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3, ipady=5)
com_label.pack(side=tk.LEFT)
combox.pack(side=tk.LEFT, padx=10)
com_hint.pack(side=tk.LEFT)
firmware_label.pack(side=tk.LEFT)
firmware_entry.pack(expand=tk.TRUE, side=tk.LEFT, fill=tk.X, padx=14)
firmware_browse_button.pack(side=tk.LEFT, padx=5)
upd_button.pack(side=tk.TOP, pady=0)
# end of firmware tab

# developer tab:
KEY = tk.StringVar()  # cryptographic key

key_frame = ttk.Labelframe(developer_tab, text="Key")
ident_frame = ttk.Labelframe(developer_tab, text="Identification")

key_label = ttk.Label(key_frame, text="Key:")                #
key_entry = ttk.Entry(key_frame, textvariable=KEY)           # Working with
set_key_button = ttk.Button(key_frame, text="  Set key  ",   # key frame
                            command=key_set)                 #
key_browse_button = ttk.Button(key_frame, text="Browse...",  #
                               command=key_browse)           #

left_frame = ttk.Frame(ident_frame)                            #
right_frame = ttk.Frame(ident_frame)                           # Working with
left_frame.pack(expand=tk.TRUE, side=tk.LEFT, fill=tk.BOTH)         # developer frame
right_frame.pack(expand=tk.TRUE, side=tk.RIGHT, fill=tk.BOTH)       #
serial_frame = ttk.Frame(left_frame)                           #
version_frame = ttk.Frame(left_frame)                          #
serial_label = ttk.Label(serial_frame, text="Serial number:")  #
serial_entry = ttk.Entry(serial_frame, foreground="grey",      #
                         font=("Calibri Italic", 10))          #
version_label = ttk.Label(version_frame, text="HW version:")   #
version_entry = ttk.Entry(version_frame, foreground="grey",    #
                          font=("Calibri Italic", 10))         #
set_ident_button = ttk.Button(right_frame,                     #
                              text="Set serial and hardware version",  #
                              width=30,                        #
                              command=ident_and_key_set)       #
set_ident_button.pack(expand=tk.TRUE)                         #

# initializing serial_entry
serial_entry.insert(tk.END, "xxx")
# initializing version_entry
version_entry.insert(tk.END, "x.x.x")

# Setting validation to entries (serial_entry and version_entry)
vcmd = main_win.register(validation_command)
ivcmd = main_win.register(invalid_command)
serial_entry.config(validatecommand=(vcmd, "%W", "%P", "%V"),
                    invalidcommand=(ivcmd, "%W", "%P"),
                    validate="all")
version_entry.config(validatecommand=(vcmd, "%W", "%P", "%V"),
                     invalidcommand=(ivcmd, "%W", "%P"),
                     validate="all")
# end of developer tab

# creating collapse button
DEV_STATE = False  # developer tab state


def collapse():
    """This function collapses or expands developer tab"""

    global DEV_STATE
    if DEV_STATE:
        separator.pack(expand=tk.TRUE, side=tk.RIGHT, fill=tk.X, padx=5)
        developer_tab.pack_forget()
        DEV_STATE = False
        if sys.platform.startswith("win"):
            main_win.geometry(win_geometry[0] + "x" + win_geometry[1])
        elif sys.platform.startswith("linux"):
            main_win.geometry(linux_geometry[0] + "x" + linux_geometry[1])
    else:
        separator.pack_forget()
        developer_tab.pack(expand=tk.TRUE, side=tk.TOP, fill=tk.BOTH)
        DEV_STATE = True
        if sys.platform.startswith("win"):
            main_win.geometry(win_geometry[0] + "x" + "530")
        elif sys.platform.startswith("linux"):
            main_win.geometry(linux_geometry[0] + "x" + "568")


collapse_frame = ttk.Frame(main_win)
collapse_button = ttk.Button(collapse_frame, text="Developer mode", command=collapse)
separator = ttk.Separator(collapse_frame, orient="horizontal")
collapse_button.pack(side=tk.LEFT, padx=5)
separator.pack(expand=tk.TRUE, side=tk.RIGHT, fill=tk.X, padx=5)
# end of collapse button

firmware_tab.pack(expand=tk.TRUE, side=tk.TOP, fill=tk.BOTH)
collapse_frame.pack(expand=tk.TRUE, side=tk.TOP, fill=tk.X)
key_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3, ipady=4)
ident_frame.pack(expand=tk.TRUE, side=tk.TOP, padx=5, fill=tk.BOTH, pady=3, ipady=4)
serial_frame.pack(side=tk.TOP, fill=tk.X, pady=7)
version_frame.pack(side=tk.TOP, fill=tk.X)
key_label.pack(side=tk.LEFT)
key_entry.pack(expand=tk.TRUE, side=tk.LEFT, fill=tk.X, padx=15)
set_key_button.pack(side=tk.RIGHT, padx=4)
key_browse_button.pack(side=tk.RIGHT)
serial_label.pack(expand=tk.FALSE, side=tk.LEFT)
serial_entry.pack(side=tk.LEFT, padx=14)
version_label.pack(side=tk.LEFT)
version_entry.pack(side=tk.LEFT, padx=26)
set_ident_button.pack(side=tk.TOP)

tk.mainloop()
