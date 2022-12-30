import asyncio
from bleak import BleakClient
from bleak import BleakScanner

async def discoverDevices():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)



addresses = ["A4:C1:38:B1:5B:82" "A4:C1:38:F8:4A:20" "A4:C1:38:83:EA:AA" "A4:C1:38:CD:A5:B7"]
address = "A4:C1:38:F8:4A:20" 
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
ACTUAL_HUMIDITY_AND_TEMPERATURE = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"
BROADCAST_HUMIDITY_AND_TEMPERATURE = "00002902-0000-1000-8000-00805f9b34fb"

async def connect(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(ACTUAL_HUMIDITY_AND_TEMPERATURE)
        print("Model Number: {0}".format("".join(map(chr, model_number))))



asyncio.run(connect(address))
