import sys
import can
import sys
import time

# hex constants corresponding to the min and max display values on the speedometer and tachometer
MPH_MAX = 0x5750
MPH_MIN = 0x0000
TACH_MAX = 0x1eff
TACH_MIN = 0x000f

# Arbitration IDs
MPH_ID = 0x158
TACH_ID = 0x1DC

def mph_checksum(s, count):
    sum = 0
    for c in s:
        sum += int(c, 16)

    sum += count 

    if (sum % 16) <= 10:
        return hex(10-(sum%16))[-1]
    elif (sum % 16) == 11:
        return 'f'
    elif (sum % 16) == 12:
        return 'e'
    elif (sum % 16) == 13:
        return 'd'
    elif (sum % 16) == 14:
        return 'c'
    elif (sum % 16) == 15:
        return 'b'
    elif (sum % 16) == 0:
        return 'a'

def tach_checksum(s, count):
    sum = 0
    for c in s:
        sum += int(c, 16)

    sum += count
    if (sum % 16) == 15:
        return 'f'
    else:
        return hex(14 - (sum % 16))[-1]

# From arduino wiki
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

# channel = 'can0'
# bus = can_init('can0')
def can_init(channel):
    bustype = 'socketcan_native'
    return can.interface.Bus(channel=channel, bustype=bustype)

def send_msg(bus, id, data, count):
    msg = can.Message(extended_id=False)
    msg.arbitration_id = id
    msg.data = data

    bus.send(msg)
    time.sleep(0.0001)

def gen_mph_data(target, count, gain):
    if target < 0:
        target = 0
    elif target > 140:
        target = 140

    val = '{0:0{1}x}'.format(int(map(target, 0, 140, MPH_MIN, MPH_MAX)), 4)
    val = val + '0000' + val
    return bytes.fromhex(val + '00' + str(count) + mph_checksum(val, count))

def gen_tach_data(target, count, gain):
    if target + gain < 0:
        target = 0
    elif target + gain > 8:
        target = 8

    val = '02' + '{0:0{1}x}'.format(int(map(target + gain, 0, 8, TACH_MIN, TACH_MAX)), 4)
    return  bytes.fromhex(str(val) + str(count) + tach_checksum(str(val), count))

def mph_toggle():
    count = 0
    i = 0
    target = 60
    bus = can_init('can0')

    while True:
        data = gen_mph_data(target, count)
        send_msg(bus, MPH_ID, data, count) 

        count = (count + 1) % 4
        i += 1
        if i % 1000 == 0:
            if target == 60:
                target = 80
            elif target == 80:
                target = 60

def mph_step():
    count = 0 
    i = 0
    target = 0
    bus = can_init('can0')

    while True:
        data = gen_mph_data(target, count)
        send_msg(bus, MPH_ID, data, count)

        count = (count + 1) % 4
        i = i + 1
        if i % 4000 == 0:
            target = (target + 5) % 140
            print('changing target to', target)

def tach_step():
    count = 0    
    i = 0
    target = 0
    bus = can_init('can0')

    while True:
        data = gen_tach_data(target, count)
        send_msg(bus, TACH_ID, data, count)
        
        count = (count + 1)% 4
        i += 1
        if i % 4000 == 0:
            target = (target + 0.5) % 9
            print('changing target to', target)

# Separated every 0.023 seconds
def get_timestamps():
    rev_timestamp_file = open('rev.csv', 'r')
    mph_timestamp_file = open('speed.csv', 'r')

    rev_timestamps = [float(l) for l in rev_timestamp_file]
    mph_timestamps = [float(l) for l in mph_timestamp_file]

    return(rev_timestamps, mph_timestamps)

def move_on_timestamps():
    count = 0    
    target = 0
    bus = can_init('can0')

    rev_timestamps, mph_timestamps = get_timestamps()    

    for i in range(len(rev_timestamps)):
        rev_data = gen_tach_data(rev_timestamps[i], count, 10)
        mph_data = gen_mph_data(mph_timestamps[i], count, 10)

        t_end = time.time() + 0.023
        while time.time() < t_end:
            send_msg(bus, TACH_ID, rev_data, count)
            send_msg(bus, MPH_ID, mph_data, count) 
            
def main():
    move_on_timestamps()

if __name__ == '__main__':
   main()


