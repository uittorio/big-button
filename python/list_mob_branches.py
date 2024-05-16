from config import get_config
from mob_next import MobNext


async def main():
    config = await get_config()
    mob_next = await MobNext.create(config.projects_paths, config.verbose)
    mob_next.list_mob_branches()
