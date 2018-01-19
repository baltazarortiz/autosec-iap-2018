import can
import sys
import time
from canlib import *

BUS_TYPE = 'socketcan_native'
CHANNEL = 'can0'
ARID =  int(ARIDS['CAR_SPEED'], 16)

print("START")
# start a connection 

bus = connect_bus(BUS_TYPE, CHANNEL)

def get_checksum(val, target_sum):
    message = '0'+'{:02x}'.format(val)
    sum_digit = sum(map(lambda x: int(x, 16), message))
    sum_digit %= 16
    ans_val = target_sum - sum_digit 
    if ans_val < 0:
        ans_val += 16
    return int_to_hex_string_suffix(ans_val)

def int_to_hex_string_prefix(val):
    return '{:07x}'.format(val).upper()
def int_to_hex_string_prefix2(val):
    return '{:015x}'.format(val).upper()
def int_to_hex_string_suffix(val):
    return '{:01x}'.format(val).upper()

def get_message_engine_speed(prefix_val):
    return int_to_hex_string_prefix(prefix_val) + get_checksum(prefix_val, 14)
def get_message_car_speed(prefix_val):
    return int_to_hex_string_prefix2(prefix_val) + get_checksum(prefix_val, 10)


def get_seq_car_speeds(speed):

    target = get_message_car_speed(get_speed(speed))
    print(target)
    # target = "00000000EE430037"

    # target = "0000000002430037"
    prefix = target[:-1]
    prefix_val = int(prefix, 16)
    diff_prefix = 1
    first_val = int(target, 16)
    curr_val = first_val #+ diff*4

    seq = []
    for i in range(40):
        message = get_message_car_speed(prefix_val)
        prefix_val += diff_prefix
        seq.append(message)
    return seq

def get_seq_engine_speeds():

    target = "02EEFFFC"

    prefix = target[:-1]
    prefix_val = int(prefix, 16)
    diff_prefix = 1
    first_val = int(target, 16)
    curr_val = first_val #+ diff*4

    seq = []
    for i in range(1000):
        message = get_message_engine_speed(prefix_val)
        prefix_val += diff_prefix
        seq.append(message)
    return seq

def get_speed(speed):
    if speed > 140:
        speed = 140
    MAX_VAL = 49217532 * 2
    MIN_VAL = 2371587
    MAX_SPEED = 140.0
    val = speed / MAX_SPEED * (MAX_VAL - MIN_VAL) + MIN_VAL
    print(val)
    return int(val)

def control_speed(bus):

    car_speeds = get_seq_car_speeds(140)
    send_data_stream(bus, int(ARIDS['CAR_SPEED'], 16), car_speeds)

def get_seq_from_arid(arid):

    for i in range(1000):
        message = get_message_car_speed(prefix_val)
        print(message)
        print(int(message[:-1], 16))
        send_message(bus, ARID, message)
        prefix_val += diff_prefix
        time.sleep(0.001)


song_speeds_file = open('speed.csv', 'r')
song_speeds = song_speeds_file.read().split()
song_speeds = list(map(lambda x: float(x)*10, song_speeds))
millis = int(round(time.time() * 1000))

last_time = round(time.time() * 1000)
for speed in song_speeds:

    car_speeds = get_seq_car_speeds(speed)
    while last_time - round(time.time() * 1000) >= 23:
        break
    send_data_stream(bus, int(ARIDS['CAR_SPEED'], 16), car_speeds)
    

print("END")

# .023




