class Availability:
    def __init__(self, timeSlot, startDate, endDate):
        self.timeSlot = timeSlot
        self.startDate = startDate
        self.endDate = endDate
        self.isAvailable = True

    def __str__(self):
        isAvailable = "available" if self.isAvailable else "unavailable"
        return f"{self.timeSlot}, from {self.startDate.strftime("%x")} to {self.endDate.strftime("%x")} is {isAvailable}"