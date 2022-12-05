from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #debigger info
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////abs/path/to/db.db' #if we dont want db in workspace
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db=SQLAlchemy(app)




class info(db.Model): #maps to a table	
#specify the columns

	id = db.Column(db.Integer,primary_key=True)
	message_desc = db.Column(db.String(50)) # db.String(<characters>)
	can_interface = db.Column(db.String(25))
	arb_id = db.Column(db.Integer) 
	data_string = db.Column(db.Integer)
	notes=db.Column(db.String(750))
	looping=db.Column(db.Integer)


class interfaces(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))
	bitrate = db.Column(db.Integer)
	data_bitrate = db.Column(db.Integer)
	can_type = db.Column(db.String(50))
	# shtutadown = db.Column(db.Boolean)


