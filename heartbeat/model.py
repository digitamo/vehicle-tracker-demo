from datetime import datetime

from sqlalchemy import case, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from heartbeat.app import db


# NOTE: Consider Creating an internal data access micorservice.
class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.String(17), primary_key=True)
    reg_no = db.Column(db.String(6))
    customer_id = db.Column(db.Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="vehicles")
    heartbeat_ts = db.Column(db.DateTime())


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    vehicles = relationship("Vehicle", back_populates="customer")


class EventSource(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sequence_id = db.Column(UUIDType(), nullable=False)
    position = db.Column(db.BigInteger(), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Text(), nullable=False)
    __table_args__ = db.Index('index', 'sequence_id', 'position', unique=True),
