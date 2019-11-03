from secret_santa.repository import Repository
from secret_santa.model import Participant
from sqlalchemy import func


class ParticipantRepository(Repository):

    def __init__(self):
        super().__init__(Participant)

    # Returns the most populated house hold id from a list of participants
    # that don't have giftee's
    def retrieve_most_populated_household_id_without_giftee(self):
        most_populated_house = self.db_session.query(
            Participant.household,
            func.count(Participant.id)
            ).filter(
                Participant.giftee == None
            ).group_by(Participant.household).first()
        if(most_populated_house is not None):
            return most_populated_house.household
        else:
            return None

    def num_people_without_giftee(self):
        num_people = self.db_session.query(func.count(Participant.id)) \
                     .filter(Participant.giftee == None).first()
        if(num_people is not None):
            return num_people[0]
        else:
            return None

    def retrieve_random_not_selected_not_in_household(self, household_id):
        participant = self.db_session.query(Participant) \
                        .filter(Participant.household != household_id) \
                        .filter(Participant.is_selected == False) \
                        .order_by(func.random()).first()
        return participant

    # returns a person in the household who does not have a giftee
    def retrieve_by_household_without_giftee(self, household_id):
        participant = self.db_session.query(Participant) \
                        .filter(Participant.household == household_id) \
                        .filter(Participant.giftee == None) \
                        .order_by(func.random()).first()
        return participant
