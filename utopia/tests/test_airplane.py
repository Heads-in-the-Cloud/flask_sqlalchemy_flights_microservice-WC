import unittest
from flask import Flask, json, jsonify
from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import count
from utopia import app
import random
from utopia.AirportController import AIRLINE_SERVICE

from utopia.service.AirplaneService import AirplaneService


AIRPLANE_SERVICE = AirplaneService()


### Tests assume there exists at least 2 airplane types in database ###


def setup_airplane_type(max_capacity):
    airplane_type = {'max_capacity' : max_capacity}
    airplane_type = AIRPLANE_SERVICE.add_airplane_type(airplane_type)
    return airplane_type

def teardown_airplane_type(id):
    AIRPLANE_SERVICE.delete_airplane_type(id)

def setup_airplane():
    type_id = AIRPLANE_SERVICE.read_airplane_types().json['airplane_types'][0]['id']
    airplane = {'type_id' : type_id}
    airplane = AIRPLANE_SERVICE.add_airplane(airplane)
    return airplane

def teardown_airplane(id):

    AIRPLANE_SERVICE.delete_airplane(id)

class TestAirline(unittest.TestCase):

    
    
    def test_max_capacity(self):

        with app.app_context():

            airplane_type = setup_airplane_type(999)

            self.assertEqual(999, AIRPLANE_SERVICE.find_airplane_type(airplane_type['id'])['max_capacity'])

            teardown_airplane_type(airplane_type['id'])

    def test_type_id(self):

        with app.app_context():


            airplane = setup_airplane()
            self.assertEqual(airplane['type_id'], AIRPLANE_SERVICE.find_airplane(airplane['id'])['type_id'])

            teardown_airplane(airplane['id'])


    def test_update_airplane_type(self):

        with app.app_context():

            airplane = setup_airplane()
            airplane_type_id = AIRPLANE_SERVICE.read_airplane_types().json['airplane_types'][1]['id']

            airplane['type_id'] = airplane_type_id
            airplane = AIRPLANE_SERVICE.update_airplane(airplane)

            self.assertEqual(airplane_type_id, AIRPLANE_SERVICE.find_airplane(airplane['id'])['type_id'])

            teardown_airplane(airplane['id'])
    
    def test_update_max_capacity(self):
        with app.app_context():

            airplane_type = setup_airplane_type(999)
    
            airplane_type['max_capacity'] = 1000
            
            airplane_type = AIRPLANE_SERVICE.update_airplane_type(airplane_type)


            self.assertEqual(airplane_type['max_capacity'], AIRPLANE_SERVICE.find_airplane_type(airplane_type['id'])['max_capacity'])

            teardown_airplane_type(airplane_type['id'])
    


