import asyncio
from bleak import BleakClient

address = "MAC address"
MODEL_NBR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

def callback(sender: object, data: bytearray):
    print(f"{sender}: {data}")

async def main(address):
    while(True):
        async with BleakClient(address) as client:
            await client.start_notify(MODEL_NBR_UUID, callback)
            while (client.is_connected):
                await asyncio.sleep(1)

        

asyncio.run(main(address))



