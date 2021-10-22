from flask import Flask, json, render_template, request, jsonify
from utopia import app
from utopia.models import Airport
from utopia.service.Airline import Airline
import logging

AIRLINE_SERVICE = Airline()

@app.route('/airlines/add/airport', methods=['POST'])
def addAirport():

    return AIRLINE_SERVICE.createAirport(request.json)


@app.route('/airlines/read/airport')
def readAllAirports():

    return AIRLINE_SERVICE.readAirport()

@app.route('/airlines/update/airport', methods=['PUT'])
def updateAirport():

    return AIRLINE_SERVICE.updateAirport(request.json) 


@app.route('/airlines/read/route', methods=['GET'])
def readAllRoutes():

    return AIRLINE_SERVICE.readRoute()
    
    


@app.route('/airlines/add/route', methods=['POST'])
def addRoute():

    return AIRLINE_SERVICE.addRoute(request.json)
  





    # cur = db.connection.cursor()
    # result_value = cur.execute('SELECT * FROM airport')
    

    # columns = [x[0] for x in cur.description]
    # data = cur.fetchall()
    # json_data = []
    # for result in data:
    #     json_data.append(dict(zip(columns, result)))

    # logging.info("Select all airports from utopia.airports", json_data)