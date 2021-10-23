import unittest
from flask import Flask, json, jsonify
from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import count
from utopia import app
import random

from utopia.service.flight_service import FlightService


FLIGHT_SERVICE = FlightService()


class TestAirline(unittest.TestCase):
    pass