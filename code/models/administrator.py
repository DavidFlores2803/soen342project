from controllers.offeringsController import OfferingsController
from models.instructor import Instructor
from models.client import Client

class Administrator:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.offerings_controller = OfferingsController()
        self.clients = []
        self.instructors = []
    
    """
    What can the admin do?

    1. Add an offering

    //should be able to create a new Offering with these attributes
    //once added it is added to the DB
     self.location = location
        self.lesson = lesson
        self.date = date
        self.timeSlot = timeSlot
        self.instructor = instructor

    2. Delete an offering

      self.id = id
        self.lesson = lesson
        self.location = location
        self.availabilities = availabilities

    delete the offering with the respective id

    3. Can delete/add a client account

    4. can delete/add an instructor account


    Temporary -> delete from list
    Future -> delete from DB
    
    """
    def addClient(self, client):
        self.clients.append(client)

    def addInstructor(self, instructor):
        self.instructors.append(instructor)

    def addOffering(self, lesson, location, availabilities):
        new_offering_id = self.offerings_controller.addOfferring(lesson, location, availabilities)
        return new_offering_id
    
    def deleteOffering(self, id):
        offering_list = self.offerings_controller.getOfferings()
        
        offering_to_delete = None
        for offering in offering_list:
                if offering.id == id:
                    offering_to_delete = offering
                break
    
        
        if offering_to_delete:
            offering_list.remove(offering_to_delete)
            return offering_list
        else:
            print("Offering not found")
            return None
   
    
    def deleteAccount(self, account_type, account_username):
        if account_type == "client":
            for client in self.clients:
                if client.username == account_username:
                    self.clients.remove(client)
        elif account_type == "instructor":
            for instructor in self.instructors:
                if instructor.username == instructor:
                    self.instructors.remove(instructor)
        else:
            print("Error with account type")


   

    





   

