from werkzeug.security import check_password_hash
from flask import Flask, flash, redirect, url_for, request, render_template, session
from sqlalchemy.orm import joinedload 
from enums.DayOfTheWeek import DayOfTheWeek

from models.models import *

from datetime import datetime
from dateutil.relativedelta import relativedelta
from app import create_app,db

app = create_app()
#app = Flask(__name__)
#app.secret_key = "chiwiwi"


# account type name constants
ADMIN = "admin"
INSTRUCTOR = "instructor"
CLIENT = "client"

with app.app_context():
    offerings_list = db.session.query(Offering).options(joinedload(Offering.lesson)).all()

    lessons_list = db.session.query(Lesson).all()
   

@app.route('/client_registration', methods=["POST", "GET"])
def client_registration():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username already exists
        client = Client.query.filter_by(username=username).first()

        if client:
            # If the username is already taken, redirect back to the registration page
            return redirect(url_for('client_registration'))

        # Create a new client if username is not already taken
        new_client = Client(name=name, age=age, username=username)
        new_client.set_password(password)

        db.session.add(new_client)
        db.session.commit()

        # Fetch the newly created client and set session details
        client = Client.query.filter_by(username=username).first()
        if client:
            session["currentAccount"] = {
                "username": client.username,
                "client_id": client.client_id,
            }
            session["accountType"] = CLIENT

        # Redirect to client login page after successful registration
        return redirect(url_for('client_login'))

    return render_template('client_registration.html')


@app.route('/instructor_registration', methods=["POST", "GET"])
def instructor_registration():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        username = request.form["username"]
        password = request.form["password"]
        phone = request.form["phone"]
        specialization = request.form["specialization"]

        instructor = Instructor.query.filter_by(username=username).first()

        if instructor:
            return redirect(url_for('instructor_registration'))

        new_instructor = Instructor(name=name, age=age, username=username, phone=phone,specialization=specialization)
        new_instructor.set_password(password)

        db.session.add(new_instructor)
        db.session.commit()

        return redirect(url_for('instructor_login'))
    
    return render_template('instructor_registration.html')


@app.route("/client_login", methods=["POST", "GET"])
def client_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        client = Client.query.filter_by(username=username).first()

        if client and check_password_hash(client.password_hash,password):

            kid = Client.query.filter_by(guardian_id=client.client_id).first()

            is_kid_account = client.age < 18
            
            session["currentAccount"] = {
                "username": client.username,
                "client_id": client.client_id,
                "is_kid_account": is_kid_account
                }
            
            if kid is not None:
                session["currentAccount"]["kid_id"] = kid.client_id

            session["accountType"] = CLIENT
        
            return redirect(url_for("home"))
        else:
            return render_template("client_login.html")
    else:
        return render_template("client_login.html")
 
@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash,password):
            session["currentAccount"] = {
                "username": admin.username,
                "client_id": admin.admin_id,
                }
            session["accountType"] = ADMIN

            return redirect(url_for("home"))
        else:
            error = "Invalid credentials. Please try again."
            return render_template("admin_login.html", error=error)
    else:
        return render_template("admin_login.html")

