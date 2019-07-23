from datetime import datetime

from sqlalchemy import case, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from search.utils import dump_datetime
from .app import db


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    __table_args__ = {'info': dict(is_view=True)}

    id = db.Column(db.String(17), primary_key=True)
    reg_no = db.Column(db.String(6))
    customer_id = db.Column(db.Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="vehicles")
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

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'registration number': self.reg_no,
            'heartbeat_ts': dump_datetime(self.heartbeat_ts),
            'customer': self.customer.serialize
        }


class Customer(db.Model):
    __tablename__ = 'customer'
    __table_args__ = {'info': dict(is_view=True)}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    vehicles = relationship("Vehicle", back_populates="customer")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }
