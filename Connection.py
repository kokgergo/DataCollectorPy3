import asyncio
import bleak
from bleak import BleakClient
from bleak import BleakScanner

# Constants

MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
ACTUAL_HUMIDITY_AND_TEMPERATURE = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"
BROADCAST_HUMIDITY_AND_TEMPERATURE = "00002902-0000-1000-8000-00805f9b34fb"

# Addresses of devices
addresses = ["A4:C1:38:B1:5B:82", "A4:C1:38:F8:4A:20", "A4:C1:38:83:EA:AA", "A4:C1:38:CD:A5:B7"]
address = "A4:C1:38:B1:5B:82" 

async def checkDeviceAvaible(address):
    found = await bleak.BleakScanner.find_device_by_address(device_identifier=address, timeout=10)
    if found is None:
        print("nothing")
    else:
        print(found)
        try:
            await connect(found)
        except Exception as e:
            print(e)

async def discoverDevices():
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        print(d)



async def subscribe(addr) :
    try:
        async with BleakClient(addr) as client :
            await client.start_notify(54,processData)
    except Exception as e:
        print(e)

def processData(GattChar, data:bytearray):
    temp, humid, batt = temp_humid_parser(data)
    print("Temp: {0} Humid: {1} Batt: {2}".format(temp, humid, batt))


async def connect(address):
    async with BleakClient(address) as client:   
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))
        actual_hum_and_temp = await client.read_gatt_char(ACTUAL_HUMIDITY_AND_TEMPERATURE)
        print(actual_hum_and_temp)
        temp, humidity, voltage = temp_humid_parser(actual_hum_and_temp)
        print("Temp: {0} Humid: {1} Batt: {2}".format(temp, humidity, voltage))

def temp_humid_parser(data : bytearray):
    """ First two byte is the temperature*100 data little endian
        Third is humidity in %
        Fourth and Fifth is Voltage level of the battery in mV little endian also
    """
    # data_str = ''.join(format(d, '02x') for d in data)
    # print("Raw data: "+ data_str)
    temp = data[:2:]
    temp = temp[::-1]
    # temp_str = ''.join(format(d, '02x') for d in temp)
    temp_int = int.from_bytes(temp,'big')
    temp_float = temp_int/100.0
    # print("Temperature: ", temp_float)
    humidity = int(data[2])
    # print("Humidity: {0}", humidity)
    battery = data[:2:-1]
    # battery_str = ''.join(format(d, '02x') for d in battery)
    battery_int = int.from_bytes(battery,'big')
    # print("Battery: {0}", battery_int)

    return temp_float, humidity, battery_int

def main():
    for addr in addresses:
        print(addr)
        asyncio.run(subscribe(addr))


main()

