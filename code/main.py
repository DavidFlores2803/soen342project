from flask import Flask, redirect, url_for, request, render_template, session
from enums.DayOfTheWeek import DayOfTheWeek
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
    # Create sample locations
    location1 = Location("EV Building", "Montreal")
    location2 = Location("Engineering Building", "Los Angeles")
    location3 = Location("History Hall", "Chicago")
    location4 = Location("Art Center", "San Francisco")
    location5 = Location("Music Hall", "Seattle")

    # Create sample lessons
    math_lesson = Lesson("Mathematics", "Online", "1 hour")
    science_lesson = Lesson("Science", "In-Person", "1.5 hours")
    history_lesson = Lesson("History", "Online", "2 hours")
    art_lesson = Lesson("Art", "In-Person", "2 hours")
    music_lesson = Lesson("Music", "Online", "30 minutes")

    # Create sample time slots
    math_time_slots = [TimeSlot(DayOfTheWeek.MONDAY, 10, 15), TimeSlot(DayOfTheWeek.WEDNESDAY, 14, 18)]
    science_time_slots = [TimeSlot(DayOfTheWeek.TUESDAY, 13, 19), TimeSlot(DayOfTheWeek.THURSDAY, 15, 21)]
    history_time_slots = [TimeSlot(DayOfTheWeek.FRIDAY, 9, 15), TimeSlot(DayOfTheWeek.SATURDAY, 12, 18)]
    art_time_slots = [TimeSlot(DayOfTheWeek.MONDAY, 11, 17), TimeSlot(DayOfTheWeek.THURSDAY, 13, 17)]
    music_time_slots = [TimeSlot(DayOfTheWeek.WEDNESDAY, 10, 12.5), TimeSlot(DayOfTheWeek.FRIDAY, 17, 22)]

    # Create a list of offerings with different locations and time slots
    offerings_list = [
        Offering(1, math_lesson, location1, math_time_slots),
        Offering(2, science_lesson, location2, science_time_slots),
        Offering(3, history_lesson, location3, history_time_slots),
        Offering(4, art_lesson, location4, art_time_slots),
        Offering(5, music_lesson, location5, music_time_slots),
    ]

    return offerings_list



if __name__ == "__main__":
    app.run()