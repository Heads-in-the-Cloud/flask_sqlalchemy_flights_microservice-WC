from flask import Flask, json, request, make_response, render_template, jsonify
from utopia.models.flights import AIRPORT_SCHEMA_MANY, ROUTE_SCHEMA_MANY
from utopia import app
from utopia.service.airport_service import AirportService
from utopia.models.users import find_user, refresh_token
import logging
from flask_jwt_extended import get_current_user, JWTManager, jwt_required



AIRLINE_SERVICE = AirportService()
jwt = JWTManager(app)
ADMIN = 1


################### GET ###################



@app.route('/')
def index():
    routes = AIRLINE_SERVICE.read_routes().json['routes']
    response = make_response(render_template('airports.html', routes=routes))
    return response


@app.route('/airlines/read/airports', methods=['GET'])
def readAirports():

    return AIRLINE_SERVICE.read_airports()


@app.route('/airlines/read/routes', methods=['GET'])
def readRoutes():

    return AIRLINE_SERVICE.read_routes() 


@app.route('/airlines/find/airport/id=<iata_id>', methods=['GET'])
def findAirport(iata_id):

    return AIRLINE_SERVICE.find_airport(iata_id)


@app.route('/airlines/find/route/id=<route_id>', methods=['GET'])
def findRoute(route_id):

    return AIRLINE_SERVICE.find_route(route_id)


@app.route('/airlines/read/routes_by_airport/<direction>/id=<iata_id>', methods=['GET'])
def readRoutesByAirport(direction, iata_id):

    return AIRLINE_SERVICE.read_routes_by_airport(direction, iata_id)


################### POST ###################


@app.route('/airlines/add/airport', methods=['POST'])
@jwt_required()
def addAirport():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRLINE_SERVICE.create_airport(request.json)


@app.route('/airlines/add/airport/test', methods=['POST'])
@jwt_required()
def addAirportTest():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    AIRLINE_SERVICE.add_airports_test(request.json)
    return ''

@app.route('/airlines/add/route', methods=['POST'])
@jwt_required()
def addRoute():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRLINE_SERVICE.add_route(request.json)


################### PUT ###################


@app.route('/airlines/update/airport', methods=['PUT'])
@jwt_required()
def updateAirport():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRLINE_SERVICE.update_airport(request.json)


@app.route('/airlines/update/route', methods=['PUT'])
@jwt_required()
def updateRoute():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRLINE_SERVICE.update_route(request.json)


################### DELETE ###################


@app.route('/airlines/delete/airport/id=<iata_id>', methods=['DELETE'])
@jwt_required()
def deleteAirport(iata_id):
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    AIRLINE_SERVICE.delete_airport(iata_id)
    return ''


@app.route('/airlines/delete/route/id=<id>', methods=['DELETE'])
@jwt_required()
def deleteRoute(id):
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        return make_response('need admin priveleges to access this resource', 403)

    return AIRLINE_SERVICE.delete_route(id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return find_user(identity)

@app.after_request
def refresh_expiring_jwts(response):
    return refresh_token(response)


