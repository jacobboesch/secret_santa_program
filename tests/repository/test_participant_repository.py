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
            "test4@example.com",
            True,
            1
        )
        participant5 = Participant(
            "person5",
            2,
            "test5@example.com",
            True,
            1
        )
        participant_repository.create(participant1)
        participant_repository.create(participant2)
        participant_repository.create(participant3)
        participant_repository.create(participant4)
        participant_repository.create(participant5)


def test_retrieve_most_populated_household_id_without_giftee(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        house_id = participant_repository. \
            retrieve_most_populated_household_id_without_giftee()
        assert(house_id == 1)


def test_num_people_without_giftee(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        num_people = participant_repository.num_people_without_giftee()
        assert(num_people == 3)


def test_retrieve_random_not_selected_not_in_household(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        participant = participant_repository. \
                        retrieve_random_not_selected_not_in_household(1)
        assert(participant is not None)
        assert(participant.household == 2)
        # using the sample data the only one that could be selected is
        # participant #3 since we forced 4, and 5 to already be selected
        assert(participant.name == "person3")


def test_retrieve_by_household_without_giftee(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        participant = participant_repository. \
                        retrieve_by_household_without_giftee(2)
        assert(participant is not None)
        assert(participant.household == 2)
        assert(participant.name == "person3")


def test_reset_giftees(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        session.query(Participant).update({"giftee": 1})
        participant_repository.reset_giftees()
        count = session.query(Participant) \
            .filter(Participant.giftee != None) \
            .count()
        assert(count == 0)


def test_unselect_all(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        session.query(Participant).update({"is_selected": True})
        participant_repository.unselect_all()
        count = session.query(Participant) \
            .filter(Participant.is_selected == True) \
            .count()
        assert(count == 0)


def test_retrieve_all_with_giftee(
        participant_repository, session, participant_sample_data):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        session.query(Participant).update({"giftee": 1})
        participants = participant_repository.retrieve_all_with_giftee()
        assert(len(participants) == 5)
