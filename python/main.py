import asyncio

from config import get_config
from mob_next import MobNext
from pico_bluetooth_handler import PicoBluetoothHandler


async def main():
    config = await get_config()

    mob_next = MobNext.create(config.projects_paths, config.verbose)
    async with PicoBluetoothHandler(config.address, config.bluetooth_service_uuid, config.bluetooth_service_uuid_tx, mob_next) as handler:
        await handler.keep_alive()


asyncio.run(main())
