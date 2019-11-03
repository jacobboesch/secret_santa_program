from secret_santa.model import ParticipantInput


def test_init_from_json():
    try:
        participant_input = ParticipantInput()
        participant_input.init_from_json({
            "name": "test",
            "email": "test@example.com",
            "household": 1
            }
        )
        assert(participant_input.name == "test")
        assert(participant_input.email == "test@example.com")
        assert(participant_input.household == 1)
    except Exception as e:
        assert(e is None)


def test_fail_init_from_json():
    try:
        participant_input = ParticipantInput()
        participant_input.init_from_json({
            "name": "test"
            }
        )
    except Exception as e:
        assert(e is not None)
