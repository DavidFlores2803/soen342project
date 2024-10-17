from account import Account

class Instructor(Account):
    def __init__(self, username, password, name, phoneNumber, specialization):
        super.__init__(username, password)
        self.name = name
        self.phoneNumber = phoneNumber
        self.specialization = specialization