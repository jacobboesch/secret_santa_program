# This class models the participant table
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates
from secret_santa.database import Base
from secret_santa.response import ErrorException
import re


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    household = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    giftee = Column(Integer, nullable=True)
    is_selected = Column(Boolean, nullable=False)

    def __init__(self, name, household, email, is_selected=False, giftee=None):
        self.name = name
        self.household = household
        self.email = email
        self.is_selected = is_selected
        self.giftee = giftee

    @validates('email')
    def validate_email(self, key, value):
        if(re.match(r"^[a-zA-Z0-9\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~\;\.]"
                    + r"{1,64}@[a-zA-Z\-]+\.[a-zA-Z\-]+", "test@example.com")
                is None):
            raise ErrorException("Invalid Email", 400)
        return value

    @validates('name')
    def validate_name(self, key, value):
        if(re.match(r"^[a-zA-Z\-\' ]+", value) is None):
            raise ErrorException("Inavlid name", 400)
        return value

    def __repr__(self):
        return '<Participant %r>' % (self.name)
