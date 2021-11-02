from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy


from utopia.models.flights import Airplane, AirplaneType, AIRPLANE_SCHEMA, AIRPLANE_TYPE_SCHEMA, AIRPLANE_SCHEMA_MANY, AIRPLANE_TYPE_SCHEMA_MANY
from utopia.models.base import Session

import logging, json, traceback

logging.basicConfig(level=logging.INFO)


class AirplaneService:


############ GET ############

    def find_airplane(self, id):
        
        logging.info("finding airplane with id %s" %id)

        session = Session()

        airplane = session.query(Airplane).filter_by(id=id).first()

        airplane = AIRPLANE_SCHEMA.dump(airplane)

        return airplane

    def read_airplanes(self):

        logging.info("reading all airplanes")

        session = Session()
        
        airplanes = session.query(Airplane).all()

        airplanes = jsonify({'airplanes' : AIRPLANE_SCHEMA_MANY.dump(airplanes)})
        session.close()

        return airplanes

    def read_airplane_types(self):

        logging.info('reading airplane types')

        session = Session()

        airplane_types = session.query(AirplaneType).all()

        airplane_types = jsonify({'airplane_types' : AIRPLANE_TYPE_SCHEMA_MANY.dump(airplane_types) })
        
        session.close()

        return airplane_types


    def find_airplane_type(self, id):
        
        logging.info('finding airplane with id %s' %id)

        session = Session()

        airplane_type = session.query(AirplaneType).filter_by(id=id).first()

        airplane_type = AIRPLANE_TYPE_SCHEMA.dump(airplane_type)
        
        return airplane_type

    def read_airplane_by_type(self, type_id):
        
        logging.info('reading airplanes of type %s ' %id)

        session = Session()

        airplanes = session.query(Airplane).filter_by(type_id=type_id)

        airplanes = AIRPLANE_SCHEMA_MANY.dump(airplanes)
        session.close()

        return jsonify({'airplanes' : airplanes})


############ POST ############


    def add_airplane(self, airplane):

        logging.info('adding airplane')

        session = Session()
        airplane = Airplane(id = None, type_id=airplane['type_id'])
        session.add(airplane)

        session.commit()

        airplane = AIRPLANE_SCHEMA.dump(airplane)
        session.close()
        
        return airplane


    def add_airplane_type(self, airplane_type):

        logging.info('adding airplane type')

        session = Session()
        airplane_type = AirplaneType(id = airplane_type['id'] if 'id' in airplane_type else None,
        
        max_capacity=airplane_type['max_capacity'])
        session.add(airplane_type)

        session.commit()

        airplane_type = AIRPLANE_TYPE_SCHEMA.dump(airplane_type)
        session.close()
        
        return airplane_type


############ PUT ############


    def update_airplane(self, airplane):

        logging.info('updating airplane')

        session = Session()
        
        airplane_to_update = session.query(Airplane).filter_by(id=airplane['id']).first()

        airplane_to_update.type_id = airplane['type_id']

        session.commit()

        airplane_to_update = AIRPLANE_SCHEMA.dump(airplane_to_update)
        session.close()

        return airplane_to_update

    
    def update_airplane_type(self, airplane_type):
            
            logging.info('updating airplane type')

            session = Session()

            airplane_type_to_update = session.query(AirplaneType).filter_by(id = airplane_type['id']).first()


            airplane_type_to_update.max_capacity = airplane_type['max_capacity']

            session.commit()

            airplane_type_to_update = AIRPLANE_TYPE_SCHEMA.dump(airplane_type_to_update)

            session.close()

            return airplane_type_to_update


############ DELETE ############

    def delete_airplane(self, id):

        logging.info('delete airplane')

        session = Session()

        session.query(Airplane).filter_by(id=id).delete()
        session.commit()
        session.close()

        return ''

    def delete_airplane_type(self, id):

        logging.info('delete airplane type')

        session = Session()

        airplane = session.query(AirplaneType).filter_by(id=id).first()
        session.delete(airplane)


        session.commit()
        session.close()
        
        return ''


 

   