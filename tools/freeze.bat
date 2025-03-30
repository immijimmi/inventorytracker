:: Freezes the project into a .exe file inside ..\dist
:: Generates a vestigial ..\build folder which should be deleted after execution
:: Installs a venv a the ..\venv subfolder if none exists at this location already
:: Automatically ensures any dependencies are installed before running

cd ..

python -m venv ./venv
venv\Scripts\python -m pip install -r requirements.txt
venv\Scripts\python -m pip install pyinstaller~=6.2.0

venv\Scripts\python -m PyInstaller --onefile main.pyw

del main.spec
pause
