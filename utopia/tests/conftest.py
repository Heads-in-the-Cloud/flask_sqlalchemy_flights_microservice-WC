from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pytest


from utopia.service.Airline import Airline
from utopia.models.Airport import Airport, Route




@pytest.fixture
def flask_app_mock():
    app_mock= Flask(__name__)
    db = SQLAlchemy(app_mock)
    db.init_app(app_mock)
    return app_mock

@pytest.fixture
def mock_airport_object():
    airport = Airport(iata_id='LAX', city = 'Los Angeles')
    return airport

@pytest.fixture
def mock_read_airport(mocker):
    mock = mocker.patch('flask_sqlalchemy.QueryProperty.__get__').return_value = mocker.Mock()
    return mock