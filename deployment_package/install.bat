@echo off
echo Installation de SyncMark...
echo.

REM Installation du Native Host
SyncMark.exe --mode install

echo.
echo Installation terminée !
echo.
echo Pour configurer SyncMark, lancez: SyncMark.exe --mode settings
echo Pour utiliser comme Native Host: SyncMark.exe --mode host
echo.
pause
