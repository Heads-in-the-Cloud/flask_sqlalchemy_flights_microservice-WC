from utopia.service.Airline import Airline
from utopia.tests.conftest import mock_airport_object

def test_read_airport(
    flask_app_mock,
    mock_get_sqlalchemy,
    mock_airport_object
):
    with flask_app_mock.app_context():
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_airport_object
        respone = Airline.readAirport






# class TestAirline(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         print('set up class')
#         airport = Airport(iata_id= 'YYY', city='City')
#         pass

#     @classmethod
#     def tearDownClass(cls):
#         print('tear down class')
#         pass

#     def test_add_airport(self):
#         print('test airport')
#         self.assertEqual(0, 0)



# if __name__ == '__main__':
#     unittest.main()