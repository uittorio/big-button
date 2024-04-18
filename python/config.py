import tomllib


class Config:
    def __init__(self, address, bluetooth_service_uuid, bluetooth_service_uuid_tx, projects_paths, verbose):
        self.address = address
        self.bluetooth_service_uuid = bluetooth_service_uuid
        self.bluetooth_service_uuid_tx = bluetooth_service_uuid_tx
        self.projects_paths = projects_paths
        self.verbose = verbose


async def get_config():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)
        address = settings["pico"]["address"]
        bluetooth_service_uuid = settings["pico"]["bluetooth_service_uuid"]
        bluetooth_service_uuid_tx = settings["pico"]["bluetooth_service_uuid_tx"]
        projects_paths = settings["local"]["projects_paths"]

        if "verbose" in settings["local"]:
            verbose = settings["local"]["verbose"] == "true"
        else:
            verbose = True

        return Config(address, bluetooth_service_uuid, bluetooth_service_uuid_tx, projects_paths, verbose)
