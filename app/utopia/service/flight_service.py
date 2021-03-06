from flask import Flask, app, jsonify
from flask.helpers import make_response
from flask_sqlalchemy import SQLAlchemy
from utopia.models.flights import ROUTE_SCHEMA, FlightSchema, Route, Airplane, Flight, FLIGHT_SCHEMA, FLIGHT_SCHEMA_MANY

from utopia.models.base import db_session

import logging, json, traceback, datetime


logging.basicConfig(level=logging.INFO)


HOURS_IN_DAY = 24
SECONDS_IN_HOUR = 3600


def generate_f_ids(length):
    flights = db_session.query(Flight).all()
    start_id = flights[len(flights)-1].id +1 if len(flights) >0 else 1
    return [x for x in range(start_id, start_id+length)]

def check_departure_time(departure_time, airplane_id):
    flight_service = FlightService()

    flights = list(map(lambda x : datetime.datetime.strptime(x['departure_time'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
    , flight_service.read_flights_by_airplane(airplane_id).json['flights']))
    for existing_time in flights:
        
        delta = abs(departure_time - existing_time)
  
        if delta.days*HOURS_IN_DAY+delta.seconds/SECONDS_IN_HOUR < HOURS_IN_DAY * 2:
            return False
    return True



class FlightService:
    

################### GET ###################


    def find_flight(self, id):

        logging.info('finding flight with id %s ' %id)

    
        flight = db_session.query(Flight).filter_by(id=id).first()
        flight = FLIGHT_SCHEMA.dump(flight)
        
        db_session.close()
   
        return flight


    def read_flights(self):

        logging.info('reading all flights')

    
        flights = db_session.query(Flight).all()
       
        flights = FLIGHT_SCHEMA_MANY.dump(flights)

        db_session.close()
    
        return jsonify({'flights' : flights})


    def read_flights_by_airplane(self, id):

        logging.info('finding flights by airplane id %s ' %id)

    
        flights = db_session.query(Airplane).filter_by(id=id).first().flights

        flights = FLIGHT_SCHEMA_MANY.dump(flights)

        db_session.close()
    
        return jsonify({'flights' : flights})

    def read_flights_by_route(self, id):

        logging.info('finding flights by route id %s' %id)

    
        flights = db_session.query(Route).filter_by(id=id).first().flights

        flights = FLIGHT_SCHEMA_MANY.dump(flights)

        db_session.close()
    
        return jsonify({'flights' : flights})


################### POST ###################

    def add_flight(self, flight):
        
        logging.info('adding flight')

    
        try:
            departure_time = datetime.datetime.strptime(flight['departure_time'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        except:
            raise ValueError()
        
        if not check_departure_time(departure_time, flight['airplane_id']):
            return make_response('Flights of the same airplane cannot take place within 48 hours', 400)

        flight_to_add = Flight(id=None if 'id' not in flight else flight['id'],
            airplane_id=flight['airplane_id'], 
            route_id = flight['route_id'],
            departure_time=departure_time, 
            reserved_seats=flight['reserved_seats'], 
            seat_price="{:.2f}".format(flight['seat_price']))

        
        db_session.add(flight_to_add)
        db_session.commit()
        flight_to_add = FLIGHT_SCHEMA.dump(flight_to_add)

        db_session.close()

        return flight_to_add


    def add_flights(self, flights):

        logging.info('adding flight')
    
        flights_to_add = []

        for flight, flight_id in zip(flights, generate_f_ids(len(flights))):
            
            try:
                departure_time = datetime.datetime.strptime(flight['departure_time'].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
            except:
                raise ValueError()

            flight_to_add = Flight(id=flight_id,
            airplane_id=flight['airplane_id'], 
            route_id = flight['route_id'],
            departure_time=departure_time, 
            reserved_seats=flight['reserved_seats'], 
            seat_price="{:.2f}".format(flight['seat_price']))

            flights_to_add.append(flight_to_add)
            
        db_session.bulk_save_objects(flights_to_add)


        db_session.commit()
        

        flights_to_add = FlightSchema(many=True, exclude=['route', 'airplane']).dump(flights_to_add)


        db_session.close()
   
        return jsonify({"flights" : flights_to_add})


################### PUT ###################


    def update_flight(self, flight):
        
        logging.info('updating flight')

    
        flight_to_update = db_session.query(Flight).filter_by(id=flight['id']).first()


        if 'airplane_id' in flight:
            flight_to_update.airplane_id = flight['airplane_id']

        if 'route_id' in flight:
            flight_to_update.route_id = flight['route_id']
        
        if 'departure_time' in flight:
            flight_to_update.departure_time = datetime.datetime.strptime(flight['departure_time'], '%Y-%m-%d %H:%M:%S')

        if 'reserved_seats' in flight:
            flight_to_update.reserved_seats = flight['reserved_seats']

        if 'seat_price' in flight:
            flight_to_update.seat_price = "{:.2f}".format(flight['seat_price'])
    
        db_session.commit()
        flight_to_update = FLIGHT_SCHEMA.dump(flight_to_update)

        db_session.close()

        return flight_to_update


################### DELETE ###################

    def delete_flight(self, id):

        logging.info("deleting flight")

    
        db_session.query(Flight).filter_by(id=id).delete()

        db_session.commit()
        db_session.close()
        return ''

