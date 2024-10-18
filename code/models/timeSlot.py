from enum import Enum

#TODO use other enum instead of doubling them
class DayOfTheWeek(Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7

class TimeSlot:
    def __init__(self, day, startTime, endTime):
        self.day = day
        self.startTime = startTime
        self.endTime = endTime

    def stringToObj(string):
        arr = string.split(",")
        day = TimeSlot.findDayOfWeek(arr[0])
        start = float(arr[1])
        end = float(arr[2])
        return TimeSlot(day, start, end)
    
    def findDayOfWeek(day):
        for dayOfWeek in DayOfTheWeek:
            if dayOfWeek.name.lower() == day:
                return dayOfWeek

    def __eq__(self, other):
        return (
            self.day.name == other.day.name and
            self.startTime == other.startTime and
            self.endTime == other.endTime
        )

    def __str__(self):
        return f"{self.day.name.lower()},{self.startTime},{self.endTime}"
        # return f"{self.day.name.lower()}s from {self.startTime} to {self.endTime}"