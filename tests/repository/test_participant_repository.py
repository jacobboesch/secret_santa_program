import pytest
from secret_santa.repository import ParticipantRepository
from secret_santa.model import Participant
from unittest.mock import patch


@pytest.fixture(scope='module')
def participant_repository():
    repo = ParticipantRepository()
    return repo

###
# Create 5 participants
# Make sure that people in group 2 have giftees so that
# we can test the method for most populated group without giftees works
###
@pytest.fixture(scope='module')
def participant_sample_data(session, participant_repository):
    with patch(
            'secret_santa.repository.repository.Repository.db_session',
            new=session):
        participant1 = Participant("person1", 1, "test1@example.com")
        participant2 = Participant("person2", 1, "test2@example.com")
        participant3 = Participant("person3", 2, "test3@example.com")
        participant4 = Participant(
            "person4",
            2,
            "test4@example.com"
        )
        participant5 = Participant(
            "person5",
            3,
            "test5@example.com"
        )
        participant_repository.create(participant1)
        participant_repository.create(participant2)
        participant_repository.create(participant3)
        participant_repository.create(participant4)
        participant_repository.create(participant5)

def test_num_people_without_giftee(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        num_people = participant_repository.num_people_without_giftee()
        assert(num_people == 5)

def test_update_giftees(participant_repository,
    session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        try:
            participant_repository.update_giftees()
        except Exception as e:
            assert(e is None)
        
        result_set = session.execute("SELECT * FROM participants")
        for row in result_set:
            assert(row.giftee is not None)

def test_retrieve_all_with_giftee(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        session.query(Participant).update({"giftee": 1})
        participants = participant_repository.retrieve_all_with_giftee()
        assert(len(participants) == 5)


