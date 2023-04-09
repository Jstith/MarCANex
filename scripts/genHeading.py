from math import degrees, floor
import can

import time

from threading import Thread
from time import sleep


def canLooping(_name,_bitrate,_data_bitrate,_fd_msg,_arb_id,_data):


    with can.interface.Bus(channel=_name, bustype="socketcan",bitrate=_bitrate,data_bitrate=_data_bitrate,fd = _fd_msg) as bus:
        print("message creation start")
        msg = can.Message(
            arbitration_id=_arb_id, data=_data, is_extended_id=True #NMEA IS EXTENDED FRAMES!!!!!
        )

        print(msg)
        try:
                bus.send(msg)
                print("Message sent.")
        except can.CanError:
            print("Message NOT sent")
        except:
            print("its all broken")
            ################################

name="can0"
bitrate=250000
dbbitrate=250000
fd=False
arb=166793838
# data=bytes.fromhex("000dfcFFFF0000FC")

BRO="000eXXFFFF0000FC"

degrees=input("Enter degrees")
print("Shooting for " + degrees)

# bytess= "{:02x}".format((int((int(degrees,10) - 0.124 )/ 1.46)))
bytess=int(0.682*int(degrees) + -0.0847)
bytess="{:02x}".format(bytess)

data=bytes.fromhex(BRO.replace("XX", bytess))
print(data)
data = bytes.fromhex(BRO.replace("XX", bytess))

print(data)

while True:
    canLooping(name,bitrate,dbbitrate,fd,arb,data)
