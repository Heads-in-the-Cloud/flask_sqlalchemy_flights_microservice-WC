from flask import Flask
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

app.config['JSON_SORT_KEYS'] = False
app.config['DB_HOST'] = os.getenv('DB_HOST')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DB_USER'] = os.getenv('DB_USER')
app.config['DB_USER_PASSWORD'] = os.getenv('DB_USER_PASSWORD')
app.config['DB'] = os.getenv('DB')

from utopia import airport_controller , airplane_controller, flight_controller, error_handler