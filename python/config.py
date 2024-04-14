import tomllib


async def get_config():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)
        address = settings["pico"]["address"]
        bluetooth_service_uuid = settings["pico"]["bluetooth_service_uuid"]
        bluetooth_service_uuid_tx = settings["pico"]["bluetooth_service_uuid_tx"]
        projects_paths = settings["local"]["projects_paths"]
        return address, bluetooth_service_uuid, bluetooth_service_uuid_tx, projects_paths
