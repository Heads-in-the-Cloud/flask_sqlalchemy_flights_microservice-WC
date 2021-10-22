from flask import Flask, app
from marshmallow.decorators import pre_dump
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.selectable import subquery
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields, pre_load, pre_dump
import json

Base = declarative_base()
ma = Marshmallow(app)


class AirplaneType(Base):
    __tablename__ = 'airplane_type'

    def __init__(self, id, max_capacity):
        self.id = id
        self.max_capacity = max_capacity

    id = Column(Integer, primary_key=True)
    max_capacity = Column(Integer)
    airplanes = relationship("Airplane", back_populates="airplane_type", cascade = "all,delete-orphan")

    def __repr__(self) -> str:
        return f"Airplane Type('{self.id}', '{self.max_capacity}')"
    def __eq__(self, obj):
        return obj.id == self.id



class Airplane(Base):
    __tablename__ = 'airplane'

    def __init__(self, id, type_id):
        self.id = id
        self.type_id = type_id

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('airplane_type.id'))
    airplane_type = relationship("AirplaneType", back_populates="airplanes")

    def __repr__(self) -> str:
        return f"Airplane('{self.id}', '{self.type_id}')"
    def __eq__(self, obj):
        return obj.id == self.id





   
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



AIRPLANE_TYPE_SCHEMA = AirplaneTypeSchema()
AIRPLANE_SCHEMA = AirplaneSchema()

AIRPLANE_TYPE_SCHEMA_MANY = AirplaneTypeSchema(many=True)
AIRPLANE_SCHEMA_MANY = AirplaneSchema(many=True)
