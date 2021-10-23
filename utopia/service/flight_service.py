from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy

from utopia.models.models import Route, Airplane, Flight, FLIGHT_SCHEMA, FLIGHT_SCHEMA_MANY

from utopia import Session

import logging, json, traceback, datetime

logging.basicConfig(level=logging.INFO)


class FlightService:
    

################### GET ###################

    def read_flights(self):

        logging.info('reading all flights')

        session = Session()

        flights = session.query(Flight).all()

        flights = FLIGHT_SCHEMA_MANY.dump(flights)

        session.close()
        return jsonify({'flights' : flights})


    def find_flight(self, id):

        logging.info('finding flight with id %s ' %id)

        session = Session()

        flight = session.query(Flight).filter_by(id=id).first()
        flight = FLIGHT_SCHEMA.dump(flight)
        
        session.close()

        return flight


    def read_flights_by_airplane(self, id):

        logging.info('finding flights by airplane id %s ' %id)

        session = Session()

        flights = session.query(Airplane).filter_by(id=id).first().flights

        flights = FLIGHT_SCHEMA_MANY.dump(flights)

        session.close()

        return jsonify({'flights' : flights})

    def read_flights_by_route(self, id):

        logging.info('finding flights by route id %s' %id)

        session = Session()

        flights = session.query(Route).filter_by(id=id).first().flights

        flights = FLIGHT_SCHEMA_MANY.dump(flights)

        session.close()

        return jsonify({'flights' : flights})


################### POST ###################

    def add_flight(self, flight):
        
        logging.info('adding flight')

        departure_time = datetime.datetime.strptime(flight['departure_time'], '%Y-%m-%d %H:%M:%S')
        session = Session()
        flight_to_add = Flight(id=None,
        airplane_id=flight['airplane_id'], 
        route_id = flight['route_id'],
        departure_time=departure_time, 
        reserved_seats=flight['reserved_seats'], 
        seat_price=flight['seat_price'])


        print("///////////////////////////////////////////////")
        print("///////////////////////////////////////////////")
        print("///////////////////////////////////////////////")
        print("///////////////////////////////////////////////")
        print("///////////////////////////////////////////////")
        print(flight_to_add)
        session.add(flight_to_add)

        session.flush()
        session.commit()
        flight_to_add = FLIGHT_SCHEMA.dump(flight_to_add)
        session.close()
        return flight