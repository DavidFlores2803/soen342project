from flask import Flask, redirect, url_for, request, render_template, session
from enums.DayOfTheWeek import DayOfTheWeek
from controllers import OfferingsController
from models import *
from models.administrator import Administrator
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.secret_key = "chiwiwi"

# account type name constants
ADMIN = "admin"
INSTRUCTOR = "instructor"
CLIENT = "client"

offeringsController = OfferingsController()
offerings_list = list()
classes_offered_list = list()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/client_login", methods=["POST", "GET"])
def client_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        number = request.form["number"]
        age = request.form["age"]
        
        session["currentAccount"] = {
            "username": username,
            "password": password,
            "name": name,
            "number": number,
            "age": age
        }

        session["accountType"] = CLIENT

        #TODO redirect to user page instead
        return redirect(url_for("home"))
    else:
        return render_template("client_login.html")

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

        session["accountType"] = INSTRUCTOR

        #TODO redirect to user page instead
        return redirect(url_for("home"))
    else:
        return render_template("instructor_login.html")
    
@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        
        if username == "admin" and password == "password":  
            session["currentAccount"] = {
                "username": username,
                "password": password,
            }
            session["accountType"] = ADMIN

            # Redirect to admin account page
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials. Please try again."
            return render_template("admin_login.html", error=error)
    else:
        return render_template("admin_login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
    
@app.route("/offerings")
def offerings():
    #TODO redirect to home if not logged in as instructor
    if len(offerings_list) == 0:
        generateOfferings()

    return render_template("offerings.html", offerings=offerings_list)

@app.route('/take_offering', methods=['POST'])
def take_offering():
    #TODO id is NOT EQUAL to arr index add a findOffering(id) method
    offering_id = int(request.form.get('offering_id'))
    time_slot = TimeSlot.stringToObj(request.form.get('time_slot'))
    
    offerings_list[offering_id].takeAvailability(time_slot)
    
    #TODO show available classes to clients and taken classes to instructors
    offeredClass = OfferedClass(
        location=offerings_list[offering_id].location,
        lesson=offerings_list[offering_id].lesson,
        date=time_slot.day,
        timeSlot=time_slot,
        instructor=session['currentAccount']['name']
    )
    classes_offered_list.append(offeredClass)

    return redirect(url_for('instructor_account'))

@app.route('/delete_offering', methods=['POST'])
def delete_offering():
    offering_id = int(request.form.get('offering_id'))

    # Create an instance of Administrator with appropriate credentials
    admin = Administrator("admin", "password")

    # Call the delete method
    success = admin.deleteOffering(offering_id)

    if success:
        return redirect(url_for('admin_account'))
    else:
        return "Offering not found", 404


@app.route('/classes_offered')
def classes_offered():
    return render_template('classes_offered.html', offered_classes=classes_offered_list)

@app.route('/instructor_account')
def instructor_account():
    return render_template('instructor_account.html', my_classes=getClassesForInstructor(session['currentAccount']['name']))

@app.route('/admin_account')
def admin_account():
    if not offeringsController.offerings:
        generateOfferings() 

    # Retrieve the offerings list from the offeringsController
    offers = offeringsController.offerings
    return render_template('admin_account.html', offered_classes=offers)

def generateOfferings():
    global offerings_list

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

    # Create sample time slots and availabilities
    now = datetime.now()
    one_month_from_now = now + relativedelta(month=1)


    math_time_slots = [TimeSlot(DayOfTheWeek.MONDAY, 10, 15), TimeSlot(DayOfTheWeek.WEDNESDAY, 14, 18)]
    science_time_slots = [TimeSlot(DayOfTheWeek.TUESDAY, 13, 19), TimeSlot(DayOfTheWeek.THURSDAY, 15, 21)]
    history_time_slots = [TimeSlot(DayOfTheWeek.FRIDAY, 9, 15), TimeSlot(DayOfTheWeek.SATURDAY, 12, 18)]
    art_time_slots = [TimeSlot(DayOfTheWeek.MONDAY, 11, 17), TimeSlot(DayOfTheWeek.THURSDAY, 13, 17)]
    music_time_slots = [TimeSlot(DayOfTheWeek.WEDNESDAY, 10, 12.5), TimeSlot(DayOfTheWeek.FRIDAY, 17, 22)]

    math_availabilities = [Availability(slot, now, one_month_from_now) for slot in math_time_slots]
    science_availabilities = [Availability(slot, now, one_month_from_now) for slot in science_time_slots]
    history_availabilities = [Availability(slot, now, one_month_from_now) for slot in history_time_slots]
    art_availabilities = [Availability(slot, now, one_month_from_now) for slot in art_time_slots]
    music_availabilities = [Availability(slot, now, one_month_from_now) for slot in music_time_slots]

    # Create a list of offerings with different locations and availabilities
    genericOfferings = [
        Offering(0, math_lesson, location1, math_availabilities),
        Offering(1, science_lesson, location2, science_availabilities),
        Offering(2, history_lesson, location3, history_availabilities),
        Offering(3, art_lesson, location4, art_availabilities),
        Offering(4, music_lesson, location5, music_availabilities),
    ]

    offerings_list.extend(genericOfferings)
    offeringsController.addOffering(math_lesson, location1, math_availabilities)
    offeringsController.addOffering(science_lesson, location2, science_availabilities)
    offeringsController.addOffering(history_lesson, location3, history_availabilities)
    offeringsController.addOffering(art_lesson, location4, art_availabilities)
    offeringsController.addOffering(music_lesson, location5, music_availabilities)

def getClassesForInstructor(name):
    #TODO should match on id not on name
    list_of_classes = []
    for class_offered in classes_offered_list:
        if class_offered.instructor == name:
            list_of_classes.append(class_offered)

    return list_of_classes

if __name__ == "__main__":
    app.run()