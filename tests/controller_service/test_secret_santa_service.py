import pytest
from secret_santa.controller_service import SecretSantaService
from unittest.mock import patch
from secret_santa.model import Participant


@pytest.fixture(scope="module")
def santa_service(session):
    with patch('secret_santa.repository.repository.Repository.db_session',
               new=session):
        santa_service = SecretSantaService()
        yield santa_service


@pytest.fixture(scope='module')
def sample_data(santa_service):
    participant1 = Participant("person1", 1, "test1@example.com")
    participant2 = Participant("person2", 1, "test2@example.com")
    participant3 = Participant("person3", 2, "test3@example.com")
    participant4 = Participant("person4", 2, "test4@example.com")
    participant5 = Participant("person5", 3, "test5@example.com")
    santa_service.repo.create(participant1)
    santa_service.repo.create(participant2)
    santa_service.repo.create(participant3)
    santa_service.repo.create(participant4)
    santa_service.repo.create(participant5)


def test_start(sample_data, santa_service):
    with patch('secret_santa.util.email_sender.EmailSender.send'):
        response = santa_service.start()
        print(response.data)
        assert(response.status_code == 200)
        count = santa_service.repo.num_people_without_giftee()
        assert(count == 0)
