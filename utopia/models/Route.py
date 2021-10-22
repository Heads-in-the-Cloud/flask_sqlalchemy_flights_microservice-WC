# from utopia import db
# from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, ForeignKeyConstraint
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Route(Base):
#     __tablename__ = 'route'


#     id = Column(Integer, primary_key=True)
#     destination_id = Column(String(3), ForeignKey('Airport.iata_id'))
#     origin_id =  Column(String(3), ForeignKey('Airport.iata_id'))
