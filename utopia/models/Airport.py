from flask import Flask, app
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.selectable import subquery
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
import json



Base = declarative_base()
ma = Marshmallow(app)


class Airport(Base):
    __tablename__ = 'airport'


    iata_id = Column(String(3), primary_key=True)
    city =  Column(String(45))
    outgoing = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.origin_id")
    incoming = relationship("Route", lazy='subquery', primaryjoin="Airport.iata_id == Route.destination_id")
    def __repr__(self) -> str:
        return f"Airport(iata_id:'{self.iata_id}', 'city:{self.city}', 'outgoing:{self.outgoing}', 'incoming:{self.incoming}')"
    def __eq__(self, obj):
        return obj.iata_id == self.iata_id

class Route(Base):
    __tablename__ = 'route'


    id = Column(Integer, primary_key=True)
    destination_id = Column(String(3) , ForeignKey("airport.iata_id"))
    origin_id =  Column(String(3) , ForeignKey("airport.iata_id"))
    def __repr__(self) -> str:
        return f"Route(id:'{self.id}', origin_id:'{self.origin_id}', 'destination_id:{self.destination_id}')"
    def __eq__(self, obj):
        return obj.id == self.id or (obj.origin_id == self.origin_id and obj.destination_id
        == self.destination_id)




class RouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Route
        ordered = True
    id = auto_field()
    origin_id = auto_field()
    destination_id = auto_field()

class AirportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        ordered = True
    iata_id = auto_field()
    city = auto_field()
    # incoming = fields.List(fields.Nested(RouteSchema))
    # outgoing= fields.List(fields.Nested(RouteSchema))

AIRPORT_SCHEMA = AirportSchema()
ROUTE_SCHEMA = RouteSchema()


AIRPORT_SCHEMA_MANY = AirportSchema(many=True)
ROUTE_SCHEMA_MANY = RouteSchema(many=True)


# def new_alchemy_encoder():
#     _visited_objs = []

#     class AlchemyEncoder(json.JSONEncoder):
#         def default(self, obj):
#             if isinstance(obj.__class__, DeclarativeMeta):
#                 # don't re-visit self
#                 if obj in _visited_objs:
#                     return None
#                 _visited_objs.append(obj)

#                 # an SQLAlchemy class
#                 fields = {}
#                 for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                     fields[field] = obj.__getattribute__(field)
#                 # a json-encodable dict
#                 return fields

#             return json.JSONEncoder.default(self, obj)

#     return AlchemyEncoder











#   class AlchemyEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields

#         return json.JSONEncoder.default(self, obj)