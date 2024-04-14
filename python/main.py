import asyncio

from bleak import BleakClient

from config import get_config
from mob_next import mob_next


def execute_mob_next_for_projects(projects_path: str):
    def execute_mob_next(_: object, __: bytearray):
        mob_next(projects_path)

    return execute_mob_next


async def main():
    address, bluetooth_service_uuid, projects_path, projects_paths = await get_config()

    print("Start searching...")
    while True:
        async with BleakClient(address) as client:
            print("Connected!")
            await client.start_notify(bluetooth_service_uuid, execute_mob_next_for_projects(projects_path))
            while client.is_connected:
                one_second = 1
                await asyncio.sleep(one_second)


asyncio.run(main())
