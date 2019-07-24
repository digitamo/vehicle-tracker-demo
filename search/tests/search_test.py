from datetime import datetime

from flask_testing import TestCase

from search.app import application, db
from search.model import Customer, Vehicle


class Search(TestCase):

    def create_app(self):
        # NOTE: By default flask will use in memory sqlite but it's better to use an application factory and generate an
        # application for testing purposes with test config.
        return application

    # TODO: populate tables with mock data.
    def setUp(self):
        db.create_all()

        customers = [
            Customer(id=1, name='Kalles Grustransporter AB', address='Cementvägen 8, 111 11 Södertälje'),
            Customer(id=2, name='Johans Bulk AB', address='Balkvägen 12, 222 22 Stockholm'),
            Customer(id=3, name='Haralds Värdetransporter AB', address='Budgetvägen 1, 333 33 Uppsala')
        ]
        vehicles = [
            Vehicle(id="YS2R4X20005399401", reg_no='ABC123', customer=customers[0], heartbeat_ts=datetime.now()),
            Vehicle(id='VLUR4X20009093588', reg_no='DEF456', customer=customers[0],
                    heartbeat_ts=datetime.fromisoformat('2019-07-24T04:51:06.562952')),
            Vehicle(id='VLUR4X20009048066', reg_no='GHI789', customer=customers[0],
                    heartbeat_ts=datetime.fromisoformat('2015-07-24T04:51:06.562952')),
            Vehicle(id='YS2R4X20005388011', reg_no='JKL012', customer=customers[1], heartbeat_ts=datetime.now()),
            Vehicle(id='YS2R4X20005387949', reg_no='MNO345', customer=customers[1],
                    heartbeat_ts=datetime.fromisoformat('2019-07-03T04:51:06.562952')),
            Vehicle(id='YS2R4X20005387765', reg_no='PQR678', customer=customers[2],
                    heartbeat_ts=datetime.fromisoformat('2019-02-24T04:00:06.562952')),
            Vehicle(id='YS2R4X20005387055', reg_no='STU901', customer=customers[2],
                    heartbeat_ts=datetime.fromisoformat('2018-03-24T09:51:06.562952')),
        ]

        db.session.add_all(customers)
        db.session.commit()
        db.session.add_all(vehicles)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_search_with_customer_name(self):
        response = self.client.get('/search?customer_name=kalles')
        self.assertEqual(len(response.json), 3)

        response = self.client.get('/search?customer_name=Bulk')
        self.assertEqual(len(response.json), 2)

        response = self.client.get('/search?customer_name=Värdetransporter')
        self.assertEqual(len(response.json), 2)

    def test_search_with_online_status(self):
        response = self.client.get('/search?online=true')
        self.assertEqual(len(response.json), 2)

        response = self.client.get('/search?online=false')
        self.assertEqual(len(response.json), 5)

    def test_search_with_online_status_and_customer_name(self):
        response = self.client.get('/search?online=true&customer_name=Bulk')
        self.assertEqual(len(response.json), 1)

        response = self.client.get('/search?online=false&customer_name=Värdetransporter')
        self.assertEqual(len(response.json), 2)
