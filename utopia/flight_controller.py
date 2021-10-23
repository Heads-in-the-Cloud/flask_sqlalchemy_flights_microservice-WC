from flask import Flask, json, request
from utopia import app
from utopia.service.flight_service import FlightService
import logging


FLIGHT_SERVICE = FlightService()


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
def addFlight():
    
    return FLIGHT_SERVICE.add_flight(request.json)


@app.route('/airlines/add/flights', methods=['POST'])
def addFlights():
    
    return FLIGHT_SERVICE.add_flights(request.json)

################### PUT ###################


@app.route('/airlines/update/flight', methods=['PUT'])
def updateFlight():
    
    return FLIGHT_SERVICE.update_flight(request.json)



################### DELETE ###################

@app.route('/airlines/delete/flight/id=<id>', methods=['DELETE'])
def deleteFlight(id):
    
    return FLIGHT_SERVICE.delete_flight(id)
