from flask import Flask, json, request
from utopia import app
from utopia.service.Airline import Airline
import logging

AIRLINE_SERVICE = Airline()

@app.route('/airlines/add/airport', methods=['POST'])
def addAirport():

    return AIRLINE_SERVICE.create_airport(request.json)


@app.route('/airlines/read/airport')
def readAllAirports():

    return AIRLINE_SERVICE.read_airport()



@app.route('/airlines/find/airport/id=<iata_id>', methods=['GET'])
def findAirport(iata_id):

    return AIRLINE_SERVICE.find_airport(iata_id)

@app.route('/airlines/read/routes_by_airport/<direction>/id=<iata_id>', methods=['GET'])
def readRoutesByAirport(direction, iata_id):

    return AIRLINE_SERVICE.read_routes_by_airport(direction, iata_id)



@app.route('/airlines/update/airport', methods=['PUT'])
def updateAirport():

    return AIRLINE_SERVICE.update_airport(request.json) 


@app.route('/airlines/delete/airport/id=<iata_id>', methods=['DELETE'])
def deleteAirport(iata_id):

    AIRLINE_SERVICE.delete_airport(iata_id)
    return ''


@app.route('/airlines/read/route', methods=['GET'])
def readAllRoutes():

    return AIRLINE_SERVICE.read_route()


@app.route('/airlines/find/route/id=<route_id>', methods=['GET'])
def findRoute(route_id):

    return AIRLINE_SERVICE.find_route(route_id)
    

@app.route('/airlines/add/route', methods=['POST'])
def addRoute():

    return AIRLINE_SERVICE.add_route(request.json)

@app.route('/airlines/update/route', methods=['PUT'])
def updateRoute():

    return AIRLINE_SERVICE.update_route(request.json)
  





    # cur = db.connection.cursor()
    # result_value = cur.execute('SELECT * FROM airport')
    

    # columns = [x[0] for x in cur.description]
    # data = cur.fetchall()
    # json_data = []
    # for result in data:
    #     json_data.append(dict(zip(columns, result)))

    # logging.info("Select all airports from utopia.airports", json_data)