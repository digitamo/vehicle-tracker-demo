import os
import random
import time
from unittest import TestCase

import requests

BASE_URL = os.environ.get('SWARM_IP', 'http://197.162.249.146')
VEHICLE_IDS = [
    'YS2R4X20005399401',
    'VLUR4X20009093588',
    'VLUR4X20009048066',
    'YS2R4X20005388011',
    'YS2R4X20005387949',
    'YS2R4X20005387765',
    'YS2R4X20005387055',
]


class HeartbeatTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.VEHICLE_ID = VEHICLE_IDS[random.randrange(7)]

    def test_01_heartbeat_should_change_offline_vehicle_to_online(self):
        url = BASE_URL + '/heartbeat/' + self.VEHICLE_ID

        response = requests.request("POST", url)
        self.assertEqual(response.status_code, 200)

    def test_02_vehicle_should_be_online_after_heartbeat(self):
        url = BASE_URL + '/search'
        querystring = {"online": "true"}
        response = requests.request("GET", url, params=querystring)
        self.assertEqual(response.status_code, 200)

        online_vehicles_ids = map(lambda x: x.get('id'), response.json())
        self.assertIn(self.VEHICLE_ID, online_vehicles_ids)

    def test_03_vehicle_should_be_offline_after_one_minute(self):
        time.sleep(60)
        url = BASE_URL + '/search'
        querystring = {"online": "true"}
        response = requests.request("GET", url, params=querystring)
        self.assertEqual(response.status_code, 200)

        online_vehicles_ids = map(lambda x: x.get('id'), response.json())
        self.assertNotIn(self.VEHICLE_ID, online_vehicles_ids)
