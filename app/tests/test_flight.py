import unittest
from flask import Flask, json
from utopia import app
import random, logging, datetime
from datetime import time

from utopia.service.flight_service import FlightService
from utopia.service.airplane_service import AirplaneService
from utopia.service.airport_service import AirportService


FLIGHT_SERVICE = FlightService()
AIRPLANE_SERVICE = AirplaneService()
AIRPORT_SERVICE = AirportService()

TEST_DATA_DATE = '2022-01-01T00:00:00'
TEST_DATA_RESERVED_SEATS = 1
TEST_DATA_SEAT_PRICE = 99.99





def setup_flight():
    logging.info("set up flight")
    airplanes = AIRPLANE_SERVICE.read_airplanes().json['airplanes']
    routes = AIRPORT_SERVICE.read_routes().json['routes']
    

    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2150, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    random_date  = datetime.datetime.combine(random_date, time()) 

    airplane_id = airplanes[random.randint(0, len(airplanes)-1)]['id']
    route_id = routes[random.randint(0, len(routes)-1)]['id']
    flight = {'airplane_id': airplane_id, 'route_id' : route_id, 'departure_time': str(random_date),
    'reserved_seats' : TEST_DATA_RESERVED_SEATS, 'seat_price' : TEST_DATA_SEAT_PRICE}  

    return flight


def teardown_flight(id):
    logging.info("tear down flight")
    print('tearing down flight %d' %id)

    FLIGHT_SERVICE.delete_flight(id)

    logging.info("flight deleted")




class TestAirline(unittest.TestCase):
    
    def test_flight(self):
        with app.app_context():

            flight = setup_flight()
            flight = FLIGHT_SERVICE.add_flight(flight)


            # self.assertEqual(flight['departure_time'], TEST_DATA_DATE)
            self.assertEqual(flight['reserved_seats'], TEST_DATA_RESERVED_SEATS)
            self.assertEqual(flight['seat_price'], TEST_DATA_SEAT_PRICE)
            teardown_flight(flight['id'])
    
    def test_update(self):
        with app.app_context():

            flight = setup_flight()
            flight = FLIGHT_SERVICE.add_flight(flight)

            flight_to_update = {'id' : flight['id'], 'reserved_seats': 100}

            flight_to_update = FLIGHT_SERVICE.update_flight(flight_to_update)

            # self.assertEqual(flight_to_update['departure_time'], TEST_DATA_DATE)
            self.assertNotEqual(flight_to_update['reserved_seats'], TEST_DATA_RESERVED_SEATS)
            self.assertEqual(flight_to_update['seat_price'], TEST_DATA_SEAT_PRICE)

            teardown_flight(flight['id'])
    
    def test_read_airplane(self):
        with app.app_context():

            airplane_id = AIRPLANE_SERVICE.read_airplanes().json['airplanes'][0]['id']

            flights = FLIGHT_SERVICE.read_flights_by_airplane(airplane_id).json['flights']
            for flight in flights:
                self.assertEqual(flight['airplane_id'], airplane_id)

    def test_read_route(self):
        with app.app_context():

            route_id = AIRPORT_SERVICE.read_routes().json['routes'][0]['id']

            flights = FLIGHT_SERVICE.read_flights_by_route(route_id).json['flights']
            print(flights)
            for flight in flights:
                self.assertEqual(flight['route_id'], route_id)

    def test_add_many(self):
        with app.app_context():
            flights = []
            for i in range(5):
                flights.append(setup_flight())
            flight_ids = [flight['id'] for flight in FLIGHT_SERVICE.add_flights(flights).json['flights']]

            flight_id_library = list(map(lambda x : x['id'], FLIGHT_SERVICE.read_flights().json['flights']))

            for flight_id in flight_ids:
                self.assertEqual(flight_id_library.count(flight_id), 1)
                teardown_flight(flight_id)

    
        


            


