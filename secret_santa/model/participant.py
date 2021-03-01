# This class models the participant table
from sqlalchemy import Column, Integer, String, Boolean
from secret_santa.database import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    household = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    ###
    # This is the id of the person who you'll be shopping for
    # can be null since particpants arn't initilaized with a giftee
    ###
    giftee = Column(Integer, nullable=True)

    def __init__(self, name, household, email, giftee=None):
        self.name = name
        self.household = household
        self.email = email
        self.giftee = giftee

    def __repr__(self):
        return '<Participant %r>' % (self.name)
