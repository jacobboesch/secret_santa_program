import pytest
from secret_santa.repository import Repository
from secret_santa.model import Participant


@pytest.fixture(scope='module')
def repo(session):
    repo = Repository(Participant)
    repo.db_session = session
    return repo


@pytest.fixture(scope='module')
def add_test_data(repo):
    participant = Participant("test_user", 1, "test@example.com")
    participant2 = Participant("test_user2", 2, "test2@example.com")
    repo.create(participant)
    repo.create(participant2)


def test_create(repo):
    participant = Participant("test_user", 1, "test@example.com")
    participant = repo.create_and_return(participant)
    assert(participant.id is not None)
    assert(participant.name == "test_user")
    assert(participant.household == 1)
    assert(participant.email == "test@example.com")
    assert(participant.is_selected is False)
    assert(participant.giftee is None)



def test_retrieve_all(repo, add_test_data):
    participants = repo.retrieve_all()
    assert(len(participants) > 0)


def test_retrieve_by_id(repo, add_test_data):
    participant = repo.retrieve_by_id(1)
    assert(participant is not None)


def test_update(repo, add_test_data):
    participant = repo.retrieve_by_id(1)
    participant.name = "New Name"
    new_participant = repo.update_and_return(participant)
    assert(new_participant.name == "New Name")
    assert(new_participant.id == 1)


def test_delete(repo):
    participant = Participant("DELETE ME", 1, "nope@example.com")
    participant = repo.create_and_return(participant)
    participant_id = participant.id
    repo.delete(participant)
    participant = repo.retrieve_by_id(participant_id)
    assert(participant is None)
