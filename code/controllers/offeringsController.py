from models import *
from enums.DayOfTheWeek import DayOfTheWeek
from datetime import datetime
from dateutil.relativedelta import relativedelta

class OfferingsController():
    id = 0
    offerings = []

    def getOfferings(self):
        return self.offerings

    def addOffering(self, lesson, location, availabilities):
        offering = Offering(id, lesson, location, availabilities)
        self.offerings.append(offering)
        id += 1
        return offering.id
    
    def generateDefaultOffering(self):
        # lesson
        lesson = Lesson("judo", "judo", 1)

        # location
        location = Location("EV", "MTL")

        # availability
        ts = TimeSlot(DayOfTheWeek.MONDAY, 12, 15)
        now = datetime.now()
        one_month_from_now = now + relativedelta(month=1)
        avail = Availability(ts, datetime.now(), one_month_from_now)

        self.addOffering(lesson, location, avail)
