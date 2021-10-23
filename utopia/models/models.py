from flask import Flask, app
from marshmallow.decorators import pre_dump
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.selectable import subquery
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
from sqlalchemy import Sequence

import json
import uuid

from sqlalchemy.sql.sqltypes import DateTime



Base = declarative_base()
ma = Marshmallow(app)


######################################## TABLES ########################################

class Airport(Base):
    __tablename__ = 'airport'


    iata_id = Column(String(3), primary_key=True)
    city =  Column(String(45))
    outgoing = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.origin_id")
    incoming = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.destination_id")


class Route(Base):
    __tablename__ = 'route'


    id = Column(Integer, primary_key=True)
    destination_id = Column(String(3) , ForeignKey("airport.iata_id"))
    origin_id =  Column(String(3) , ForeignKey("airport.iata_id"))
    flights = relationship('Flight', backref='route', lazy='subquery', cascade='all, delete')


class AirplaneType(Base):
    __tablename__ = 'airplane_type'

    id = Column(Integer, primary_key=True)
    max_capacity = Column(Integer)
    airplanes = relationship("Airplane", lazy='subquery', cascade='all, delete', backref="airplane_type")



class Airplane(Base):
    __tablename__ = 'airplane'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey(AirplaneType.id))
    flights = relationship("Flight", lazy='subquery', cascade='all, delete', backref='airplane')



class Flight(Base):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    airplane_id = Column(Integer, ForeignKey('airplane.id'))
    departure_time = Column(DateTime)
    reserved_seats = Column(Integer)
    seat_price = Column(Integer)


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
    airplane = fields.Nested(AirplaneSchema(only=['airplane_type']))
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




