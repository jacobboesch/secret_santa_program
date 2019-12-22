# used to preform CRUD operations on the participant table
from secret_santa.controller_service import CRUDService
from secret_santa.model import Participant


class ParticipantService(CRUDService):

    def __init__(self):
        super().__init__(Participant)

    def get_model_json_object(self, model):
        return {
            "id": model.id,
            "name": model.name,
            "household": model.household,
            "email": model.email,
            "giftee": model.giftee,
            "is_selected": model.is_selected
        }

    def get_table_model(self, json_input):
        model = self.table(
            json_input.get("name"),
            json_input.get("household"),
            json_input.get("email"))
        return model
