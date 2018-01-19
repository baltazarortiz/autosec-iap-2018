import can
import time

ARIDS = {'CAR_SPEED': '158', 'ENGINE_SPEED': '1DC'}

def connect_bus(bustype, channel):
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    return bus

def send_message(bus, arid, data):
    # print(arid, data, len(data))
    msg = can.Message(extended_id=False)
    msg.arbitration_id = arid
    msg.data = bytes.fromhex(data)
    bus.send(msg)

def send_data_stream(bus, arid, data_stream):
    for data in data_stream:
        send_message(bus, arid, data)
        time.sleep(0.0001)