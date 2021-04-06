from secret_santa.controller_service.email_service import EmailService
from secret_santa import app
from flask import request
from secret_santa.controller.controller_functions import get_http_response


@app.route('/email_participants', methods=['POST'])
def email_participants():
    service = EmailService()
    # TODO add JSON validation before sending emails
    response = service.email_participants(request.json)
    return get_http_response(response)
