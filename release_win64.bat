:: Releases EPCboot_GUI
@echo off
set pyinstaller_arg=%1

if exist venv rd /s/q venv
if exist dist rd /s/q dist
if exist built rd /s/q built
if exist release rd /s/q release
echo Please wait. Unfortunately, sometimes it takes several minutes :(
python -m venv  venv

venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt

venv\Scripts\python -m pip install pyinstaller
venv\Scripts\pyinstaller --clean %pyinstaller_arg% -F --add-binary "epcboot_gui/resources/win64/epcbootlib.dll;resources/win64/" epcboot_gui/epcboot_gui.py

move dist release
if exist build rd /s/q build
if exist dist rd /s/q dist
if exist epcboot_gui.spec del epcboot_gui.spec
cd release