from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password