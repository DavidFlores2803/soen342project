from models import *
from enums.DayOfTheWeek import DayOfTheWeek
from datetime import datetime
from dateutil.relativedelta import relativedelta

locations = []

def addLocation():
    location1 = Location("EV", "MTL")
    locations.append(location1)

def generateAvailabilities():
    avails = []
    
    now = datetime.now()
    one_month_from_now = now + relativedelta(month=1)
    # return Availability(DayOfTheWeek.MONDAY, 9, 10, now, one_month_from_now)
    
    ts = TimeSlot(DayOfTheWeek.MONDAY, 12, 15)
    avails.append(Availability(ts, datetime.now(), one_month_from_now))
    return avails

def createOffering():
    availabilities = generateAvailabilities()
    lesson = Lesson("judo", "judo", 1)
    offering = Offering(0, lesson, locations[0], availabilities)
    print(offering)

def viewLocations():
    for loc in locations:
        print(loc)

def generateData():
    addLocation()
    createOffering()

def aaaaaaaaa():
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
        Offering(1, math_lesson, "location1", math_time_slots),
        Offering(2, science_lesson, "location2", science_time_slots),
        Offering(3, history_lesson, "location3", history_time_slots),
        Offering(4, art_lesson, "location4", art_time_slots),
        Offering(5, music_lesson, "location5", music_time_slots),
    ]

    for off in offerings_list:
        for ts in off.availabilities:
            print(ts)
        print("-----------")




def main():    
    aaaaaaaaa()
    # generateData()

if __name__ == '__main__':
    main()