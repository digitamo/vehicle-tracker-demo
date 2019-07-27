from datetime import datetime

from flask import abort
from eventsourcing.domain.model.events import subscribe, unsubscribe
from eventsourcing.infrastructure.eventstore import AbstractEventStore
from heartbeat.model import Vehicle
from heartbeat.app import db


class ViewPersistencePolicy(object):
    def __init__(self, event_store, persist_event_type=None):
        assert isinstance(event_store, AbstractEventStore), type(event_store)
        self.event_store = event_store
        self.persist_event_type = persist_event_type
        subscribe(self.update_status, self.is_event)

    def close(self):
        unsubscribe(self.update_status, self.is_event)

    def is_event(self, event):
        if self.persist_event_type is None:
            return False
        if isinstance(event, (list, tuple)):
            return all(map(self.is_event, event))
        return isinstance(event, self.persist_event_type)

    @staticmethod
    def update_status(event):
        vehicle_id = event.vehicle_id
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            vehicle.heartbeat_ts = datetime.fromtimestamp(event.timestamp)
            db.session.commit()
        else:
            abort(404)
