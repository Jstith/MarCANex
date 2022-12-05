import json
class Client:
    client_nodes = {}
    def __init__(self,server,jsonTemplates):
        self.server = server
        self.beaconMessages = ["CAN Message","Exfil Data"]
        self.jsonTemplates = jsonTemplates
        
    def viewAttacks(self): #i think we  may need a thread here too?
        print(self.server.attacks)
    def viewNodes(self): #i think we  may need a thread here too?
        print(self.server.nodes)
    def sendMessage(self):
        self.server.viewNodes()
        node = input("Client> Enter a nodeID to send to: ")
        if(not node in self.server.nodes):
            print("Client> Enter a valid node ID!")
            return
        ip = self.server.nodes[node][0]
        port = self.server.nodes[node][1]
        #Add if len of nodes is 0 then dont cos u got no nodes..
        print("Client> Displaying message optinos...")
        for i in range(len(self.beaconMessages)):
            print(f"{i+1}. {self.beaconMessages[i]}")
        selector = input("Client> Select option\n")
        selector = int(selector)
        if(selector == 1): #CAN Message
            try:
                dataList = []
                print("Client> Message template\n",self.jsonTemplates['send_command'])
                interface = input("Client> Enter interface: ")
                arb = input("Client> Enter arbitration id: ")
                data = input("Client> Enter data: ")
                looping = input("Client> \"start\" = looping \"stop\" = stop: ")
                dataList.append(interface)
                dataList.append(arb)
                dataList.append(data)
                dataList.append(looping)
                print(self.jsonTemplates['send_command'])
                jsonCopy = self.jsonTemplates['send_command']
                jsonCopy['data'] = str(dataList)
                print("Client> Sending: ",json.dumps(jsonCopy))
    # def send(self,ip,source_port,destination_port,data):
                self.server.send(ip,port,self.server.client_listener,jsonCopy) 
                self.server.recieve(port)
            except Exception as e: print(e)                 
                # if("start" in looping):  
            #     self.server.addAttack(ip,port)
            # else:
            #     self.server.removeAttack(ip,port) #TODO
            # print("Client> Message sent.")
            # self.viewAttacks()
        # print("Client> Failed to send message :( Enter and integer and check that youre JSON templates are correct")
           
        # if(selector > (len(self.beaconMessages)+1) or selector < (len(self.beaconMessages)+1)): #TODO
        #     print(selector)
        #     print("Client> Enter a valid message option please!")
        #     return
        
            


    def menu(self):
        print("Client> Starting client...")
        print(f"Client> {str(self.beaconMessages)}")
        while True:
            selector = input("1. Send new message \n2. Add new node manually \n3. View all nodes \n4. Delete a node \n")
            print(f"Client> Selected {selector}")
            selector=int(selector)

            if(selector==1):
                self.sendMessage()
                print("Client> Sending message to a node")

            if(selector==2):
                print("Adding new node...")
            
            if(selector==3):
                print("Client> Displaying all nodes...")
                self.viewNodes()