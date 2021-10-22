from flask import Flask, json, request
from utopia import app
from utopia.service.AirplaneService import AirplaneService
import logging

AIRPLANE_SERVICE = AirplaneService()


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
def addAirplane():

    return AIRPLANE_SERVICE.add_airplane(request.json)


@app.route('/airlines/add/airplane_type', methods=['POST'])
def addAirplaneType():

    return AIRPLANE_SERVICE.add_airplane_type(request.json)


################### PUT ###################


@app.route('/airlines/update/airplane', methods=['PUT'])
def updateAirplane():

    return AIRPLANE_SERVICE.update_airplane(request.json)


@app.route('/airlines/update/airplane_type', methods=['PUT'])
def updateAirplaneType():

    return AIRPLANE_SERVICE.update_airplane_type(request.json)

################### DELETE ###################


@app.route('/airlines/delete/airplane/id=<id>', methods=['DELETE'])
def deleteAirplane(id):

    return AIRPLANE_SERVICE.delete_airplane(id)

@app.route('/airlines/delete/airplane_type/id=<id>', methods=['DELETE'])
def deleteAirplaneType(id):

    return AIRPLANE_SERVICE.delete_airplane_type(id)





