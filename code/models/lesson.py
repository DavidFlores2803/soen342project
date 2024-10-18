class Lesson:
    def __init__(self, name, type, duration):
        self.name = name
        self.type = type
        self.duration = duration

    def __str__(self):
        return f"{self.name}, {self.type}, {self.duration}"