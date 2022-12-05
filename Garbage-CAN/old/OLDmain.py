from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user
from . import db, info, interfaces
from cmath import atan
import os, random, pathlib
import can
from can.message import Message
import time
from threading import Thread
from time import sleep
# from database import info, interfaces

main = Blueprint('main', __name__)

# Search filter statuses
search_state = {"message_desc":True,"can_interface":True,"arb_id":True,"data_string":True,"id":True}

# Dabatase Class
# class info(db.Model): #maps to a table    
#     #specify the columns
#     id = db.Column(db.Integer,primary_key=True)
#     message_desc = db.Column(db.String(50)) # db.String(<characters>)
#     can_interface = db.Column(db.String(25))
#     arb_id = db.Column(db.Integer) 
#     data_string = db.Column(db.Integer)
#     notes = db.Column(db.String(750))
#     looping = db.Column(db.Integer)

#     def __init__(self, _primary_key:int,_message_desc:str,_can_interface:str,_arb_id:int,_data_string:int,_notes:str,_looping:int):
#         self.primary_key=_primary_key
#         self.message_desc=_message_desc
#         self.can_interface =_can_interface
#         self.arb_id=_arb_id
#         self.data_string=_data_string
#         self.notes=_notes
#         self.looping=_looping

#     @staticmethod
#     def insert(_primary_key,_message_desc,_can_interface,_arb_id,_data_string,_notes,_looping):
#         newInfo = info(_primary_key,_message_desc,_can_interface,_arb_id,_data_string,_notes,_looping)
#         db.session.add(newInfo)
#         db.session.commit()


# class interfaces(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(50))
#     bitrate = db.Column(db.Integer)
#     data_bitrate = db.Column(db.Integer)
#     can_type = db.Column(db.Boolean)
#     # shtutadown = db.Column(db.Boolean)

# To view list of all messages
@main.route('/table', methods=['GET'])
@login_required
def table():
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
        print("no search string")
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
        # Populate with data based on passed ID
        data = info.query.filter(info.id == id).first()
        if(not data):
            return redirect(url_for('table'))
        return render_template('inspect.html', data=data)

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
        return redirect(url_for('table'))
    
    except:
        return redirect(url_for('table'))
    
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
        return redirect(url_for('inspect',id=id))
    except: ()
    
    if(len(request.form['message_desc']) == 0):
        flash('Missing or invalid message description')
        # flash that message
        return redirect(url_for('inspect',id=id))

    entry.message_desc = request.form['message_desc']

    if(len(request.form['can_interface']) == 0):
        flash('Missing or invalid CAN Interface')
        # flash that message
        return redirect(url_for('inspect',id=id))

    entry.can_interface = request.form['can_interface']

    try:
        # Check for valid hex value
        entry.arb_id = int(request.form['arb_id'], 16)
        # Convert to decimal for storage
        #_arb_id = int(_arb_id)
    except:
        flash('Missing or invalid Arb-ID')
        # flash that message
        return redirect(url_for('inspect',id=id))

    try:
        # Check for valid hex value
        entry.data_string = int(request.form['data_string'], 16)
        # Convert to decimal for storage
        #_data_string = int(request.form['data_string'], 16)
    except:
        flash('Missing or invalid data string')
        # flash that message
        return redirect(url_for('inspect',id=id))
    
    try:
        _notes = request.form['notes']

        if(_notes):
            entry.notes = _notes
    except: ()
 
    # If everything passes the checks
    db.session.commit()
    flash('nominally updated')

    return redirect(url_for('inspect',id=id))

# To delete an existing message
@main.route('/delete/<id>',methods=['POST'])
@login_required
def deleteFromTable(id):

    _primary_key = id
    # info.query.filter(info.id == _primary_key).delete()
    obj = info.query.filter_by(id = _primary_key).one()
    db.session.delete(obj)
    db.session.commit()

    return redirect(url_for('table'))

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

    with can.interface.Bus(channel=_name, bustype="socketcan",bitrate=_bitrate,data_bitrate=_data_bitrate,fd = _fd_msg) as bus:
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
    global looping_state
    #assume already initalized?
    print('trying to send')
    #Get FD Status
    _can_interface = request.form['interface_place'].split()[0]
    print(_can_interface)
    _arb_id = request.form['arb_place']
    _dataString = request.form['data_place']
    _looping = request.form['looping_place']

    if(_looping == "1"): #1 means global looping is on.
        looping_state=True
    else:
        looping_state=False #not 1 means looping is off.
    try:
        _data = bytes.fromhex(_dataString)
        _arb_id = int(_arb_id,16)
        print(_arb_id)
        print("test formatting")

        try:
            print("second try")
            obj = interfaces.query.filter(interfaces.name.contains(_can_interface)).first() #filter for interface
            print(obj)
            _fd_msg = obj.can_type #gather pertinant data
            _bitrate = obj.bitrate
            print(_bitrate)
            _data_bitrate = obj.data_bitrate
            _name = obj.name
            print(_name)
            # if(_fd_msg==1):
            #     _fd_msg = True
            # else:
            #     _fd_msg = False
            # print(_fd_msg)
            _fd_msg=False
            print(_fd_msg)
            if(_looping == "1"): #1 means global looping is on.
                looping_state=True
            else:
                looping_state=False #not 1 means looping is off.
            print(looping_state)
            if(looping_state):
                print("in here")
                thread = Thread(target=canLooping(_name,_bitrate,_data_bitrate,_fd_msg,_arb_id,_data))
                thread.start()
                print("Thread Started")
            else:
                print("Send one shot can here")
                
        except:
            flash("Interface not found.")
    except:
        flash("Enter a valid CAN data frame and Arb ID.")

        # return redirect(url_for('table'))
    if "custom" in id:
        return redirect(url_for('command'))
    else:
        return redirect(url_for('inspect',id=id))


@main.route('/interface')
@login_required
def interface():
    data=interfaces.query
    return render_template('interface.html',data=data)

@main.route('/init', methods=['POST'])
@login_required
def init():
    path = pathlib.Path(__file__).parent.resolve() / request.form['type']
    print(str(path) + ' 500000')
    os.system(str(path) + ' 500000')
    flash('Ran script ' + request.form['type'])
    return redirect(url_for('interface'))

@main.route('/command')
@login_required
def command():
    return render_template('command.html')

@main.route('/exfil', methods=['GET', 'POST'])
@login_required
def exfil():
    if(request.method == 'POST'):    
        
        data = [request.form['d_can'], request.form['d_arb'], request.form['d_mask'], request.form['d_time']]
        prepStr = 'timeout ' + data[3] + ' candump ' + data[0] + ',' + data[1] + ':' + data[2] + ' -t A > dump_file'
        
        os.system(prepStr)
        return_data = open('./dump_file', 'r').read()
        os.system('rm ./dump_file')

        print(return_data)
        flash('Capture Executed!')

        return render_template('exfil.html',data=return_data)
    return render_template('exfil.html')
    
@main.route('/cant', methods=['GET', 'POST'])
@login_required
def cant():
    if(request.method == 'GET'):
        return render_template('cant.html')
    
    path = pathlib.Path(__file__).parent.resolve() / request.form['type']
    os.system(str(path))
    flash('Ran script ' + request.form['type'])
    return redirect(url_for('cant'))

# Run
# looping_state = Value('b', False)
# p = Process(target=canLooping, args=(looping_state,))

if(__name__ == '__main__'):
    #os.system('initialize.sh')

    app.run(debug=False,host='0.0.0.0',use_reloader=False,port='8000') #use_reloader=False needed for the child stuff
