# Email Selection Input
# used for sending the emails to participants
# validates the input
from secret_santa.model.input.json_input import JsonInput

class SelectionInput(JsonInput):
    email = ""
    name = ""
    giftee = ""

    def __init__(self, email="", name="", giftee=""):
        self.email = email
        self.name = name
        self.giftee = giftee
        super().__init__()

    # TODO add code to validate input
    
