import tomllib


async def get_config():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)
        address = settings["pico"]["address"]
        bluetooth_service_uuid = settings["pico"]["bluetooth_service_uuid"]
        projects_path = settings["local"]["projects_path"]
        return address, bluetooth_service_uuid, projects_path
