import socket
from cryptography.fernet import Fernet
from socket import timeout as TimeoutException
import base64
import time
from termcolor import colored

class SneakySend:

    def __init__(self, key, interface_ip, listen_port):
        self.key = key
        self.load_key()

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Stays binded and listening for new data all the time
        
        self.interface_ip = interface_ip
        self.listen_port = listen_port
        
        self.receive_socket.bind((self.interface_ip, self.listen_port))
        self.receive_socket.listen()

    def load_key(self):
        # key = Fernet.generate_key()
        with open(self.key, 'rb') as f:
            sym_key = f.read()
            f.close()
            self.fernet = Fernet(sym_key)
    
    def send_encrypted_message(self, data, server_ip, server_port):
        enc = self.fernet.encrypt(data.encode())
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print(f'server_ip: {server_ip} server_port: {server_port}')
        try:
            self.send_socket.connect((server_ip, server_port))
            self.send_socket.sendall(enc)
            print(colored(f'[ss] SEND: Data sent', 'blue'))
        except Exception as e:
            print(colored(f'[ss] SEND: {server_ip}:{server_port} {e}', 'yellow'))
        self.send_socket.close()
        return

    # -1 seconds for infinite wait
    # bad things happen if the received message is not formatted for Fermat (aka it crashes)
    def receive_encrypted_message(self, wait_seconds):
        try:
            self.receive_socket.settimeout(wait_seconds)
            conn, addr = self.receive_socket.accept()
            with conn:
                    print(colored(f"[ss] RECV: Connection from {addr}", 'blue'))
                    data = conn.recv(1024)
                    # If there is a time to wait, wait that time then return something
                    # Otherwise, wait indefinintely (only broken by outer try catch)
                    if(data):
                        print(colored('[ss] RECV: Received data', 'blue'))
                        return(self.fernet.decrypt(data).decode('UTF-8').strip())
                    else:
                        print(colored(f'[ss] RECV: {self.interface_ip}:{self.listen_port} no data received after {wait_seconds} seconds..', 'yellow'))
                        return None
        except Exception as e:
            if(not type(e) == TimeoutException):
                print(colored(f'[ss] RECV: {self.interface_ip}:{self.listen_port} {e}', 'yellow'))
        return None