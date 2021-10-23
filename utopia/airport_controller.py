from flask import Flask, json, request
from utopia import app
from utopia.service.airport_service import AirportService
import logging

AIRLINE_SERVICE = AirportService()


################### GET ###################


@app.route('/airlines/read/airports')
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
def addAirport():

    return AIRLINE_SERVICE.create_airport(request.json)


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

    # cur = db.connection.cursor()
    # result_value = cur.execute('SELECT * FROM airport')

    # columns = [x[0] for x in cur.description]
    # data = cur.fetchall()
    # json_data = []
    # for result in data:
    #     json_data.append(dict(zip(columns, result)))

    # logging.info("Select all airports from utopia.airports", json_data)
