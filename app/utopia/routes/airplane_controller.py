from flask import Flask, json, request, make_response
from utopia.models.users import refresh_token
from utopia import app
from utopia.service.airplane_service import AirplaneService
from utopia.models.users import find_user
import logging
from flask_jwt_extended import get_current_user, JWTManager, jwt_required

AIRPLANE_SERVICE = AirplaneService()

jwt = JWTManager(app)
ADMIN = 1

################### GET ###################
   


@app.route('/airlines/read/airplanes', methods=['GET'])
def readAirplanes():

    return AIRPLANE_SERVICE.read_airplanes()

@app.route('/airlines/find/airplane/id=<id>', methods=['GET'])
def findAirplane(id):

    return AIRPLANE_SERVICE.find_airplane(id)

@app.route('/airlines/read/airplane_types', methods=['GET'])
def readAirplaneTypes():

    return AIRPLANE_SERVICE.read_airplane_types()

@app.route('/airlines/find/airplane_type/id=<id>', methods=['GET'])
def findAirplaneType(id):

    return AIRPLANE_SERVICE.find_airplane_type(id)


@app.route('/airlines/read/airplanes/type=<id>', methods=['GET'])
def readAirplaneByType(id):

    return AIRPLANE_SERVICE.read_airplane_by_type(id)


################### POST ###################


@app.route('/airlines/add/airplane', methods=['POST'])
@jwt_required()
def addAirplane():

    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRPLANE_SERVICE.add_airplane(request.json)


@app.route('/airlines/add/airplane_type', methods=['POST'])
@jwt_required()
def addAirplaneType():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)
    return AIRPLANE_SERVICE.add_airplane_type(request.json)


################### PUT ###################


@app.route('/airlines/update/airplane', methods=['PUT'])
@jwt_required()
def updateAirplane():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRPLANE_SERVICE.update_airplane(request.json)


@app.route('/airlines/update/airplane_type', methods=['PUT'])
@jwt_required()
def updateAirplaneType():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)
    return AIRPLANE_SERVICE.update_airplane_type(request.json)

################### DELETE ###################


@app.route('/airlines/delete/airplane/id=<id>', methods=['DELETE'])
@jwt_required()
def deleteAirplane(id):
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)
    return AIRPLANE_SERVICE.delete_airplane(id)

@app.route('/airlines/delete/airplane_type/id=<id>', methods=['DELETE'])
@jwt_required()
def deleteAirplaneType(id):
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRPLANE_SERVICE.delete_airplane_type(id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return find_user(identity)

@app.after_request
def refresh_expiring_jwts(response):
    return refresh_token(response)



