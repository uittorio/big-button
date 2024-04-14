import asyncio
from config import get_config
from mob_next import mob_next


async def main():
    address, bluetooth_service_uuid, projects_path = await get_config()

    mob_next(projects_path)


asyncio.run(main())
