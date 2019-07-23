from eventsourcing.domain.model.decorators import attribute
from eventsourcing.domain.model.entity import TimestampedVersionedEntity, EntityWithHashchain


# NOTE: Consider adding more Events.
class Heartbeat(EntityWithHashchain, TimestampedVersionedEntity):
    class Event(EntityWithHashchain.Event, TimestampedVersionedEntity.Event):
        """Supertype for events of example entities."""

    class Created(Event, EntityWithHashchain.Created, TimestampedVersionedEntity.Created):
        """Published when an Heartbeat is created."""

    def __init__(self, vehicle_id='', **kwargs):
        super(Heartbeat, self).__init__(**kwargs)
        self._vehicle_id = vehicle_id

    @attribute
    def vehicle_id(self):
        pass


def create_new_hit(vehicle_id=''):
    """
    Factory method for hit entities.

    :rtype: Heartbeat
    """
    return Heartbeat.__create__(vehicle_id=vehicle_id)
