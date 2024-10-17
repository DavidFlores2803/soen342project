class TimeSlot:
    def __init__(self, day, startTime, endTime):
        self.day = day
        self.startTime = startTime
        self.endTime = endTime

    def __str__(self):
        return f"{self.day.name.lower()}s from {self.startTime} to {self.endTime}"