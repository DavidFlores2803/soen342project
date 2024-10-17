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





def main():
    generateData()

if __name__ == '__main__':
    main()