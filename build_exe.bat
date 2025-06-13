@echo off
echo [+] Gerando o executável...
pyinstaller ^
  --onefile ^
  --noconsole ^
  --icon=icon.ico ^
  --add-data "icon.ico;." ^
  --add-data "downloaded_files;downloaded_files" ^
  sdown.py
echo Executável criado em: dist\sdown.exe
pause
