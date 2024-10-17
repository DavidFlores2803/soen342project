class Offering():
    def __init__(self, id, lesson, location, availabilities):
        self.id = id
        self.lesson = lesson
        self.location = location
        self.availabilities = availabilities

    def availabilitiesToStringHelper(self):
        string = ""
        for avail in self.availabilities:
            string += f"\n {avail}"

        return string


    def __str__(self):
        availabilities = self.availabilitiesToStringHelper()
        return f"The {self.location} is available for {self.lesson.name} classes on {availabilities}"