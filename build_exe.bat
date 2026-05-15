@echo off
setlocal
cd /d %~dp0

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install customtkinter pyinstaller
python -m PyInstaller aggregator.spec --clean --noconfirm

echo.
echo 构建完成：dist\aggregator\aggregator.exe
endlocal
