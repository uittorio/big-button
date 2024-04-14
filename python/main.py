import asyncio

from config import get_config
from mob_next import MobNext
from python.pico_bluetooth_handler import PicoBluetoothHandler


async def main():
    address, bluetooth_service_uuid, bluetooth_service_uuid_tx, projects_paths = await get_config()

    async with PicoBluetoothHandler(address, bluetooth_service_uuid, bluetooth_service_uuid_tx) as handler:
        await MobNext.create(handler, projects_paths)
        await handler.keep_alive()


asyncio.run(main())
