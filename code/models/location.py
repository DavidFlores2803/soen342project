class Location:
    def __init__(self, name, city): #, availability, lesson):
        self.name = name
        self.city = city
        # self.availability = availability
        # self.lesson = lesson

    def updateAvailabilities(self, availabilities):
        self.availabilities = availabilities

    def __str__(self):
        return f"{self.name}, in {self.city}"