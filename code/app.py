from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
@event.listens_for(Engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    dbapi_connection.execute('PRAGMA foreign_keys=ON')


def create_app():
    app = Flask(__name__, template_folder='templates')
    
  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "chiwiwi"
    db.init_app(app)


    Migrate(app, db)


    from models import Client

    
    from routes import register_routes
    register_routes(app, db)

    return app
