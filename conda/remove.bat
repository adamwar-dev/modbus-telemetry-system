@echo off
echo [REMOVE]

conda deactivate
conda env remove -n modbus_telemetry -y

echo Done.
pause
