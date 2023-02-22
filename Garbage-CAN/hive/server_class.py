import socket
from cryptography.fernet import Fernet
import json
import random
import time
#from art import tprint
import threading
from threading import Thread

#Client code
from .client_class import Client

from termcolor import colored

import os,random
from pathlib import Path


import base64


class Server:
    lock = threading.Lock()
    nodes={}
    attacks = {}
    ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sym_key = open('./hive/sym.key', 'rb').read()
    fernet = Fernet(sym_key)
    host = "0.0.0.0" #TODO Get the host working so i dont have to hardcode the 0.0.0.0 IP and we can choose certain interfaces
    def __init__(self,port,client_listener):
        # self.host = "0.0.0.0"
        self.port = port
        self.addr = (self.host, self.port)
        self.client_listener = client_listener

    # def getClientListener(self):
    #     self.lock.acquire()
    #     port =  self.client_listener
    #     self.lock.release()
    #     return str(port)
    # #Make this prettier
    #Also can i just say that i love thread locks for making this code work :D <3
    def viewNodes(self):
        self.lock.acquire()
        print(self.nodes)
        self.lock.release()
    def updateNodes(self,nodeID,dataList):
        self.lock.acquire()
        self.nodes[nodeID] = dataList
        self.lock.release()
    # def viewAttacks(self):
    #     self.lock.acquire()
    #     print(self.attacks)
    #     self.lock.release()
    # def removeAttack(self,attackID):
    #     self.lock.acquire()
    #     for attacks in self.attacks.keys():
    #         if(ip in self.attacks[attacks] and )
    def initalize(self):
        fname = random.choice((os.listdir('./hive/terminalArt/')))
        data_folder = Path("./hive/terminalArt/")
        file_to_open = data_folder / fname
        print(file_to_open.read_text())
        self.lock.acquire()
        print(colored(f"Server> Initialising!\nServer> Listening Port: {self.port}\n","green"))
        print(colored('Server> C-2PO Server is listening..',"green"))
        self.ServerSideSocket.bind((self.host, self.port))
        self.ServerSideSocket.listen(10)
        self.lock.release()


        return
    
    def send(self,ip,source_port,destination_port,data):
        print("Entered send function.")
        self.lock.acquire()
        print(colored(f"Server> Attempting to send to {ip}:{destination_port} from {source_port}...","blue"))
        portSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Override the Error 98 issues
        print("1")
        portSocket.bind((self.host,source_port)) #random port on 0.0.0.0
        print("2")

        sent = False
        while(not sent):
            try:
                portSocket.connect((ip,destination_port)); #usually port 4000
                sent = True
            except:
                pass
        print("3")

        portSocket.sendall(self.fernet.encrypt(json.dumps(data).encode()))
        print("4")

        portSocket.close()
        print("5")
        self.lock.release()
        print(colored("Server> Maybe sent?","blue"))

    def encryptJSON(self,message):
        return self.fernet.encrypt(json.dumps(message).encode())

    def decryptJSON(self, message): #i had jsut added conn.close and locks and that made thigns stop working idk
        return self.fernet.decrypt(message).decode("UTF-8").strip()
