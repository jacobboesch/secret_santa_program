import pytest
from secret_santa.controller_service import ParticipantService
from secret_santa.model import Participant
from unittest.mock import patch
from secret_santa.repository import Repository

###
# module so it only runs once in this file, thus all tests
# using this fixture will have the same json input
###
@pytest.fixture(scope='module')
def json_input_data():
    json_input = {
        "name": "test_user",
        "email": "me@example.com",
        "household": 1
    }
    return json_input
###
# scope is function so that they can have a different participant
# this is so we can test updating and deleting without
# interfering with each other
###
@pytest.fixture(scope='function')
def sample_participant(session):
    with patch('secret_santa.repository.Repository.db_session', new=session):
        repo = Repository(Participant)
        participant = repo.create_and_return(
            Participant("test_user", 1, "me@example.com"))
        return participant

# module scope so that they all share the same Participant service
@pytest.fixture(scope='module')
def participant_service():
    service = ParticipantService()
    return service


def test_create(session, json_input_data, participant_service):
    with patch('secret_santa.repository.Repository.db_session', new=session):
        response = participant_service.create(json_input_data)
        assert(response.status_code == 201)


def test_update(session, json_input_data,
                sample_participant, participant_service):
    response = participant_service.update(
        {"name": "New", "email": "new@example.com", "household": 1},
        sample_participant.id
    )
    print(response.json_data)
    assert(response.status_code == 200)


def test_delete(session, sample_participant, participant_service):
    with patch('secret_santa.repository.Repository.db_session', new=session):
        response = participant_service.delete(sample_participant.id)
        assert(response.status_code == 200)


def test_retrieve_all(session, sample_participant, participant_service):
    with patch('secret_santa.repository.Repository.db_session', new=session):
        response = participant_service.retrieve_all()
        assert(response.status_code == 200)
        assert(len(response.data["participants"]) > 0)


def test_retrieve_by_id(session, participant_service, sample_participant):
    with patch('secret_santa.repository.Repository.db_session', new=session):
        response = participant_service.retrieve_by_id(
            sample_participant.id)
        assert(response.status_code == 200)
        assert(response.data["name"] == sample_participant.name)
