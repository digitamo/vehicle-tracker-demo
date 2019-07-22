from sqlalchemy import Integer, Column, BigInteger, String, Text
from sqlalchemy_utils import UUIDType

from .app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class IntegerSequencedItem(db.Model):
    __tablename__ = 'integer_sequenced_items'

    id = db.Column(Integer(), primary_key=True)
    sequence_id = Column(UUIDType(), nullable=False)
    position = Column(BigInteger(), nullable=False)
    topic = Column(String(255), nullable=False)
    state = Column(Text(), nullable=False)
    __table_args__ = db.Index('index', 'sequence_id', 'position', unique=True),
