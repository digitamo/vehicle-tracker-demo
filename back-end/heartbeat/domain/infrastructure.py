from eventsourcing.example.domainmodel import AbstractExampleRepository
from eventsourcing.infrastructure.eventsourcedrepository import EventSourcedRepository


class ApplicationRepository(EventSourcedRepository, AbstractExampleRepository):
    """
    Event sourced repository for the Heartbeat domain model entity.
    """
    __page_size__ = 1000
