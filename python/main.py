import asyncio

from config import get_config
from mob_next import MobNext
from pico_bluetooth_handler import PicoBluetoothHandler


async def main():
    config = await get_config()

    async with PicoBluetoothHandler(config.address, config.bluetooth_service_uuid, config.bluetooth_service_uuid_tx) as handler:
        await MobNext.create(handler, config.projects_paths, config.verbose)
        await handler.keep_alive()


asyncio.run(main())
