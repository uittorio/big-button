import asyncio

from config import get_config
from mob import Mob


async def main():
    config = await get_config()
    mob = Mob.create(config.projects_paths, config.verbose)
    await mob.next()


asyncio.run(main())
