from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os, random, pathlib 

# Used for relative paths
basedir = os.path.abspath(os.path.dirname(__file__))

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, './database.sqlit3.nmea')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from . import models

    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

class info(db.Model): #maps to a table    
    #specify the columns
    id = db.Column(db.Integer,primary_key=True)
    message_desc = db.Column(db.String(50)) # db.String(<characters>)
    can_interface = db.Column(db.String(25))
    arb_id = db.Column(db.Integer) 
    data_string = db.Column(db.Integer)
    notes = db.Column(db.String(750))
    looping = db.Column(db.Integer)

    def __init__(self, _primary_key:int,_message_desc:str,_can_interface:str,_arb_id:int,_data_string:int,_notes:str,_looping:int):
        self.primary_key=_primary_key
        self.message_desc=_message_desc
        self.can_interface =_can_interface
        self.arb_id=_arb_id
        self.data_string=_data_string
        self.notes=_notes
        self.looping=_looping

    @staticmethod
    def insert(_primary_key,_message_desc,_can_interface,_arb_id,_data_string,_notes,_looping):
        newInfo = info(_primary_key,_message_desc,_can_interface,_arb_id,_data_string,_notes,_looping)
        db.session.add(newInfo)
        db.session.commit()


class interfaces(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    bitrate = db.Column(db.Integer)
    data_bitrate = db.Column(db.Integer)
    can_type = db.Column(db.Boolean)


class nodes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

    # shtutadown = db.Column(db.Boolean)
