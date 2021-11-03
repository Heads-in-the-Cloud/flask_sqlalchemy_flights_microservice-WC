from flask import Flask, json, request, make_response
from utopia import app
from utopia.service.flight_service import FlightService
import logging
from utopia.models.users import find_user, refresh_token
from flask_jwt_extended import get_current_user, JWTManager, jwt_required

FLIGHT_SERVICE = FlightService()
jwt = JWTManager(app)
TRAVELER = 3
################### GET ###################



@app.route('/airlines/read/flights', methods=['GET'])
def readFlights():
    
    return FLIGHT_SERVICE.read_flights()


@app.route('/airlines/find/flight/id=<id>', methods=['GET'])
def findFlight(id):
    
    return FLIGHT_SERVICE.find_flight(id)


@app.route('/airlines/read/flights/airplane=<id>', methods=['GET'])
def readFlightByAirplane(id):
    
    return FLIGHT_SERVICE.read_flights_by_airplane(id)

@app.route('/airlines/read/flights/route=<id>', methods=['GET'])
def readFlightByRoute(id):
    
    return FLIGHT_SERVICE.read_flights_by_route(id)


################### POST ###################


@app.route('/airlines/add/flight', methods=['POST'])
@jwt_required()
def addFlight():
    current_user = get_current_user()
    if current_user['role_id'] == TRAVELER:
        return make_response('need at least agent privileges to access this resource', 403)

    return FLIGHT_SERVICE.add_flight(request.json)


@app.route('/airlines/add/flights', methods=['POST'])
@jwt_required()
def addFlights():
    
    current_user = get_current_user()
    if current_user['role_id'] == TRAVELER:
        return make_response('need at least agent privileges to access this resource', 403)

    return FLIGHT_SERVICE.add_flights(request.json)

################### PUT ###################


@app.route('/airlines/update/flight', methods=['PUT'])
@jwt_required()
def updateFlight():
    
    current_user = get_current_user()
    if current_user['role_id'] == TRAVELER:
        return make_response('need at least agent privileges to access this resource', 403)

    return FLIGHT_SERVICE.update_flight(request.json)



################### DELETE ###################

@app.route('/airlines/delete/flight/id=<id>', methods=['DELETE'])
@jwt_required()
def deleteFlight(id):

    current_user = get_current_user()
    if current_user['role_id'] == TRAVELER:
        return make_response('need at least agent privileges to access this resource', 403)

    return FLIGHT_SERVICE.delete_flight(id)




@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return find_user(identity)

@app.after_request
def refresh_expiring_jwts(response):
    return refresh_token(response)
