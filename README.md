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

Build binary release on linux:
```bash
source release.sh
```
Windows:
```bash
.\release_win64.bat
```

NOTE. On linux machine we recommend to stop(or remove) the modemmanager. The modemmanager interferes with our 
bootloader.
```bash
sudo systemctl stop ModemManager.service
```

#### For developer

This repository is configured to build automatically. Find build artifacts here 
https://github.com/EPC-MSU/epcboot-gui/actions?query=workflow%3ABuild Use them when creating a release
