import asyncio

from config import get_config
from mob_next import MobNext


class LocalHandler:
    def __init__(self):
        self.run = None

    async def on_start(self):
        pass

    async def on_end(self):
        pass

    async def on_notify(self, run):
        self.run = run


async def main():
    config = await get_config()

    handler = LocalHandler()
    await MobNext.create(config.handler, config.projects_paths, config.verbose)

    await handler.run()


asyncio.run(main())
