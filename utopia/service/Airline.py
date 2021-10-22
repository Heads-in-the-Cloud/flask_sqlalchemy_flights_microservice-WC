from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields

from utopia.models.Airport import Airport, Route
from utopia import Session

import logging, json, traceback

logging.basicConfig(level=logging.INFO)

ma = Marshmallow(app)



class RouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Route
        ordered = True
    id = auto_field()
    origin_id = auto_field()
    destination_id = auto_field()

class AirportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        ordered = True
    iata_id = auto_field()
    city = auto_field()
    # incoming = fields.List(fields.Nested(RouteSchema))
    # outgoing= fields.List(fields.Nested(RouteSchema))


AIRPORT_SCHEMA = AirportSchema(many=True)
ROUTE_SCHEMA = RouteSchema(many=True)

class Airline:

    def __init__(self):
	    self = self

    def createAirport(self, airport):

        logging.info("Create Airport")
        logging.info(airport)
        
        new_airport = Airport(iata_id= airport['iata_id'], city = airport['city'])
        session = Session()
        
        session.add(new_airport)

        # logging.info("Adding routes to the database if any are listed") FUNCTIONALITY NOT NEEDED

        # for route in airport['incoming']:
        #    session.add(Route(origin_id=route['origin_id'], destination_id=route['destination_id']))

        # for route in airport['outgoing']:
        #     session.add(Route(origin_id=route['origin_id'], destination_id=route['destination_id']))

        new_airport = AIRPORT_SCHEMA.dump([new_airport])
        session.commit()

        session.close()

        return jsonify({'airport' : new_airport})

    
    def readAirport(self):

        logging.info("Reading all airports")
        
        json_data = []

        session = Session()
        airports = session.query(Airport).all()
        session.close()

        return jsonify({'airports':AIRPORT_SCHEMA.dump(airports)})


    def updateAirport(self, airport):
        logging.info("Update airport")
        logging.info(airport)
        
        session = Session()
        airport_to_update = session.query(Airport).filter_by(iata_id=airport['iata_id']).first()
        airport_to_update.city = airport['city']
        session.commit()

        airport_to_update = AIRPORT_SCHEMA.dump([airport_to_update])
        session.close()

        return jsonify({'airport' : airport_to_update})


    
    def addRoute(self, route):
        logging.info("Create Route")
        logging.info(route)

        new_route = Route(**route)

        session = Session()
        session.add(new_route)
        session.commit()

        new_route = ROUTE_SCHEMA.dump([new_route])
        session.close()

        return jsonify({'route' : new_route})

    
    def readRoute(self):

        logging.info("Reading all routes")

        session = Session()

        routes = session.query(Route).all()
        route_schema = RouteSchema(many=True)
        session.close()

        return jsonify({"routes": route_schema.dump(routes)})

        

        
    
    











