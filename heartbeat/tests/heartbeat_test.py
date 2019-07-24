import json
from datetime import datetime

from flask_testing import TestCase

from heartbeat.app import application, db
from heartbeat.domain.model import Heartbeat
from heartbeat.model import Customer, Vehicle, EventRecord
from heartbeat.domain.application import get_application


class HeartBeat(TestCase):

    def create_app(self):
        # NOTE: By default flask will use in memory sqlite but it's better to use an application factory and generate an
        # application for testing purposes with test config.
        return application

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
            Vehicle(id='YS2R4X20005387949', reg_no='MNO345', customer=customers[1]),
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

    def test_heartbeat_should_return_entity_id(self):
        response = self.client.post('/heartbeat/VLUR4X20009048066')
        entity_id = response.json.get('entity_id')
        self.assertIsNotNone(entity_id)

    def test_heartbeat_should_init_application(self):
        self.client.post('/heartbeat/VLUR4X20009048066')
        eventsourcing_app = get_application()
        self.assertIsNotNone(eventsourcing_app)

    def test_heartbeat_should_store_entity_in_application_repository(self):
        response = self.client.post('/heartbeat/VLUR4X20009048066')
        entity_id = response.json.get('entity_id')
        eventsourcing_application = get_application()
        application_repository = eventsourcing_application.application_repository
        entity = application_repository[entity_id]

        self.assertIsNotNone(entity, msg='Expected entity not to be `None`')
        self.assertIsInstance(entity, Heartbeat, msg='Expected entity not to be of type `HeartBeat`')
        self.assertEqual(entity.vehicle_id, 'VLUR4X20009048066')

    def test_heartbeat_should_store_event_in_event_source_table(self):
        self.client.post('/heartbeat/VLUR4X20009048066')
        event_source = db.session.query(EventRecord).first()
        self.assertIsNotNone(event_source)

    def test_heartbeat_should_store_vehicle_id_in_event_source_table(self):
        self.client.post('/heartbeat/VLUR4X20009048066')
        event_source = db.session.query(EventRecord).first()
        state = event_source.state
        state_data = json.loads(state)
        vehicle_id = state_data.get('vehicle_id')
        self.assertEqual(vehicle_id, 'VLUR4X20009048066')

    def test_heartbeat_should_update_vehicle_heartbeat_ts_in_view_table(self):
        self.client.post('/heartbeat/VLUR4X20009048066')
        vehicle = db.session.query(Vehicle).get('VLUR4X20009048066')
        old_heartbeat_ts = datetime.fromisoformat('2015-07-24T04:51:06.562952')

        self.assertNotEqual(vehicle.heartbeat_ts, old_heartbeat_ts)

    def test_heartbeat_should_write_vehicle_heartbeat_ts_in_view_table(self):
        self.client.post('/heartbeat/YS2R4X20005387949')
        vehicle = db.session.query(Vehicle).get('VLUR4X20009048066')

        self.assertIsNotNone(vehicle.heartbeat_ts)

    def test_heartbeat_with_non_existing_vehicle_should_return_404(self):
        response = self.client.post('/heartbeat/dummy_value')

        self.assertEqual(response.status_code, 404)

# TODO: Increase `domain.application` and `domina.policy` coverage.
