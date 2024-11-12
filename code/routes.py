from flask import render_template, request
from models import Client
from models import Instructor

def register_routes(app, db):
    @app.route('/')
    def home():
        clients = Client.query.all()
        return render_template("index.html")
   
    
    @app.route('/clients')
    def list_clients():
        clients = Client.query.all()
        return render_template("client_list.html", clients=clients)

    @app.route('/instructors')
    def list_instructors():
        instructors = Instructor.query.all()
        return render_template("instructor_list.html", instructors=instructors)

    