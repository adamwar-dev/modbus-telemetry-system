@echo off
echo [INSTALL]

conda env create -f environment.yml -n modbus_telemetry

call develop.bat

echo Done.
pause
