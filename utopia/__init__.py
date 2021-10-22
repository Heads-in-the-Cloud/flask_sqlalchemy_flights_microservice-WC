from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/utopia'

# db = SQLAlchemy(app)
engine = create_engine('mysql://root:root@localhost/utopia', echo=True)
Session = sessionmaker(bind=engine)

from utopia import routes

