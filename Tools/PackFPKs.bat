@echo off
cd /d "%~dp0"
set ASSETS_DIR=%~dp0..\Assets
set FPK_IN_DIR=%ASSETS_DIR%\unpacked

PakBuild /I="%FPK_IN_DIR%" /O="%ASSETS_DIR%" /F /S=256 /R=C2C
