#!/bin/python3

import asyncio
from bleak import BleakScanner
from bleak import BleakClient
address = "48:87:2D:62:95:1E"
SIGNATURE               = 0x55
CMD_SERVO_MOVE          = 0x03
CMD_GET_BATTERY_VOLTAGE = 0x0f
CMD_SERVO_STOP          = 0x14
CMD_GET_SERVO_POSITION  = 0x15

async def discovery():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

async def main(address):
    async with BleakClient(address) as client:
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))
        print(client.services.characteristics)
        print(client.services.descriptors)

async def getServices(address):
    async with BleakClient(address) as client:
	    svcs = client.services
	    print("Services:")
	    for service in svcs:
	    	print(service.description, service.handle, service.uuid)
	    	for characteristic in service.characteristics:
	    		print('\t',characteristic.description, characteristic.handle, characteristic.uuid)
	    		for descriptor in characteristic.descriptors:
	    			print("\t\t", descriptor.description, descriptor.handle, descriptor.uuid)
	    		for proprty in characteristic.properties:
	    			print("\t\t", proprty)
	    		if 'write' in proprty:
	    			print("Write property detected:")
	    			data = ""
	    			cmd = CMD_GET_BATTERY_VOLTAGE
	    			print("\t\t Sending: ",bytes([SIGNATURE, SIGNATURE, len(data) + 2, cmd]))
	    			print("\t\t Recieved from write:", await client.write_gatt_char(characteristic.handle,bytes([0x00,SIGNATURE, SIGNATURE, len(data) + 2, cmd]), response=True))
    			if 'read' in proprty:
    				print("\t\t Received: ", await client.read_gatt_char(characteristic.handle))
	    # print(await client.read_gatt_char(23))
	    # print(await )


# asyncio.run(discovery())
#asyncio.run(main(address))
asyncio.run(getServices(address))