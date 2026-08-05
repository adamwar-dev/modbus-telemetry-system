from asyncio import run
from pymodbus import __version__ as pymodbus_version

from modbus_server_sim import ModbusServer

REQUIRED_PYMODBUS_VERSION = "3.14.0"

def validate_dependencies() -> None:
    print(f"PyModbus version: {pymodbus_version}")

    if pymodbus_version != REQUIRED_PYMODBUS_VERSION:
        raise RuntimeError(
            f"Unsupported PyModbus version: {pymodbus_version}. "
            f"Required version: {REQUIRED_PYMODBUS_VERSION}."
        )

async def main() -> None:
    validate_dependencies()
    server = ModbusServer(host="localhost", port=5020)
    await server.start()


if __name__ == "__main__":
    run(main())