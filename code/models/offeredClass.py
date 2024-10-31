class OfferedClass:
    def __init__(self, id, location, lesson, date, timeSlot, instructor):
        self.id = id
        self.location = location
        self.lesson = lesson
        self.date = date
        self.timeSlot = timeSlot
        self.instructor = instructor

    def __str__(self):
        return f"{self.location}, {self.lesson}, {self.date}, {self.timeSlot}, {self.instructor}"