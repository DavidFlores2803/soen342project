from models.account import Account

class Client(Account):
    def __init__(self, username, password,name, phone, age):
        super().__init__(username, password)
        self.name = name
        self.phone = phone
        self.age = age
    