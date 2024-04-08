import asyncio
import subprocess
from bleak import BleakClient

BIG_BUTTON_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

def execute_ls_command(sender: object, data: bytearray):
    print(f"RECEIVED: {sender}: {data}")
    result = subprocess.run(["mob", "next"], capture_output=True, text=True, cwd="/media/pmyl/Tardis/Projects")
    print(result.stdout)

async def main():
    address = get_address()
    print("Start searching...")
    while(True):
        async with BleakClient(address) as client:
            print("Connected!")
            await client.start_notify(BIG_BUTTON_UUID, execute_ls_command)
            while (client.is_connected):
                await asyncio.sleep(1)

def get_address():
    with open("address.txt", "r") as file:
        return file.read()

asyncio.run(main())



