from flask import request
from secret_santa import app
from secret_santa.controller_service import ParticipantService
from secret_santa.controller.controller_functions import get_http_response


@app.route('/participant', methods=['POST'])
def create_participant():
    service = ParticipantService()
    response = service.create(request.json)
    return get_http_response(response)


@app.route('/participant/<id>', methods=['PUT'])
def update_participant(id):
    service = ParticipantService()
    response = service.update(request.json, id)
    return get_http_response(response)


@app.route('/participant/<id>', methods=['DELETE'])
def delete_participant(id):
    service = ParticipantService()
    response = service.delete(id)
    return get_http_response(response)


@app.route('/participant', methods=['GET'])
def retrieve_participant():
    service = ParticipantService()
    response = service.retrieve_all()
    return get_http_response(response)


@app.route('/participant/<id>', methods=['GET'])
def retrieve_participant_by_id(id):
    service = ParticipantService()
    response = service.retrieve_by_id(id)
    return get_http_response(response)
