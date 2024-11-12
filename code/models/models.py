from app import db
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

class BookingStatus(Enum):
    BOOKED = "booked"
    CANCELED = "canceled"
    COMPLETED = "completed"

class OfferingStatus(Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    CANCELED = "canceled"

class DayOfTheWeek(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('clients.client_id', name='fk_client_id'), nullable=True)

    guardian = db.relationship('Client', backref=db.backref('guardians', lazy=True), remote_side=[client_id])  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'Client with name {self.name}'

class Instructor(db.Model):
    __tablename__ = 'instructors'
    instructor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    specialization = db.Column(db.String(128))
    phone = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
         return f'Instructor with name {self.name}'

class Admin(db.Model):
     __tablename__ = 'admin'
     admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     username = db.Column(db.String(128), unique=True, nullable=False)
     password_hash = db.Column(db.String(128), nullable=False)
     
     #admin should have acces to the list of client and instructor objects
     #admin should have access to the list of offerings
     def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
     def check_password(self, password):
        return check_password_hash(self.password_hash, password)
     
     #all methods below should be able to
     """
     a) directly add an offering to the data base
     b) directly delete an offering to the database
     c) directly delete an instructor account from the database
     d) directly delete a client account from the database
     e) directly add a client account to the database (from registration method)
     f) directly add an instructor account to the database (from registration method)
     """
     def addOffering(self, lesson, instructor):
        
        new_offering = Offering(
            lesson_id=lesson.lesson_id,  
            instructor_id=instructor.instructor_id  
        )
        
        
        db.session.add(new_offering)
        db.session.commit()
        
        return new_offering.offering_id
     
     def createLesson(self, name, lesson_type, description, capacity):
     
        existing_lesson = Lesson.query.filter_by(name=name).first()
        if existing_lesson:
            return f"Lesson with the name '{name}' already exists."

        new_lesson = Lesson(
            name=name,
            lesson_type=lesson_type,
            description=description,
            capacity=capacity
        )
        
        db.session.add(new_lesson)
        db.session.commit()
        
        return f"Lesson '{name}' created successfully!"
     
     def deleteOffering(self, id):
         offering_to_delete = Offering.query.get(id)  
    
         if offering_to_delete:
            db.session.delete(offering_to_delete) 
            db.session.commit() 
            return True
         else:
            return False
            

        
    #delete based on username (unique) and account type (different sections)
     def deleteAccount(self, account_type, account_username):
        if account_type == "client":
            client = Client.query.filter_by(username=account_username).first()
            if client:
                db.session.delete(client)
                db.session.commit()
        
        elif account_type == "instructor":
            instructor = Instructor.query.filter_by(username=account_username).first()
            if instructor:
                db.session.delete(instructor)
        else:
            print("Not valid account type")

     def __repr__(self):
        return f'Admin with name {self.name}'

#lesson does not have an instructor
# lesson is not posted to the public 
#if lesson available, instructor can take it, and once taken it turns into an offering
class Lesson(db.Model):
    __tablename__ = 'lessons'
    lesson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    lesson_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    offerings = db.relationship('Offering', backref='lesson', lazy=True)
    lesson_time_slots = db.relationship('TimeSlot', back_populates='lesson', lazy=True)
    is_available = db.Column(db.Boolean, default=True)

    def __init__(self, name, lesson_type, description, capacity, is_available=True):
        self.name = name
        self.lesson_type = lesson_type
        self.description = description
        self.capacity = capacity
        self.is_available = is_available
       
    #temporary until figure out 
    def mark_as_available(self):
        self.is_available = True
    
    def mark_as_taken(self):
        self.is_available = False


    def add_time_slot(self, day, start_time, end_time):
        time_slot = TimeSlot(
            day=day,
            start_time=start_time,
            end_time=end_time,
            lesson_id=self.lesson_id
        )
        db.session.add(time_slot)
        db.session.commit()

    def get_available_time_slots(self):
        available_slots = []
        schedules = Schedule.query.filter_by(lesson_id=self.lesson_id).all()
        for schedule in schedules:
            if schedule.time_slot.is_available:  # Assuming time_slot is available
                available_slots.append(schedule)
        return available_slots


    def get_taken_time_slots(self):
        return [slot for slot in self.time_slots if not slot.isAvailable]

    def mark_time_slot_taken(self, day, start_time, end_time):
        time_slot = self._find_time_slot(day, start_time, end_time)
        if time_slot:
            time_slot.markAsTaken()

    def mark_time_slot_available(self, day, start_time, end_time):
        time_slot = self._find_time_slot(day, start_time, end_time)
        if time_slot:
            time_slot.markAsAvailable()

    def _find_time_slot(self, day, start_time, end_time):
        for slot in self.time_slots:
            if slot.day == day and slot.startTime == start_time and slot.endTime == end_time:
                return slot
        return None

#offering is a lesson with an instructor
#add corresponding instructor relationship
#offering is posted to the public
class Offering(db.Model):
    __tablename__ = 'offerings'
    offering_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey('lessons.lesson_id', name='fk_lesson_id'),
        nullable=False
    )
    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey('instructors.instructor_id', name='fk_instructor_id'),
        nullable=False
    )
    
    instructor = db.relationship('Instructor', backref=db.backref('offerings', lazy=True))
   
     
