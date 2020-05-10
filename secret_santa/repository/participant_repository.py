from secret_santa.repository import Repository
from secret_santa.model import Participant
from sqlalchemy import func
import random

class ParticipantRepository(Repository):

    def __init__(self):
        super().__init__(Participant)

    def num_people_without_giftee(self):
        num_people = self.db_session.query(func.count(Participant.id)) \
                        .filter(Participant.giftee == None).first()
        if(num_people is not None):
            return num_people[0]
        else:
            return None
            
    def retrieve_all_with_giftee(self):
        participants = self.db_session.query(Participant) \
                        .filter(Participant.giftee != None) \
                        .all()
        return participants

    def update_giftees(self):
        matches = []
        options = []
        taken_giftees = set()
        num_participants = 0
        sql = "SELECT P.id AS id, COUNT(G.id) AS num_possible_giftees, \
                group_concat(G.id) AS possible_giftees \
               FROM participants AS P, participants AS G \
               WHERE P.id <> G.id AND P.household != G.household \
                AND (G.id <> P.giftee OR P.giftee IS NULL) \
               GROUP BY P.id \
               ORDER BY num_possible_giftees ASC"

        result_set = self.db_session.execute(sql)
        
        for row in result_set:
            possible_giftees = set(map(int,row.possible_giftees.split(",")))
            options.append((row.id, possible_giftees))

        
        fail_count = 0
        # algorhim only gets it right about 77% of the time on the first try
        # so I'll allow for a maximum of 8 attemps to prevent an infinte loop
        while(fail_count < 8):
            try:
                matches.clear()
                taken_giftees.clear()
                for option in options:
                    possible_giftees = list(option[1] - taken_giftees)
                    if(len(possible_giftees) == 0):
                        raise Exception("Failed to find a giftee")
                    random.shuffle(possible_giftees)
                    matches.append({
                        "id": option[0], 
                        "giftee": possible_giftees[0]
                        }
                    )
                    taken_giftees.add(possible_giftees[0])

                if(len(matches) != len(options)):
                    raise Exception("Failed")
                else: 
                    break
            except:
                fail_count += 1
        # if it failed to assign giftees 8 times then we are over 99% certain
        # that it's impossible to ever select a giftee for everyone
        if(fail_count == 8):
            raise Exception("Unable to find giftees for all participants")
        self.db_session.bulk_update_mappings(Participant, matches)
        self.db_session.commit()