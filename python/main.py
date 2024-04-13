import asyncio
import tomllib
from mob_next import mob_next
from bleak import BleakClient


def execute_mob_next_for_projects(projects_path: str):
    def execute_mob_next(_: object, __: bytearray):
        mob_next(projects_path)
    return execute_mob_next


async def main():
    address, bluetooth_service_uuid, projects_path = await get_config()

    print("Start searching...")
    while True:
        async with BleakClient(address) as client:
            print("Connected!")
            await client.start_notify(bluetooth_service_uuid, execute_mob_next_for_projects(projects_path))
            while client.is_connected:
                await asyncio.sleep(1)


async def get_config():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)
        address = settings["pico"]["address"]
        bluetooth_service_uuid = settings["pico"]["bluetooth_service_uuid"]
        projects_path = settings["local"]["projects_path"]
        return address, bluetooth_service_uuid, projects_path


asyncio.run(main())
