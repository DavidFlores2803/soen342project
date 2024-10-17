from flask import Flask, redirect, url_for, request, render_template, session
from controllers import OfferingsController
from models import *

app = Flask(__name__)
app.secret_key = "chiwiwi"

offeringsController = OfferingsController()


@app.route("/")
def home():
    if("currentAccount" in session):
        print(f"worked {session['currentAccount']['name']}")
    return render_template("index.html")

@app.route("/instructor_login", methods=["POST", "GET"])
def instructor_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        number = request.form["number"]
        specialization = request.form["specialization"]
        
        session["currentAccount"] = {
            "username": username,
            "password": password,
            "name": name,
            "number": number,
            "specialization": specialization
        }

        #TODO redirect to user page instead
        return redirect(url_for("home"))
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

    
@app.route("/offerings")
def offerings():
    return render_template("offerings.html", content=offeringsController.getOfferings)



if __name__ == "__main__":
    app.run()