@app.route("/instructor_login", methods=["POST", "GET"])
def instructor_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        instructor = Instructor.query.filter_by(username=username).first()
        if instructor and check_password_hash(instructor.password_hash,password):
            session["currentAccount"] = {
                "username": instructor.username,
                "instructor_id": instructor.instructor_id,
                }
            session["accountType"] = INSTRUCTOR

            return redirect(url_for("home"))
        else:
            error = "Invalid credentials. Please try again."
            return render_template("instructor_login.html", error=error)
    else:
        return render_template("instructor_login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
    
@app.route("/offerings")
def offerings():
    offerings = Offering.query.all()
    user_bookings = Booking.query.filter_by(client_id=session['currentAccount']['client_id']).all()
    kid_bookings = None
    if session['currentAccount'].get('kid_id'):
        kid_bookings = Booking.query.filter_by(client_id=session['currentAccount']['kid_id']).all()
        
    return render_template("offerings.html", offerings=offerings, user_bookings=user_bookings, kid_bookings=kid_bookings)

#take lesson
@app.route('/take_lesson', methods=['POST'])
def take_lesson():
    lesson_id = request.form.get('lesson_id')
    instructor_id = session.get('currentAccount')['instructor_id']  
    sched_id = request.form.get('schedule_id')
    
    schedule = Schedule.query.filter_by(schedule_id=sched_id).first()
    if not schedule:
        print("Schedule not found.", "error")
        return redirect(url_for('lessons'))

    schedule.is_available = False

    # # Create a new offering for this lesson with the current instructor
    new_offering = Offering(
        lesson_id=lesson_id,
        instructor_id=instructor_id,
        shedule_id = sched_id
    )
    
    db.session.add(new_offering)
    db.session.commit()

    
    return redirect(url_for('lessons'))


@app.route('/lessons')
def lessons():
    # Fetch all lessons from the database
    lessons = Lesson.query.all()
    lesson_and_time_slots = list()

    for l in lessons:
        scheds = Schedule.query.filter_by(lesson_id=l.lesson_id).all() 
        lts = {
            'lesson' : l,
            'schedules' : scheds
        }

        lesson_and_time_slots.append(lts)

    # Render the lessons.html template and pass the lessons data
    return render_template('lessons.html', lessons=lesson_and_time_slots)

# booking a class
@app.route('/book_class', methods=['POST'])
def book_class():
    offering_id = request.form.get('offering_id')  
    is_for_child = request.form.get("for_child") == "True"

    if is_for_child:
        client_id = session.get("currentAccount")["kid_id"]
    else:
        client_id = session.get("currentAccount")["client_id"]

    booked_class = Booking(client_id=client_id, offering_id=offering_id)

    # Check if client and offering exist
    client_exists = Client.query.get(booked_class.client_id)
    offering_exists = Offering.query.get(booked_class.offering_id)

    if not client_exists:
        print(f"Client with ID {booked_class.client_id} does not exist.")
    elif not offering_exists:
        print(f"Offering with ID {booked_class.offering_id} does not exist.")
    else:
        # Only add booking if it doesn’t already exist
        existing_booking = Booking.query.filter_by(
            client_id=booked_class.client_id,
            offering_id=booked_class.offering_id
        ).first()

        if not existing_booking:
            print(f"Adding booking {booked_class.client_id}, {booked_class.offering_id} to the db")
            db.session.add(booked_class)
            db.session.commit()
        else:
            print("Booking already exists in the database.")
    
    return redirect(url_for('client_account'))


@app.route('/delete_offering', methods=['POST'])
def delete_offering():
    offering_id = request.form.get('offering_id')
    
    admin = Admin.query.first() 
   
    success = admin.deleteOffering(offering_id)
    if success:
        return redirect(url_for('admin_account'))
    else:
        return "Offering not found", 404



@app.route('/classes_offered')
def classes_offered():
    
    offered_classes = Offering.query.options(joinedload(Offering.instructor)).all()
    if session.get('currentAccount') == "CLIENT":  # User is logged in
        return render_template('classes_offered.html', offered_classes=offered_classes)
    elif session.get('currentAccount') == "ADMIN":
        return render_template('admin_account.html', offered_classes=offered_classes)
    else:  # User is not logged in
        return render_template('classes_view_only.html', offered_classes=offered_classes)


# Show all booked classes for the client
@app.route('/client_account')
def client_account():
    client_id = session.get("currentAccount")["client_id"]  
    booked_classes = db.session.query(Booking).filter(Booking.client_id == client_id).all()
    return render_template('client_account.html', classes_taken=booked_classes)


@app.route('/instructor_account')
def instructor_account():
    instructor_id = session.get('currentAccount')['instructor_id']
    my_classes = db.session.query(Offering).filter(Offering.instructor_id == instructor_id).all()
    return render_template('instructor_account.html', my_classes=my_classes)

#show list of offerings
@app.route('/admin_account')

def admin_account():
    offered_classes = Offering.query.options(joinedload(Offering.instructor)).all()
    return render_template('admin_account.html', offered_classes=offered_classes)

@app.route('/create_lesson', methods=['GET', 'POST'])
def create_lesson():
    if request.method == 'POST':
   
        lesson_name = request.form['lesson']
        lesson_type = request.form['type']
        description = request.form['description']
        capacity = request.form['capacity']
        location_id = request.form['location_id']
        time_slot_ids = request.form.getlist('time_slots_id')

        location = Location.query.get(location_id)
        time_slots = TimeSlot.query.filter(TimeSlot.id.in_(time_slot_ids)).all()

        for time_slot in time_slots:
            existing_lesson = Lesson.query.join(Lesson.lesson_time_slots).filter(TimeSlot.id == time_slot.id).first()
            if existing_lesson:
                flash(f"Lesson with the time-slot {time_slot.start_time} - {time_slot.end_time} already exists.")
                return redirect(url_for('create_lesson'))

        admin = Admin.query.first()  
        result = admin.createLesson(
            name=lesson_name,
            lesson_type=lesson_type,
            description=description,
            capacity=capacity,
            location=location,
            time_slots=time_slots
        )

        flash("lesson added!!!!!")
        return redirect(url_for('admin_lessons'))

   
    locations = Location.query.all()
    time_slots = TimeSlot.query.all()

    return render_template('create_lesson.html', locations=locations, time_slots=time_slots)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    
    return render_template('add_location.html')

@app.route('/view_locations')
def view_locations():
    locations = Location.query.all()
    return render_template('view_locations.html', locations=locations)

@app.route('/create_location', methods=['POST'])
def create_location():
    name = request.form['location_name']
    location_address = request.form['location_address']
    location_city = request.form['location_city']


    existing_location = Location.query.filter_by(name=name, city=location_city, address=location_address).first()

    if existing_location:
        #figure out alerts
        flash("this location already exists..")
        return redirect(url_for('home')) 
   
    new_location = Location(name=name, address=location_address, city=location_city)
    db.session.add(new_location)
    db.session.commit()
    flash("wohoooo added new location!")
    return redirect(url_for('home'))

@app.route('/create_timeslot', methods=['POST'])
def create_timeslot():
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    day_of_week = request.form['day_of_week']
   

    start_time_date = request.form['start_time_date']
    end_time_date = request.form['end_time_date']

    new_start = start_time_date + " " + start_time
    new_end = end_time_date + " " + end_time   

    existing_slot = TimeSlot.query.filter_by(day_of_week=day_of_week, start_time=new_start, end_time=new_end).first()

    if existing_slot:
        flash('This time-slot already exists')
        return redirect(url_for('home'))

    new_time_slot = TimeSlot(day_of_week=day_of_week,start_time=new_start, end_time=new_end)
    db.session.add(new_time_slot)
    db.session.commit()

    flash('wohooooooo')
    return redirect(url_for('home'))

@app.route('/create_timeslot_by_id', methods=['POST'])
def create_timeslot_by_id():
    lesson_id = request.form['lesson_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    day_of_week = request.form['day_of_week']
    print(request.form)
    start_time_date = request.form['start_time_date']
    print(start_time_date)
    end_time_date = request.form['end_time_date']

    new_start = start_time_date + " " + start_time
    print(new_start)
    new_end = end_time_date + " " + end_time   

    
    # start_time_obj = datetime.strptime(start_time)
    # end_time_obj = datetime.strptime(end_time)

    
    new_time_slot = TimeSlot(
        day_of_week=day_of_week,
        lesson_id=lesson_id,
        start_time=new_start,
        end_time=new_end
    )
    lesson = Lesson.query.get(lesson_id)
    new_schedule = Schedule(lesson=lesson, time_slot=new_time_slot)
    db.session.add(new_schedule)
    db.session.commit()
    
    db.session.add(new_time_slot)
    db.session.commit()

    return redirect(url_for('admin_lessons'))


@app.route('/admin_lessons')
def admin_lessons():
    lessons = Lesson.query.all()  
    for lesson in lessons:
        
        lesson.time_slots = Schedule.get_schedule_by_lesson(lesson.lesson_id)
    return render_template('admin_lessons.html', lessons=lessons)


#delete instructor
@app.route('/manage_instructors', methods=['GET', 'POST'])
def manage_instructors():
    if session.get("accountType") == ADMIN:
        
        instructors = Instructor.query.all()
        #admin_id = session.get('currentAccount', {}).get('admin_id')
        admin = Admin.query.first() 

        if request.method == 'POST':
            account_username = request.form.get('username')
    
            admin.deleteAccount("instructor", account_username)
            db.session.commit()

            return redirect(url_for('manage_instructors'))

        return render_template('manage_instructors.html', instructors=instructors)
    else:
        return redirect(url_for("home"))

@app.route('/manage_clients', methods=['GET', 'POST'])
def manage_clients():
    if session.get("accountType") == ADMIN:
        clients = Client.query.all()
        admin = Admin.query.first() 

        if request.method == 'POST':
            account_username = request.form.get('username')
            
            admin.deleteAccount("client", account_username)
            db.session.commit()
            return redirect(url_for('manage_clients'))

        return render_template('manage_clients.html', clients=clients)
    else:
        return redirect(url_for("home"))
    
# @app.route('/pick_lesson/<lesson_id>', methods=['POST'])
# def pick_lesson(lesson_id):
#     if session.get("accountType") == "INSTRUCTOR":
#         instructor_id = session.get('currentAccount', {}).get('instructor_id')
        
#         if not instructor_id:
#             return redirect(url_for("home"))
        
       
#         lesson = Lesson.query.filter_by(id=lesson_id).first()
#         if not lesson:
#             return redirect(url_for("home"))
        
       
#         instructor = Instructor.query.filter_by(id=instructor_id).first()
#         if instructor:
#             offering = Offering(lesson=lesson, instructor=instructor)
#             db.session.add(offering)
#             db.session.commit()

#             return redirect(url_for('instructor_account', message="You have successfully picked the lesson as your offering."))

#         return redirect(url_for("home"))

   
#     return redirect(url_for("home"))

# def getClassesForInstructor(name):
#     #TODO should match on id not on name
#     list_of_classes = []
#     for class_offered in classes_offered_list:
#         if class_offered.instructor == name:
#             list_of_classes.append(class_offered)

#     return list_of_classes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)