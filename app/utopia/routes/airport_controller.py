from flask import Flask, json, request, make_response, render_template, jsonify
from utopia.models.flights import AIRPORT_SCHEMA_MANY, ROUTE_SCHEMA_MANY
from utopia import app
from utopia.service.airport_service import AirportService
import logging

AIRLINE_SERVICE = AirportService()



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

    return AIRLINE_SERVICE.read_routes(1) 


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
def addAirport():

    return AIRLINE_SERVICE.create_airport(request.json)


@app.route('/airlines/add/airport/test', methods=['POST'])
def addAirportTest():

    AIRLINE_SERVICE.add_airports_test(request.json)
    return ''

@app.route('/airlines/add/route', methods=['POST'])
def addRoute():

    return AIRLINE_SERVICE.add_route(request.json)


################### PUT ###################


@app.route('/airlines/update/airport', methods=['PUT'])
def updateAirport():

    return AIRLINE_SERVICE.update_airport(request.json)


@app.route('/airlines/update/route', methods=['PUT'])
def updateRoute():

    return AIRLINE_SERVICE.update_route(request.json)


################### DELETE ###################


@app.route('/airlines/delete/airport/id=<iata_id>', methods=['DELETE'])
def deleteAirport(iata_id):

    AIRLINE_SERVICE.delete_airport(iata_id)
    return ''


@app.route('/airlines/delete/route/id=<id>', methods=['DELETE'])
def deleteRoute(id):

    return AIRLINE_SERVICE.delete_route(id)

