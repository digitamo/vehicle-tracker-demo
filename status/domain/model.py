from eventsourcing.domain.model.decorators import attribute
from eventsourcing.domain.model.entity import TimestampedVersionedEntity, EntityWithHashchain


# NOTE: Consider adding more Events.
class Ping(EntityWithHashchain, TimestampedVersionedEntity):
    class Event(EntityWithHashchain.Event, TimestampedVersionedEntity.Event):
        """Supertype for events of example entities."""

    class Created(Event, EntityWithHashchain.Created, TimestampedVersionedEntity.Created):
        """Published when an Ping is created."""

    def __init__(self, vehicle_id='', **kwargs):
        super(Ping, self).__init__(**kwargs)
        self._vehicle_id = vehicle_id

    @attribute
    def vehicle_id(self):
        pass


def create_new_hit(vehicle_id=''):
    """
    Factory method for hit entities.

    :rtype: Ping
    """
    return Ping.__create__(vehicle_id=vehicle_id)
