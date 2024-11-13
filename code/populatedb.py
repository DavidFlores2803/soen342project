from app import db, create_app
from models.models import Admin, Client, Instructor, Lesson, TimeSlot, Offering, Location, Schedule, DayOfTheWeek
from werkzeug.security import generate_password_hash
from datetime import datetime


def populate_database():
    clients_data = [
        {'name': 'Sydney Campbell', 'age': 21, 'username': 'syd', 'password': 'password100'},
        {'name': 'David Flores', 'age': 22, 'username': 'david', 'password': 'password101'},
        {'name': 'Bilel Fekih', 'age': 22, 'username': 'bilel', 'password': '123viva'},
        {'name': 'Jimmy', 'age': 10, 'username': 'jim', 'password': 'password102', 'guardian_id': 1}
    ]

    admin_data = [
        {'username': 'admin', 'password': 'password'}
    ]

    instructors_data = [
        {'name': 'Aurora Blackwood', 'age': 30, 'username': 'aurora_blackwood', 'phone': '123-456-7890', 'password': 'instructor123'},
        {'name': 'Jasper Vance', 'age': 28, 'username': 'jasper_vance', 'phone': '987-654-3210', 'password': 'instructor456'},
        {'name': 'Indigo Wilder', 'age': 33, 'username': 'indigo_wilder', 'phone': '555-666-7777', 'password': 'instructor789'},
        {'name': 'Felix Storm', 'age': 27, 'username': 'felix_storm', 'phone': '333-444-5555', 'password': 'instructor101'},
        {'name': 'Nova Rain', 'age': 35, 'username': 'nova_rain', 'phone': '444-555-6666', 'password': 'instructor202'},
        {'name': 'Dante Hawke', 'age': 32, 'username': 'dante_hawke', 'phone': '777-888-9999', 'password': 'instructor303'},
    ]

    lesson_data = [
        {'name': 'Yoga for Beginners', 'lesson_type': 'Yoga', 'description': 'A beginner-level yoga class for all ages.', 'capacity': 20, 'location_name': 'Downtown Studio', 'location_city': 'Montreal'},
        {'name': 'Advanced Swimming', 'lesson_type': 'Swimming', 'description': 'An intensive swimming class for experienced swimmers.', 'capacity': 15, 'location_name': 'Uptown Pool', 'location_city': 'Montreal'},
        {'name': 'Boxing Basics', 'lesson_type': 'Boxing', 'description': 'An introductory class for boxing fundamentals.', 'capacity': 25, 'location_name': 'Central Gym', 'location_city': 'Montreal'},
        {'name': 'Dance Fusion', 'lesson_type': 'Dance', 'description': 'A mix of dance styles for fitness and fun.', 'capacity': 30, 'location_name': 'Dance Loft', 'location_city': 'Montreal'},
        {'name': 'Pilates Core Strength', 'lesson_type': 'Pilates', 'description': 'Focus on core strength with this pilates class.', 'capacity': 20, 'location_name': 'Wellness Center', 'location_city': 'Montreal'},
    ]

    time_slot_data = [
        {'lesson_name': 'Yoga for Beginners', 'day_of_week': 'Monday', 'start_time': '2024-11-12 10:00:00', 'end_time': '2024-11-12 11:00:00', 'is_available': True},
        {'lesson_name': 'Advanced Swimming', 'day_of_week': 'Monday', 'start_time': '2024-11-12 12:00:00', 'end_time': '2024-11-12 13:00:00', 'is_available': True},
        {'lesson_name': 'Boxing Basics', 'day_of_week': 'Tuesday', 'start_time': '2024-11-13 09:00:00', 'end_time': '2024-11-13 11:00:00', 'is_available': True},
        {'lesson_name': 'Dance Fusion', 'day_of_week': 'Wednesday', 'start_time': '2024-11-14 15:00:00', 'end_time': '2024-11-14 16:30:00', 'is_available': True},
        {'lesson_name': 'Pilates Core Strength', 'day_of_week': 'Thursday', 'start_time': '2024-11-15 08:00:00', 'end_time': '2024-11-15 09:00:00', 'is_available': True},
        {'lesson_name': 'Yoga for Beginners', 'day_of_week': 'Friday', 'start_time': '2024-11-16 11:00:00', 'end_time': '2024-11-16 12:00:00', 'is_available': True},
        {'lesson_name': 'Dance Fusion', 'day_of_week': 'Saturday', 'start_time': '2024-11-17 13:00:00', 'end_time': '2024-11-17 14:30:00', 'is_available': True},
    ]

    location_data = [
        {'name': 'Downtown Studio', 'city': 'Montreal', 'address': '123 Main St'},
        {'name': 'Uptown Pool', 'city': 'Montreal', 'address': '456 Elm St'},
        {'name': 'Central Gym', 'city': 'Montreal', 'address': '789 Oak Ave'},
        {'name': 'Dance Loft', 'city': 'Montreal', 'address': '101 Pine Blvd'},
        {'name': 'Wellness Center', 'city': 'Montreal', 'address': '202 Maple St'},
    ]

    schedule_data = [
        {'lesson_id': 1, 'time_slot_id': 1},
        {'lesson_id': 2, 'time_slot_id': 2},
        {'lesson_id': 3, 'time_slot_id': 3},
        {'lesson_id': 4, 'time_slot_id': 4},
        {'lesson_id': 5, 'time_slot_id': 5},
        {'lesson_id': 1, 'time_slot_id': 6},
        {'lesson_id': 4, 'time_slot_id': 7},
    ]

    # Populating locations
    for data in location_data:
        existing_location = Location.query.filter_by(name=data['name'], city=data['city']).first()
        if existing_location:
            continue

        location = Location(
            name=data['name'],
            city=data['city'],
            address=data['address']
        )
        db.session.add(location)  # Add location to session

    db.session.commit()  # Commit to create locations in the database

    # Populating clients
    for data in clients_data:
        existing_client = Client.query.filter_by(username=data['username']).first()
        if existing_client:
            continue
        
        client = Client(
            name=data['name'],
            age=data['age'],
            username=data['username'],
            password_hash=generate_password_hash(data['password'])
        )
        if 'guardian_id' in data:
            client.add_guardian(data['guardian_id'])
        db.session.add(client)  # Add client to session

    # Populating admin
    for data in admin_data:
        existing_admin = Admin.query.filter_by(username=data['username']).first()
        if existing_admin:
            continue
        
        admin = Admin(
            username=data['username'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(admin)  # Add admin to session

    # Populating instructors
    for data in instructors_data:
        existing_instructor = Instructor.query.filter_by(username=data['username']).first()
        if existing_instructor:
            continue

        instructor = Instructor(
            name=data['name'],
            age=data['age'],
            username=data['username'],
            phone=data['phone'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(instructor)  # Add instructor to session
   
   # Populate lessons
    for data in lesson_data:
        existing_lesson = Lesson.query.filter_by(name=data['name']).first()
        if existing_lesson:
            continue

        # Retrieve location by name
        location = Location.query.filter_by(name=data['location_name']).first()
        if not location:
            print(f"Location {data['location_name']} not found.")
            continue

        # Create the lesson object
        lesson = Lesson(
            name=data['name'],
            lesson_type=data['lesson_type'],
            description=data['description'],
            capacity=data['capacity'],
            location=location  # Assign the Location object directly
        )

        db.session.add(lesson)  # Add lesson to session

    db.session.commit()

    # Populate time slots
    for slot_data in time_slot_data:
        lesson = Lesson.query.filter_by(name=slot_data['lesson_name']).first()
        if lesson:
            start_time = datetime.strptime(slot_data['start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(slot_data['end_time'], '%Y-%m-%d %H:%M:%S')
        
        # Create time slot and associate it with the lesson
            time_slot = TimeSlot(
                day_of_week=slot_data['day_of_week'],
                start_time=start_time,
                end_time=end_time,
                lesson_id=lesson.lesson_id,
                is_available=slot_data['is_available']
            )
            time_slot.lesson = lesson
            db.session.add(time_slot) 

    db.session.commit()

    # Populate offerings
    admin = Admin.query.first()  # Assuming there's only one admin
    instructors = Instructor.query.all()  # Get all instructors

    for lesson in Lesson.query.all():
        # Assign the first instructor to the first lesson
        offering = Offering(
            lesson_id=lesson.lesson_id,
            instructor_id=instructors[0].instructor_id,
        )
        db.session.add(offering)
    db.session.commit()

    # Populate schedules
    for data in schedule_data:
        print(data)
        lesson = Lesson.query.filter_by(lesson_id=data['lesson_id']).first()
        time_slot = TimeSlot.query.filter_by(id=data['time_slot_id']).first()

        schedule = Schedule(
            lesson=lesson,
            time_slot = time_slot
        )
        db.session.add(schedule)
    
    db.session.commit()  
    print("Database populated with sample client, admin, instructor, lesson, time slot, location, and offering data.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # db.drop_all()
        # db.create_all()  
        # #populate_database()
        offerings = Offering.query.all()
        for offering in offerings:
            if offering.schedule is None:
                db.session.delete(offering)
                db.session.commit()
