pyinstaller --onefile politics.py
rd /s /q __pycache__
rd /s /q build
move dist\politics.exe ..\bin
rd /s /q dist
del politics.spec

pause