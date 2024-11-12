from enum import Enum

class DayOfTheWeek(Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7

class TimeSlot:
    def __init__(self, day, startTime, endTime, isAvailable=True):
        self.day = day
        self.startTime = startTime
        self.endTime = endTime
        self.isAvailable = isAvailable

    @staticmethod
    def stringToObj(string):
        arr = string.split(",")
        day = TimeSlot.findDayOfWeek(arr[0])
        start = float(arr[1])
        end = float(arr[2])
        return TimeSlot(day, start, end)

    @staticmethod
    def findDayOfWeek(day):
        for dayOfWeek in DayOfTheWeek:
            if dayOfWeek.name.lower() == day:
                return dayOfWeek
        raise ValueError(f"Invalid day: {day}")

    def __eq__(self, other):
        return (
            self.day == other.day and
            self.startTime == other.startTime and
            self.endTime == other.endTime
        )

    def __str__(self):
        availability = 'available' if self.isAvailable else 'taken'
        return f"{self.day.name.lower()},{self.startTime},{self.endTime},{availability}"

    def markAsTaken(self):
        self.isAvailable = False
