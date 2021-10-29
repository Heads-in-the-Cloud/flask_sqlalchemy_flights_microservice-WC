from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config
from utopia import app

Base = declarative_base()

engine = create_engine(f"mysql://{app.config['DB_USER']}:{app.config['DB_USER_PASSWORD']}@{app.config['DB_HOST']}/{app.config['DB']}", echo=True)
Session = sessionmaker(bind=engine)