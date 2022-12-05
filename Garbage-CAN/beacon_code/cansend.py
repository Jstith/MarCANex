import can
from can.message import Message
import time
import threading
from termcolor import colored

class CanSend:

    def __init__(self):
        self.looping_state = False
        self.running_threads = {}
        self.thread_status = {}

    # Just imported right now, probably doesn't work in its current state
    def canLooping(self, _name,_bitrate,_data_bitrate,_fd_msg,_arb_id,_data, command_id):
        # print(_name)
        # print(_bitrate)
        # print(_data_bitrate)
        # print(_fd_msg)
        # print(_arb_id)
        # print(_data)
        with can.interface.Bus(channel=_name, bustype="socketcan",bitrate=_bitrate,data_bitrate=_data_bitrate,fd = _fd_msg) as bus:
            #print("message creation start")
            msg = can.Message(
                arbitration_id=_arb_id, data=_data, is_extended_id=True #NMEA IS EXTENDED FRAMES!!!!!
            )
            #print(f'Created message successfully! {msg}')
            try:
                while True:

                    # Stops thread when global flag is changed
                    if(not self.thread_status[command_id]):
                        break

                    bus.send(msg)
                    # print("Message sent.")
                    time.sleep(0.008)
            except can.CanError as e:
                print(colored(f'[cs] LOOP ERROR: {e}', 'red'))
            except Exception as e:
                print(colored(f'[cs] GENERIC ERROR: {e}', 'red'))
                ################################

    def canLoop(self, data, command_id):

        # Check if we're starting or stopping loop
        # Call method or stop method

        #print(f'Data: {data}')
        #print(f'Command ID: {command_id}')

        if('start' in data):
            # Start looping command
            # name: can0
            # bitrate = 250000
            # _data_bitrate = 250000
            # fd_msg = False
            # arb = arb
            t1 = threading.Thread(target=self.canLooping, args=(str(data[0]), 250000, 250000, False, int(data[1], 16), bytes.fromhex(data[2]), command_id))
            t1.start()
            self.running_threads[command_id] = t1
            self.thread_status[command_id] = True

        elif('stop' in data[3].lower()):
            #stop looping command
            self.thread_status[command_id] = False