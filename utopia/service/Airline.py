from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy


from utopia.models.Airport import AIRPORT_SCHEMA_MANY, ROUTE_SCHEMA, ROUTE_SCHEMA_MANY, Airport, Route, AIRPORT_SCHEMA
from utopia import Session

import logging, json, traceback

logging.basicConfig(level=logging.INFO)


class Airline:

    def __init__(self):
	    self = self


############ GET ############


    def read_airports(self):

        logging.info("Reading all airports")


        session = Session()
        airports = session.query(Airport).all()

        airports = AIRPORT_SCHEMA_MANY.dump(airports)
        session.close()

        return jsonify({'airports' : airports})


    def find_airport(self, iata_id):

        logging.info("Finding airport %s" %iata_id)

        session = Session()
        airport = session.query(Airport).filter_by(iata_id=iata_id).first()

        airport = AIRPORT_SCHEMA.dump(airport)

        session.close()
        return airport

    def read_routes(self):

            logging.info("Reading all routes")

            session = Session()

            routes = session.query(Route).all()

            session.close()

            return jsonify({"routes": ROUTE_SCHEMA_MANY.dump(routes)})

    def find_route(self, id):

        logging.info("Finding route %s" %id)

        session = Session()

        route = session.query(Route).filter_by(id=id).first()

        route = ROUTE_SCHEMA.dump(route)
        session.close()
        return route

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

        return jsonify({"routes": ROUTE_SCHEMA_MANY.dump(routes)})


    

############ POST ############


    def create_airport(self, airport):

        logging.info("Create Airport")
        logging.info(airport)
        
        new_airport = Airport(iata_id= airport['iata_id'], city = airport['city'])
        session = Session()
        
        session.add(new_airport)

        new_airport = AIRPORT_SCHEMA.dump(new_airport)
        session.commit()

        session.close()

        return new_airport


    def add_route(self, route):
            logging.info("Create Route")
            logging.info(route)

            new_route = Route(**route)

            session = Session()
            session.add(new_route)
            session.commit()

            new_route = ROUTE_SCHEMA.dump(new_route)
            session.close()

            return new_route


############ PUT ############


    def update_airport(self, airport):
        logging.info("Update airport")
        logging.info(airport)

        session = Session()
        airport_to_update = session.query(Airport).filter_by(iata_id=airport['iata_id']).first()
        airport_to_update.city = airport['city']
        
        session.commit()

        airport_to_update = AIRPORT_SCHEMA.dump(airport_to_update)
        session.close()

        return airport_to_update

    def update_route(self, route):

            logging.info("Update route")

            session = Session()

            route_to_update = session.query(Route).filter_by(id=route['id']).first()

            if(route['origin_id'] != None):
                route_to_update.origin_id = route['origin_id']
            if(route['destination_id'] != None):
                route_to_update.destination_id = route['destination_id']
            
            session.commit()
            route_to_update = ROUTE_SCHEMA.dump(route_to_update)
            
            session.close()

            return route_to_update



############ DELETE ############


    def delete_airport(self, iata_id):
        logging.info("Delete airport iata_id = %s" %iata_id)

        session = Session()

        session.query(Airport).filter_by(iata_id=iata_id).delete()
        session.commit()
        session.close()

        return

    def delete_route(self, id):

        logging.info("Deleting route with id %s" %id)

        session = Session()
        session.query(Route).filter_by(id=id).delete()
        
        session.commit()
        session.close()
        return ''

    



 
    
 



 






        

        
    
    











