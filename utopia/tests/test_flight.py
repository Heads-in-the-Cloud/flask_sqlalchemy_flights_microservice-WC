import unittest
from flask import Flask, json
from utopia import app
import random, logging, datetime

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
    
    airplane_id = airplanes[random.randint(0, len(airplanes)-1)]['id']
    route_id = routes[random.randint(0, len(routes)-1)]['id']
    flight = {'airplane_id': airplane_id, 'route_id' : route_id, 'departure_time': TEST_DATA_DATE,
    'reserved_seats' : TEST_DATA_RESERVED_SEATS, 'seat_price' : TEST_DATA_SEAT_PRICE}  

    return flight


def teardown_flight(id):
    logging.info("tear down flight")

    FLIGHT_SERVICE.delete_flight(id)

    logging.info("flight deleted")




class TestAirline(unittest.TestCase):
    
    def test_flight(self):
        with app.app_context():

            flight = setup_flight()
            flight = FLIGHT_SERVICE.add_flight(flight)
            self.assertEqual(flight['departure_time'], TEST_DATA_DATE)
            self.assertEqual(flight['reserved_seats'], TEST_DATA_RESERVED_SEATS)
            self.assertEqual(flight['seat_price'], TEST_DATA_SEAT_PRICE)
            teardown_flight(flight['id'])
    
    def test_update(self):
        with app.app_context():

            flight = setup_flight()
            flight = FLIGHT_SERVICE.add_flight(flight)

            flight_to_update = {'id' : flight['id'], 'reserved_seats': 100}

            flight_to_update = FLIGHT_SERVICE.update_flight(flight_to_update)

            self.assertEqual(flight['departure_time'], TEST_DATA_DATE)
            self.assertNotEqual(flight['reserved_seats'], TEST_DATA_RESERVED_SEATS)
            self.assertEqual(flight['seat_price'], TEST_DATA_SEAT_PRICE)

            teardown_flight(flight['id'])

