import pprint 
import sys
import can
import time
import binascii



speed_id = 0x158
tach_id = 0x1DC
safety_id = 0x39
seatbelt_id = 0x305
skid_id = 0x1A4
tpms_id = 0x333
coolant_id = 0x324

def add_checksum_tach(val):
    last_c = hex(sum([int(c, 16) for c in val]))[-1]
    print("last_c", last_c)
    if last_c == 'f':
        checksum = 0xf
    else:
        checksum = 0xe - int(last_c, 16)
    print("checksum", checksum)
    return val + format(checksum, 'x')

def add_checksum_speed(val):
    last_c = hex(sum([int(c, 16) for c in val]))[-1]
    print("last_c", last_c)
    if last_c == 'b':
        checksum = 0xf
    elif last_c == 'c':
        checksum = 0xe
    elif last_c == 'd':
        checksum = 0xd
    elif last_c == 'e':
        checksum = 0xc
    elif last_c == 'f':
        checksum = 0xb
    else:
        checksum = 0xa - int(last_c, 16)
    print("checksum", checksum)
    return val + format(checksum, 'x')

def add_checksum_safety(val):
    last_c = hex(sum([int(c, 16) for c in val]))[-1]
    print("last_c safety_bag", last_c)
    checksum = 0xc - int(last_c, 16)
    print("checksum", checksum)
    return val + format(checksum, 'x')

def add_checksum_seatbelt(val):
    last_c = hex(sum([int(c, 16) for c in val]))[-1]
    print("last_c seatbelt", last_c)
    if last_c == '0':
        checksum = 0
    else:
        checksum = 0x10 - int(last_c, 16)
    print("checksum", checksum)
    return val + format(checksum, 'x')

def add_checksum_skid(val):
    last_c = hex(sum([int(c, 16) for c in val]))[-1]
    print("last_c seatbelt", last_c)
    checksum = 9 - int(last_c, 16)
    print("checksum", checksum)
    return val + format(checksum, 'x')

def add_checksum_tpms(val):
    last_c = hex(sum([int(c, 16) for c in val]))[-1]
    print("last_c tpms", last_c)
    checksum = 0xf - int(last_c, 16)
    print("checksum", checksum)
    return val + format(checksum, 'x')


rpm = ['02FFFe0',
'02FFFe1',
'02FFFe2',
'02FFFe3'
]

speed = ['F9830000F9830D0',
'F9830000F9830D1',
'F9830000F9830D2',
'F9830000F9830D3'
]

safety_bag = ['000', '011', '012', '013']

# 00 is on, 08 is off
seatbelt = ['808','009','00A', '00B' ]
skid = ['111111111111180','000000000000001','000000000000002','000000000000003' ]
tpms = ['FFFFFFFFFFFF0', '0000000000001', '0000000000002', '0000000000003']
coolant = ['693A03FD0000000', '000000000000001', '000000000000002', '000000000000003']

seatbelt_clear = ['008','009','00A', '00B' ]
skid_clear = ['000000000000000','000000000000001','000000000000002','000000000000003' ]
tpms_clear = ['0000000000000', '0000000000001', '0000000000002', '0000000000003']
coolant_clear = ['000000000000000', '000000000000001', '000000000000002', '000000000000003']

speed = list(map(add_checksum_speed, speed))
rpm = list(map(add_checksum_tach, rpm))
safety_bag = list(map(add_checksum_safety, safety_bag))
seatbelt = list(map(add_checksum_seatbelt, seatbelt))
skid = list(map(add_checksum_skid, skid))
tpms = list(map(add_checksum_tpms, tpms))
coolant = list(map(add_checksum_tpms, coolant))

seatbelt_clear = list(map(add_checksum_seatbelt, seatbelt_clear))
skid_clear = list(map(add_checksum_skid, skid_clear))
tpms_clear = list(map(add_checksum_tpms, tpms_clear))
coolant_clear = list(map(add_checksum_tpms, coolant_clear))

print("tpms", tpms)

def send_msg(bus, arb_id, data):
    msg = can.Message(extended_id=False, arbitration_id = speed_id)
    #Construct data fields
    msg.data = binascii.unhexlify(data)
    bus.send(msg)


def pulse(bus, pulse_len):
    # msg = can.Message(extended_id=False, arbitration_id = safety_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(safety_bag[j%4])
    # bus.send(msg)

    # Pulse on 
    msg = can.Message(extended_id=False, arbitration_id = seatbelt_id)
    #Construct data fields
    msg.data = binascii.unhexlify(seatbelt[0])
    bus.send(msg)

    msg = can.Message(extended_id=False, arbitration_id = skid_id)
    #Construct data fields
    msg.data = binascii.unhexlify(skid[0])
    bus.send(msg)

    msg = can.Message(extended_id=False, arbitration_id = tpms_id)
    #Construct data fields
    msg.data = binascii.unhexlify(tpms[0])
    bus.send(msg)    

    # msg = can.Message(extended_id=False, arbitration_id = coolant_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(coolant[0])
    # bus.send(msg)    

    time.sleep(pulse_len)

    # Turn off seatbelt
    msg = can.Message(extended_id=False, arbitration_id = seatbelt_id)
    #Construct data fields
    msg.data = binascii.unhexlify(seatbelt[1])
    bus.send(msg)

    # Turn off skid
    msg = can.Message(extended_id=False, arbitration_id = skid_id)
    #Construct data fields
    msg.data = binascii.unhexlify(skid[1])
    bus.send(msg)

    # Turn off tpms
    msg = can.Message(extended_id=False, arbitration_id = tpms_id)
    #Construct data fields
    msg.data = binascii.unhexlify(tpms[1])
    bus.send(msg)

    # msg = can.Message(extended_id=False, arbitration_id = coolant_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(coolant[1])
    # bus.send(msg)
    
      
j = 0
# while True:
    # msg = can.Message(extended_id=False, arbitration_id = speed_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(speed[j%4])
    # bus.send(msg)

    # msg = can.Message(extended_id=False, arbitration_id = tach_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(rpm[j%4])
    # bus.send(msg)
  

    # msg = can.Message(extended_id=False, arbitration_id = seatbelt_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(seatbelt[0])
    # bus.send(msg)
    # time.sleep(.2)

    # msg = can.Message(extended_id=False, arbitration_id = seatbelt_id)
    # #Construct data fields
    # msg.data = binascii.unhexlify(seatbelt[1])
    # bus.send(msg)
      
    # time.sleep(.5)

    # j+=1

def clear_all(bus):
    for i in range(4):
    # Pulse on 
        msg = can.Message(extended_id=False, arbitration_id = seatbelt_id)
        #Construct data fields
        msg.data = binascii.unhexlify(seatbelt_clear[i%4])
        bus.send(msg)

        msg = can.Message(extended_id=False, arbitration_id = skid_id)
        #Construct data fields
        msg.data = binascii.unhexlify(skid_clear[i%4])
        bus.send(msg)

        msg = can.Message(extended_id=False, arbitration_id = tpms_id)
        #Construct data fields
        msg.data = binascii.unhexlify(tpms_clear[i%4])
        bus.send(msg)    
        time.sleep(.001)

def pulse_timestamps(bus, timestamps):
    # time.sleep(1.2)
    for i in range(0, len(timestamps)):
        print("timestamp", timestamps[i])
        if i == len(timestamps)-1:
            print("Done")
            break

        s = time.time()
        pulse_time = .2
        pulse(bus, pulse_time)
        diff = time.time() - s

        wait = timestamps[i+1] - timestamps[i] - diff + .001
        print ("wait", wait)
        time.sleep(wait)