class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=False)
  
    def __repr__(self):
        return f'Location: {self.name}, {self.city}'
    
class Schedule(db.Model):
    __tablename__ = 'schedules'
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_of_week = db.Column(db.Enum(DayOfTheWeek), nullable=False)
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)
    
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id', name='lesson_id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id', name='instructor_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id', name='location_id'), nullable=False)
    
    lesson = db.relationship('Lesson', backref=db.backref('schedules', lazy=True))
    instructor = db.relationship('Instructor', backref=db.backref('schedules', lazy=True))
    location = db.relationship('Location', backref=db.backref('schedules', lazy=True))

    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id', name='time_slots.id'), nullable=False)
    time_slot = db.relationship('TimeSlot', backref=db.backref('schedules', lazy=True))


    def __repr__(self):
        return f'{self.lesson.lesson_type} on {self.day_of_week.name} from {self.start_time} to {self.end_time} at {self.location.name}'

    def add_schedule(cls, lesson, instructor, location, day, start_time, end_time):
        # Create a new schedule
        new_schedule = Schedule(
            lesson_id=lesson.lesson_id,
            instructor_id=instructor.instructor_id,
            location_id=location.location_id,
            day_of_week=day,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(new_schedule)
        db.session.commit()
        return new_schedule

    @staticmethod
    def get_schedule_by_lesson(lesson_id):
        return Schedule.query.filter_by(lesson_id=lesson_id).all()
    

    def __repr__(self):
        return f'{self.lesson_type} on {self.day} from {self.start_time} to {self.end_time}'


class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.BOOKED)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id', name='fk_client_id'), nullable=False)
    
    offering_id = db.Column(db.Integer, db.ForeignKey('offerings.offering_id', name='fk_offering_id'), nullable=False)

    client = db.relationship('Client', backref=db.backref('bookings', lazy=True))
    #schedule = db.relationship('Schedule', backref=db.backref('bookings', lazy=True))
    offering = db.relationship('Offering', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
     return f'Booking of {self.client.name} for {self.offering.lesson.lesson_type} on {self.offering.lesson.day}'
    
    @classmethod
    def create_booking(cls, client, offering):
       
        if not offering or not offering.lesson:
            return "Offering not found or invalid"
        
        if offering.status == OfferingStatus.BOOKED:
            return "Offering is already booked"

        # Create the booking
        new_booking = Booking(client_id=client.client_id, offering_id=offering.offering_id)
        
        # Mark the offering as booked
        offering.status = OfferingStatus.BOOKED
        
        db.session.add(new_booking)
        db.session.commit()

        return f"Booking confirmed for {client.name} in {offering.lesson.name} on {offering.lesson.day}"


class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id', name='fk_lesson_id'), nullable=False)

    lesson = db.relationship('Lesson', back_populates='lesson_time_slots', lazy=True)

    day_of_week = db.Column(db.Enum(DayOfTheWeek), nullable=False)

    def __init__(self, day_of_week, start_time, end_time, lesson_id,is_available=True):
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.lesson_id = lesson_id 
        self.is_available = is_available

    def __repr__(self):
        return f"TimeSlot({self.day_of_week.name}, {self.start_time}, {self.end_time}, {'available' if self.is_available else 'taken'})"
    
    def mark_as_taken(self):
        self.is_available = False

    def mark_as_available(self):
        self.is_available = True

    @staticmethod
    def string_to_obj(time_slot_string):
        
        arr = time_slot_string.split(",")
        day = DayOfTheWeek[arr[0].upper()]
        start = arr[1]
        end = arr[2]
        return TimeSlot(day, start, end)
    
    @staticmethod
    def find_day_of_week(day):
        
        for day_of_week in DayOfTheWeek:
            if day_of_week.name.lower() == day.lower():
                return day_of_week
        raise ValueError(f"Invalid day: {day}")