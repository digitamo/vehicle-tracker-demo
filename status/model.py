from datetime import datetime

from sqlalchemy import case
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import UUIDType

from status.app import db


class Vehicle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    heartbeat_ts = db.Column(db.DateTime())

    @hybrid_property
    def online(self):
        current_timestamp = datetime.now().timestamp()
        return current_timestamp - self.heartbeat_ts.timestamp() < 59

    @online.expression
    def dominance(self):
        current_timestamp = datetime.now().timestamp()
        return case(
            [(current_timestamp - self.heartbeat_ts.timestamp() < 59, True), ],
            else_=False
        )


class EventSource(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sequence_id = db.Column(UUIDType(), nullable=False)
    position = db.Column(db.BigInteger(), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Text(), nullable=False)
    __table_args__ = db.Index('index', 'sequence_id', 'position', unique=True),
