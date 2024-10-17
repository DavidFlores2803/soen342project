from flask import Flask, redirect, url_for, request, render_template, session
from controllers import OfferingsController
from models import *

app = Flask(__name__)
app.secret_key = "chiwiwi"

offeringsController = OfferingsController()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["number"] = request.form["number"]
        session["specialization"] = request.form["specialization"]
        #TODO redirect to user page instead
        return redirect(url_for("home"))
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.pop("name", None)
    session.pop("number", None)
    session.pop("specialization", None)
    return redirect(url_for("home"))

    
@app.route("/offerings")
def offerings():
    return render_template("offerings.html", content=offeringsController.getOfferings)



if __name__ == "__main__":
    app.run()