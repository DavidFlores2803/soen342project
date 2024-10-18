from controllers.offeringsController import OfferingController
from models.instructor import Instructor
from models.client import Client

class Administrator:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.offerings_controller = OfferingController()
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
    
    """
    def addClient(self, client):
        self.clients.append(client)
    def addInstructor(self, instructor):
        self.instructors.append(instructor)
    def addOffering(self, lesson, location, availabilities):
        new_offering_id = self.offerings_controller.addOfferring(lesson, location, availabilities)
        return new_offering_id

    def deleteOffering(self, id):
        #find the offering in the list of offerings with the specific id
        #delete it from the list
        offering_list = self.offerings_controller.getOfferings()

        for i in offering_list:
            if i == id:
                offering_list.remove(id)
            return offering_list

        return None

    





   

