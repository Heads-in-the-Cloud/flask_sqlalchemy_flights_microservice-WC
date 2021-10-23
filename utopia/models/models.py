from flask import Flask, app

from sqlalchemy.sql.expression import false, null
from sqlalchemy.sql.selectable import subquery
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
from sqlalchemy import Sequence
from utopia import db
from sqlalchemy.dialects.mysql import FLOAT

import json

from sqlalchemy.sql.sqltypes import DateTime



Base = declarative_base()
ma = Marshmallow(app)


def generate_f_id():
    flight_ids = db.session.execute('SELECT id FROM flight')
    i=1
    for id in flight_ids:
        
        if i == id[0]:
            i+=1
        else:
            break
    return i


######################################## TABLES ########################################

class Airport(db.Model):
    __tablename__ = 'airport'


    iata_id = db.Column(db.String(3), primary_key=True)
    city =  db.Column(db.String(45))
    outgoing = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.origin_id")
    incoming = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.destination_id")


class Route(db.Model):
    __tablename__ = 'route'


    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.String(3) , db.ForeignKey("airport.iata_id"))
    origin_id =  db.Column(db.String(3) , db.ForeignKey("airport.iata_id"))
    flights = relationship('Flight', backref='route', lazy='subquery', cascade='all, delete')


class AirplaneType(db.Model):
    __tablename__ = 'airplane_type'

    id = db.Column(db.Integer, primary_key=True)
    max_capacity = db.Column(db.Integer)
    airplanes = relationship("Airplane", lazy='subquery', cascade='all, delete', backref="airplane_type")



class Airplane(db.Model):
    __tablename__ = 'airplane'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, ForeignKey(AirplaneType.id))
    flights = relationship("Flight", lazy='subquery', cascade='all, delete', backref='airplane')



class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True, default=generate_f_id)
    route_id = db.Column(db.Integer, ForeignKey('route.id'))
    airplane_id = db.Column(db.Integer, ForeignKey('airplane.id'))
    departure_time = db.Column(db.DateTime)
    reserved_seats = db.Column(db.Integer)
    seat_price = db.Column(FLOAT(precision=None, scale=1))






######################################## SCHEMAS ########################################

   
class AirportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        ordered = True
    iata_id = auto_field()
    city = auto_field()


class RouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Route
        ordered = True
    id = auto_field()
    origin_id = auto_field()
    destination_id = auto_field()


class AirplaneTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AirplaneType
        ordered = True
    id = auto_field()
    max_capacity = auto_field()


class AirplaneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airplane
        ordered = True

    id = auto_field()
    type_id = auto_field()
    airplane_type = fields.Nested(AirplaneTypeSchema(only=["max_capacity"],))


class FlightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        ordered = True
    id = auto_field()
    # route_id = auto_field()
    #airplane_id = auto_field()
    departure_time = auto_field()
    reserved_seats = auto_field()
    seat_price  = auto_field()
    airplane = fields.Nested(AirplaneSchema(only=['id', 'airplane_type']))
    route = fields.Nested(RouteSchema())



AIRPORT_SCHEMA = AirportSchema()
ROUTE_SCHEMA = RouteSchema()
AIRPLANE_TYPE_SCHEMA = AirplaneTypeSchema()
AIRPLANE_SCHEMA = AirplaneSchema()
FLIGHT_SCHEMA = FlightSchema()

AIRPORT_SCHEMA_MANY = AirportSchema(many=True)
ROUTE_SCHEMA_MANY = RouteSchema(many=True)
AIRPLANE_TYPE_SCHEMA_MANY = AirplaneTypeSchema(many=True)
AIRPLANE_SCHEMA_MANY = AirplaneSchema(many=True)
FLIGHT_SCHEMA_MANY = FlightSchema(many=True)




