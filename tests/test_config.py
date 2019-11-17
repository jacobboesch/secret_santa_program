import pytest
import secret_santa.config as config
from os import path


def test_config():
    assert(config.CONNECTION_STRING is not None)
    assert(config.SENDER_EMAIL is not None)
    assert(config.SENDER_PASSWORD is not None)
    assert(config.SMTP_SERVER is not None)
    assert(config.PORT is not None)
    assert(config.EMAIL_TEMPLATE is not None)
    assert(path.exists(config.EMAIL_TEMPLATE))
    assert(config.EMAIL_SUBJECT is not None)
    if(config.EMAIL_TEMPLATE_STYLE):
        assert(path.exists(config.EMAIL_TEMPLATE_STYLE))