#FINISH THIS THEN WORK ON SEDNING
    def recieve(self,listening_port):
        print("In recieve")
        portSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Override the Error 98 issues
        portSocket.bind((self.host,listening_port)) #random port on 0.0.0.0
        portSocket.listen(2)
        print(colored(f"Server> Opened port on {listening_port}","blue"))
        conn, address = portSocket.accept()        

        print(colored(f"Server> Recieved connection from {address}","green"))
        data = conn.recv(1024)
        print(data)


        if(data):
            print("here")
            print(colored(f"Server> {self.decryptJSON(self,data)}","green"))
            conn.sendall(data)
            conn.close()
            portSocket.close()
            
            # return self.decryptJSON(self,data)
        else:
            print("Else")
            conn.sendall(data)
            conn.close()
            portSocket.close()
    def normal_recieve(self,listening_port):
        print("In recieve")
        portSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Override the Error 98 issues
        portSocket.bind((self.host,listening_port)) #random port on 0.0.0.0
        portSocket.listen(2)
        print(colored(f"Server> Opened port on {listening_port}","blue"))
        conn, address = portSocket.accept()        

        print(colored(f"Server> Recieved connection from {address}","green"))
        data = conn.recv(256000)
        if(data):
            print("here")
            conn.sendall(data)
            conn.close()
            portSocket.close()
            data2 = base64.b64decode(data).decode("UTF-8")
            return data2
            # return self.decryptJSON(self,data)
        else:
            print("Else")
            conn.sendall(data)
            conn.close()
            portSocket.close()
            return

    def addAttack(self,ip,port):
        self.lock.acquire()
        attackID = time.time()
        data = []
        data.append(ip)
        data.append(port)
        self.attacks[attackID] = data
        self.lock.release()

    def processJson(self,jsonObject,client_ip): #Will handle recieving the json data and the appropriate action for inits and ACKS.
        print("Server> In Process JSON")
        if(jsonObject['message'] == "INIT?"):
            print("Server> In IF statement JSON")
            port_assigned = random.randint(10000,65000)
            node_data = [client_ip,port_assigned]

            init_response={
                "message":"INIT",
                "data":"NONE"
            }
            port_agreement={
                "message":"PORT SET",
                "data":str(port_assigned)
            }
    
            self.lock.acquire()
            nodeID = len(self.nodes)+1
            self.lock.release()  
            dataList = []
            dataList.append(client_ip)
            dataList.append(port_assigned)
            self.updateNodes(str(nodeID),dataList)
            print(colored(f"Server> Creating new node.\nServer> NodeID: {nodeID} Connection Info: {str(node_data)}","green"))
            self.send(client_ip,port_assigned,self.client_listener,init_response)
            print("Server> Sent data Process JSON")
             #Connect to the port 4000 on client
            self.send(client_ip,port_assigned,self.client_listener,port_agreement)
            self.recieve(port_assigned)
            

            return        

    def listening_nodes(self):
        
        while True:
            Client, address = self.ServerSideSocket.accept()

            if(Client):
                nodeip = address[0]
                nodeport = address[1]
                print(colored('Server> Connected to: ' + nodeip + ':' + str(nodeport),"blue"))
                # nodes_dic[address[0]]=address[1]
                data = Client.recv(1024)
                print(colored(f'Server> Printing data from {nodeip}:{nodeport}',"blue"))
                print("{!r}".format(data))
                if data:
                    try:
                        jsonObject = json.loads(self.fernet.decrypt(data).decode("UTF-8").strip())
                        print(colored(f"Server> Decrypted data:\n {jsonObject}","green"))
                        try:
                            self.processJson(jsonObject,nodeip)
                            Client.close()
                        except:
                            # print(colored("Server> Could not process JSON Data","red")) #TODO FIX THIS ON INTIIALISATION, BUT IT WORKS WHEN SENDING?  ONE METHOD FOR SEND ONE FOR INIT?
                            Client.close()
                    except:
                        print(self.decryptJSON(data))
                        print(colored("Server> Could not decrypt data, closing socket","red"))
                        Client.close()


                else:
                    print(colored('no data from', address[0],"red"))
                    break




#TODO
#Add manual nodes
#Delete Nodes
#Exfil

def main():
    server_port = 2023
    client_port = 4000

    jsonTemplates = json.load(open("message_templates.json"))
    
    server = Server(server_port,client_port) 
    server.initalize()
    

    client = Client(server,jsonTemplates)
    serverThread = Thread(target=server.listening_nodes,args=()) #Wehn you make a thread/process dont have () in the target... that took way too long.
    clientThread = Thread(target=client.menu,args=()) #Needs to be a thread not a process otherwise the menu wont work
    clientThread.start()
    serverThread.start()
    while True:
       pass

    ServerSideSocket.close()

if __name__ == '__main__':
    main()