from secret_santa import app
from secret_santa.controller_service import SecretSantaService
from secret_santa.controller.controller_functions import get_http_response


@app.route('/email_participants', methods=['GET'])
def email_participants():
    service = SecretSantaService()
    response = service.start()
    return get_http_response(response)
