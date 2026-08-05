import asyncio
from pymodbus.server import ModbusTcpServer
from pymodbus.datastore import (
    ModbusServerContext,
    ModbusDeviceContext,
    ModbusSequentialDataBlock
)

from .thermo_hygrometer_sim import ThermohigrometerSim

# TODO
# ModbusDeviceContext, ModbusSequentialDataBlock, ModbusSparseDataBlock are deprecated and will be removed in v4.
# Please convert to SimData/SimDevice.
# Please read https://pymodbus.readthedocs.io/en/dev/source/upgrade_40.html#convert-to-simdata-simdevice
# ModbusServerContext is deprecated and will be removed in v4.
class ModbusServer:
    TEMPERATURE_REGISTER = 1
    HUMIDITY_REGISTER = 2

    def __init__(self, host, port):
        self.host = host
        self.port = port

        input_registers = ModbusSequentialDataBlock(1, [0] * 2)
        self.device = ModbusDeviceContext(ir=input_registers)
        self.context = ModbusServerContext(devices=self.device, single=True)
        self.server = ModbusTcpServer(
            context=self.context,
            address=(self.host, self.port),
            trace_connect=self.handle_client_connection,
        )

        self.thermo_hygrometer_sim = ThermohigrometerSim()

    def handle_client_connection(self, connected: bool) -> None:
        if connected:
            print("Modbus client connected")
        else:
            print("Modbus client disconnected")

    async def update_registers(self):
        while True:
            self.thermo_hygrometer_sim.simulate_changes()

            temperature = self.thermo_hygrometer_sim.read_temperature()
            humidity = self.thermo_hygrometer_sim.read_humidity()

            temperature_register = self.encode_signed_int16(
                temperature,
                scale=10,
            )

            humidity_register = self.encode_unsigned_int16(
                humidity,
                scale=10,
            )

            await self.server.async_setValues(
                device_id=1,
                func_code=4,
                address=0,
                values=[
                    temperature_register,
                    humidity_register,
                ],
            )

            print(
                f"Temperature: {temperature:.1f} °C, "
                f"humidity: {humidity:.1f} %"
            )

            await asyncio.sleep(1)

    async def start(self):
        print(f"Starting Modbus server on {self.host}:{self.port}")
        asyncio.create_task(self.update_registers())
        await self.server.serve_forever()

    @staticmethod
    def encode_signed_int16(value, scale=1):
        scaled_value = round(value * scale)

        if not -32768 <= scaled_value <= 32767:
            raise ValueError("Value does not fit in signed 16-bit register")

        return scaled_value & 0xFFFF

    @staticmethod
    def encode_unsigned_int16(value: float, scale=1) -> int:
        scaled_value = round(value * scale)

        if not 0 <= scaled_value <= 65535:
            raise ValueError("Value does not fit in unsigned 16-bit register")

        return scaled_value