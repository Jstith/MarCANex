import can

import time

from threading import Thread
from time import sleep


def canLooping(_name,_bitrate,_data_bitrate,_fd_msg,_arb_id,_data):

    print(_name)
    print(_bitrate)
    print(_data_bitrate)
    print(_fd_msg)
    print(_arb_id)
    print(_data)

    with can.interface.Bus(channel=_name, bustype="socketcan",bitrate=_bitrate,data_bitrate=_data_bitrate,fd = _fd_msg) as bus:
        print("message creation start")
        msg = can.Message(
            arbitration_id=_arb_id, data=_data, is_extended_id=True #NMEA IS EXTENDED FRAMES!!!!!
        )

        print(msg)
        try:
                bus.send(msg)
                print("Message sent.")
                time.sleep(0.008)
        except can.CanError:
            print("Message NOT sent")
        except:
            print("its all broken")
            ################################

name="can0"
bitrate=250000
dbbitrate=250000
fd=False
arb=167248238
#XX  = LAT BYTE
#YY = LONG BYTE
broo="000000XX000000YY"
lathexx=""
longhexx=""
deslat=input("Please input desired lat (i dont wanna do input validation so please just be nice)")
deslong=input("Please input desired lat (i dont wanna do input validation so please just be nice)")

try:
    int(desLong)
    int(deslat)
except:
    print("dont make me actually do input validation... tsk tsk")

deslat=int(deslat)
deslong=int(deslong)

#Positives
if(deslat > 0 and deslat < 213): #not sure why 213?
    lathexx= "{:02x}".format((int((int(deslat) * 0.596)- 0.000874)))
    print(lathexx)
if(deslong > 0 and deslong < 213): #not sure why 213?
    longhexx= "{:02x}".format((int((int(deslong) * 0.596)- 0.000874)))
    print(longhexx)


#Negatives
if(deslat < 0 and deslat >  -213): #not sure why 213?
    lathexx= "{:02x}".format((int((int(deslat) * 0.596) + 256)))
    print(lathexx)

if(deslong < 0 and deslong > -213): #not sure why 213?
    longhexx= "{:02x}".format((int((int(deslong) * 0.596) + 256)))
    print(longhexx)


broo=broo.replace("XX",lathexx)
broo=broo.replace("YY",longhexx)
print(broo)

data=bytes.fromhex(broo)

print(name)
print(bitrate)
print(dbbitrate)
print(fd)
print(arb)
print(data)
while True:
    canLooping(name,bitrate,dbbitrate,fd,arb,data)