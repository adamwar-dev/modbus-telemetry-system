@echo off
echo [UPDATE]

conda env update -f environment.yml -n modbus_telemetry --prune

call develop.bat

echo Done.
pause
