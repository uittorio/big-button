import asyncio

from config import get_config
from mob_next import mob_next


async def main():
    address, bluetooth_service_uuid, projects_paths = await get_config()

    mob_next(projects_paths)


asyncio.run(main())
