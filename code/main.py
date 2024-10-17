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

    return render_template("offerings.html", offerings=generateOfferings())

def generateOfferings():
    # Create sample lessons
    math_lesson = Lesson("Mathematics", "Online", "1 hour")
    science_lesson = Lesson("Science", "In-Person", "1.5 hours")
    history_lesson = Lesson("History", "Online", "2 hours")
    art_lesson = Lesson("Art", "In-Person", "2 hours")
    music_lesson = Lesson("Music", "Online", "30 minutes")

    # Create a list of offerings with different locations and availabilities
    offerings_list = [
        Offering(1, math_lesson, "New York", ["Monday 9 AM", "Wednesday 11 AM"]),
        Offering(2, science_lesson, "Los Angeles", ["Tuesday 2 PM", "Thursday 4 PM"]),
        Offering(3, history_lesson, "Chicago", ["Friday 1 PM", "Saturday 3 PM"]),
        Offering(4, art_lesson, "San Francisco", ["Monday 10 AM", "Thursday 2 PM"]),
        Offering(5, music_lesson, "Seattle", ["Tuesday 3 PM", "Friday 5 PM"]),
    ]

    return offerings_list



if __name__ == "__main__":
    app.run()