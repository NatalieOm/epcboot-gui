# EPCboot GUI 

EPCboot GUI allows you to:
* browse firmware on PC and load it to controller
* browse key file (*.txt) and load it to controller (developer only)
* update serial and version (developer only)

Run (python):
```bash
python -m pip install -r requirements.txt
cd epcboot_gui
python epcboot_gui.py
```

Linux:
You should delete modemmanager! It interferes in the connection
For it type in terminal: sudo apt-get remove --auto-remove modemmanager
