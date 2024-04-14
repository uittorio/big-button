import asyncio

from bleak import BleakClient


class PicoBluetoothHandler:
    def __init__(self, address, rx, tx):
        self.client = None
        self.address = address
        self.rx = rx
        self.tx = tx
        self.client = BleakClient(self.address)

    async def __aenter__(self):
        print("Connecting")
        await self.client.__aenter__()
        print("Connected")
        return self

    async def __aexit__(self, *args):
        await self.client.__aexit__(*args)
        print("Disconnected")

    async def on_start(self):
        await self.client.write_gatt_char(self.tx, bytearray([0x01]), response=True)

    async def on_end(self):
        await self.client.write_gatt_char(self.tx, bytearray([0x02]), response=True)

    async def on_notify(self, run):
        async def await_run(_, __):
            await run()

        await self.client.start_notify(self.rx, await_run)

    async def keep_alive(self):
        while self.client.is_connected:
            await asyncio.sleep(1)
