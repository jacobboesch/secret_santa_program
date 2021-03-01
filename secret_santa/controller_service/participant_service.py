# used to preform CRUD operations on the participant table
from secret_santa.controller_service import CRUDService
from secret_santa.model import ParticipantInput
from secret_santa.model import Participant


class ParticipantService(CRUDService):

    def __init__(self):
        super().__init__(Participant, ParticipantInput)

    def get_model_json_object(self, model):
        return {
            "id": model.id,
            "name": model.name,
            "household": model.household,
            "email": model.email
        }

    def get_table_model(self, input_object):
        # TODO add error checking for invalid email addresses and other input
        # For now I'll assume that all input is valid
        model = self.table(
            input_object.name, input_object.household, input_object.email)
        return model
