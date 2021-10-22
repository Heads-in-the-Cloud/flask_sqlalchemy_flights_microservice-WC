import unittest
from flask import Flask, json, jsonify
from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import count
from utopia import app
import random

from utopia.service.Airline import AIRPORT_SCHEMA, Airline


AIRLINE_SERVICE = Airline()



IATA_ID_1 = 'AAA'
IATA_ID_2 = 'BBB'
CITY = 'CITY'


class TestAirline(unittest.TestCase):


    @classmethod
    def setUpClass(cls):

        print('set up class')

        with app.app_context():
            airport1 = {'iata_id' : IATA_ID_1, 'city':CITY}
            airport2 = {'iata_id' : IATA_ID_2, 'city':CITY}

            AIRLINE_SERVICE.create_airport(airport1)
            AIRLINE_SERVICE.create_airport(airport2)

            route = {'origin_id' : IATA_ID_1, 'destination_id' : IATA_ID_2}
            AIRLINE_SERVICE.add_route(route)


    @classmethod
    def tearDownClass(cls):
        print('tear down class')

        with app.app_context():
            AIRLINE_SERVICE.delete_airport(IATA_ID_1)
            AIRLINE_SERVICE.delete_airport(IATA_ID_2)
            pass

    def test_read_airport(self):
        print('test read airport')

        with app.app_context():
            airports = AIRLINE_SERVICE.read_airports()
            self.assertEqual(list(map(lambda x: x['iata_id'], airports.json['airports'])).count(IATA_ID_1), 1)

    def test_update_airport(self):
        print("test update airport")
        
        with app.app_context():
            airport = {'iata_id': IATA_ID_1, 'city' : 'hello world'}
            AIRLINE_SERVICE.update_airport(airport)
            updated_airport = AIRLINE_SERVICE.find_airport(IATA_ID_1)

            self.assertEqual(updated_airport['iata_id'], IATA_ID_1)
            self.assertEqual(updated_airport['city'], 'hello world')

    
    def test_read_route(self):
        print("test read route")

        with app.app_context():
            routes = AIRLINE_SERVICE.read_routes().json['routes']
            
            routes = list(filter(lambda x: x['origin_id'] == IATA_ID_1, routes))
            self.assertEqual(len(routes), 1)
            self.assertEqual(routes[0]['destination_id'], IATA_ID_2)

    def test_update_route(self):
        print("test update route")

        with app.app_context():

            routes = AIRLINE_SERVICE.read_routes().json['routes']
            route = list(filter(lambda x : x['origin_id'] == IATA_ID_1, routes))[0]
            route_id = route['id']
            route = {'id':route_id, 'origin_id':IATA_ID_2, 'destination_id': IATA_ID_1}
        
            AIRLINE_SERVICE.update_route(route)

            routes = AIRLINE_SERVICE.read_routes().json['routes']

            routes = list(filter(lambda x: x['origin_id'] == IATA_ID_2, routes))
            self.assertEqual(len(routes), 1)
            self.assertEqual(routes[0]['destination_id'], IATA_ID_1)


    def test_read_incoming_routes(self):
        print("test read incoming routes")

        with app.app_context():

            airports = AIRLINE_SERVICE.read_airports().json['airports']
            random_iata_id = airports[random.randint(0, len(airports))]['iata_id']

            print("incoming routes to airport %s" %random_iata_id)

            incoming_routes = AIRLINE_SERVICE.read_routes_by_airport('incoming', random_iata_id).json['routes']

            for route in incoming_routes:
                self.assertEqual(route['destination_id'], random_iata_id)

    def test_read_incoming_routes(self):
            print("test read outgoing routes")

            with app.app_context():

                airports = AIRLINE_SERVICE.read_airports().json['airports']
                random_iata_id = airports[random.randint(0, len(airports))]['iata_id']
                print("outgoing routes from airport %s" %random_iata_id)

                incoming_routes = AIRLINE_SERVICE.read_routes_by_airport('outgoing', random_iata_id).json['routes']

                for route in incoming_routes:
                    self.assertEqual(route['origin_id'], random_iata_id)



if __name__ == '__main__':
    unittest.main()