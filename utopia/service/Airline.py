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

    def create_airport(self, airport):

        logging.info("Create Airport")
        logging.info(airport)
        
        new_airport = Airport(iata_id= airport['iata_id'], city = airport['city'])
        session = Session()
        
        session.add(new_airport)

        new_airport = AIRPORT_SCHEMA.dump([new_airport])
        session.commit()

        session.close()

        return jsonify({'airport' : new_airport})

    
    def read_airport(self):

        logging.info("Reading all airports")


        session = Session()
        airports = session.query(Airport).all()
        session.close()

        return jsonify({'airports':AIRPORT_SCHEMA.dump(airports)})

    def find_airport(self, iata_id):

        logging.info("Finding airport %s" %iata_id)

        session = Session()
        airport = session.query(Airport).filter_by(iata_id=iata_id).first()

        airport = AIRPORT_SCHEMA.dump([airport])

        session.close()
        return airport[0]

    def update_airport(self, airport):
        logging.info("Update airport")
        logging.info(airport)
        
        session = Session()
        airport_to_update = session.query(Airport).filter_by(iata_id=airport['iata_id']).first()
        airport_to_update.city = airport['city']
        
        session.commit()

        airport_to_update = AIRPORT_SCHEMA.dump([airport_to_update])
        session.close()

        return airport_to_update[0]


    def delete_airport(self, iata_id):
        logging.info("Delete airport iata_id = %s" %iata_id)

        session = Session()

        session.query(Airport).filter_by(iata_id=iata_id).delete()
        session.commit()
        session.close()

        return

    

  ############################################# Routes ###################################################


    def add_route(self, route):
        logging.info("Create Route")
        logging.info(route)

        new_route = Route(**route)

        session = Session()
        session.add(new_route)
        session.commit()

        new_route = ROUTE_SCHEMA.dump([new_route])
        session.close()

        return jsonify({'route' : new_route})

    
    def read_route(self):

        logging.info("Reading all routes")

        session = Session()

        routes = session.query(Route).all()

        session.close()

        return jsonify({"routes": ROUTE_SCHEMA.dump(routes)})

    def find_route(self, id):

        logging.info("Finding route %s" %id)

        session = Session()

        route = session.query(Route).filter_by(id=id).first()

        route = ROUTE_SCHEMA.dump([route])
        session.close()
        return route[0]


    def update_route(self, route):

        logging.info("Update route")

        session = Session()

        route_to_update = session.query(Route).filter_by(id=route['id']).first()

        if(route['origin_id'] != None):
            route_to_update.origin_id = route['origin_id']
        if(route['destination_id'] != None):
            route_to_update.destination_id = route['destination_id']
        
        session.commit()
        route_to_update = ROUTE_SCHEMA.dump([route_to_update])
        
        session.close()

        return route_to_update[0]


    def read_routes_by_airport(self, direction, iata_id):
        logging.info("Finding inbounding and outgoing flights to/from %s" %iata_id)

        routes = None

        session = Session()

        airport = session.query(Airport).filter_by(iata_id=iata_id).first()
        if(direction == 'incoming'):
            routes = airport.incoming
        elif(direction == 'outgoing'):
            routes = airport.outgoing

        session.close()

        return jsonify({"routes": ROUTE_SCHEMA.dump(routes)})

        

        
    
    











