from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy


from utopia.models.flights import AIRPORT_SCHEMA_MANY, ROUTE_SCHEMA, ROUTE_SCHEMA_MANY, Airport, Route, AIRPORT_SCHEMA
from utopia.models.base import db_session

import logging, json, traceback

logging.basicConfig(level=logging.INFO)

NUM_ROUTES_PER_PAGE = 50

class AirportService:



############ GET ############


    def read_airports(self):

        logging.info("Reading all airports")


        airports = Airport.query.all()

        airports = jsonify({'airports' : AIRPORT_SCHEMA_MANY.dump(airports)})
        db_session.close()

        return airports



    def find_airport(self, iata_id):

        logging.info("Finding airport %s" %iata_id)
        airport = db_session.query(Airport).get(iata_id)
        airport = AIRPORT_SCHEMA.dump(airport)
        db_session.close()

        return airport

    def read_routes(self):

            logging.info("Reading all routes")

            routes = db_session.query(Route).all()
            # routes = Route.query.paginate(per_page=NUM_ROUTES_PER_PAGE, page=page)

            routes =  jsonify({"routes": ROUTE_SCHEMA_MANY.dump(routes)})
            db_session.close()

            return routes

    def find_route(self, id):

        logging.info("Finding route %s" %id)


        route = db_session.query(Route).filter_by(id=id).first()

        route = ROUTE_SCHEMA.dump(route)
        db_session.close()
        return route

    def read_routes_by_airport(self, direction, iata_id):
        logging.info("Finding inbounding and outgoing flights to/from %s" %iata_id)

        routes = None


        airport = db_session.query(Airport).filter_by(iata_id=iata_id).first()
        if(direction == 'incoming'):
            routes = airport.incoming
        elif(direction == 'outgoing'):
            routes = airport.outgoing

        routes = jsonify({"routes": ROUTE_SCHEMA_MANY.dump(routes)})

        db_session.close()

        return routes


    

############ POST ############


    def create_airport(self, airport):

        logging.info("Create Airport")
        logging.info(airport)
        
        new_airport = Airport(iata_id= airport['iata_id'], city = airport['city'])
        
        db_session.add(new_airport)

        db_session.commit()
        new_airport = AIRPORT_SCHEMA.dump(new_airport)

        db_session.close()

        return new_airport


    def add_route(self, route):
            logging.info("Create Route")
            logging.info(route)

            new_route = Route(**route)

            db_session.add(new_route)
            db_session.commit()

            new_route = ROUTE_SCHEMA.dump(new_route)
            db_session.close()

            return new_route


############ PUT ############


    def update_airport(self, airport):
        logging.info("Update airport")
        logging.info(airport)

        airport_to_update = db_session.query(Airport).filter_by(iata_id=airport['iata_id']).first()
        airport_to_update.city = airport['city']
        
        db_session.commit()

        airport_to_update = AIRPORT_SCHEMA.dump(airport_to_update)
        db_session.close()

        return airport_to_update

    def update_route(self, route):

            logging.info("Update route")

    
            route_to_update = db_session.query(Route).filter_by(id=route['id']).first()

            if(route['origin_id'] != None):
                route_to_update.origin_id = route['origin_id']
            if(route['destination_id'] != None):
                route_to_update.destination_id = route['destination_id']
            
            db_session.commit()
            route_to_update = ROUTE_SCHEMA.dump(route_to_update)
            db_session.close()
           
            return route_to_update



############ DELETE ############


    def delete_airport(self, iata_id):
        logging.info("Delete airport iata_id = %s" %iata_id)


        db_session.query(Airport).filter_by(iata_id=iata_id).delete()
        db_session.commit()
        db_session.close()

        return ''

    def delete_route(self, id):

        logging.info("Deleting route with id %s" %id)

        db_session.query(Route).filter_by(id=id).delete()
      
        db_session.commit()

        db_session.close()

        return ''

    



 
    
 



 






        

        
    
    











