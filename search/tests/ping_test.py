import requests
from flask_testing import LiveServerTestCase

from search.app import application


class Ping(LiveServerTestCase):

    def create_app(self):
        application.config['TESTING'] = True
        application.config['LIVESERVER_PORT'] = 8943
        application.config['LIVESERVER_TIMEOUT'] = 10
        return application

    def test_ping_should_return_200_OK(self):
        url = self.get_server_url() + '/ping'
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

    def test_ping_should_return_pong_message(self):
        response = requests.get(self.get_server_url() + '/ping')

        self.assertEqual(response.json(), {'message': 'pong'})
