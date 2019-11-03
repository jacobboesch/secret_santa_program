# used to create or update a participant in the database
from secret_santa.model import JsonInput


class ParticipantInput(JsonInput):
    email = ""
    name = ""
    household = 0

    def __init__(self, name="", email="", household=0):
        self.name = name
        self.email = email
        self.household = household
        super().__init__(self.id)
