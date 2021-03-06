from abc import ABC

from eventsourcing.application.policies import PersistencePolicy
from eventsourcing.domain.model.entity import VersionedEntity
from eventsourcing.infrastructure.eventstore import EventStore
from eventsourcing.infrastructure.sequenceditemmapper import SequencedItemMapper
from eventsourcing.utils.transcoding import ObjectJSONDecoder, ObjectJSONEncoder

from heartbeat.domain.infrastructure import ApplicationRepository
from heartbeat.domain.model import create_new_hit, Heartbeat


# Application classes are based on event store examples found here:
# https://github.com/johnbywater/eventsourcing/blob/master/eventsourcing/example/application.py

class ApplicationWithEventStores(ABC):
    """
    Event sourced application object class.

    Can construct event stores using given database records.
    Supports three different event stores: for entity events.
    """

    def __init__(self, entity_record_manager=None,
                 cipher=None,
                 sequenced_item_mapper_class=SequencedItemMapper):
        self.entity_event_store = None
        if entity_record_manager:
            self.entity_event_store = self.construct_event_store(
                event_sequence_id_attr='originator_id',
                event_position_attr='originator_version',
                record_manager=entity_record_manager,
                cipher=cipher,
                sequenced_item_mapper_class=sequenced_item_mapper_class,
            )

    def construct_event_store(self, sequenced_item_mapper_class, event_sequence_id_attr, event_position_attr,
                              record_manager, cipher=None):
        sequenced_item_mapper = self.construct_sequenced_item_mapper(
            sequenced_item_mapper_class=sequenced_item_mapper_class,
            sequenced_item_class=record_manager.sequenced_item_class,
            event_sequence_id_attr=event_sequence_id_attr,
            event_position_attr=event_position_attr,
            cipher=cipher,
        )
        event_store = EventStore(
            record_manager=record_manager,
            sequenced_item_mapper=sequenced_item_mapper,
        )
        return event_store

    @staticmethod
    def construct_sequenced_item_mapper(sequenced_item_mapper_class,
                                        sequenced_item_class,
                                        event_sequence_id_attr,
                                        event_position_attr,
                                        cipher=None,
                                        json_encoder_class=ObjectJSONEncoder,
                                        json_decoder_class=ObjectJSONDecoder):
        return sequenced_item_mapper_class(
            sequenced_item_class=sequenced_item_class,
            sequence_id_attr_name=event_sequence_id_attr,
            position_attr_name=event_position_attr,
            json_encoder_class=json_encoder_class,
            json_decoder_class=json_decoder_class,
            cipher=cipher,
        )

    def close(self):
        self.entity_event_store = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class ApplicationWithPersistencePolicies(ApplicationWithEventStores):
    def __init__(self, **kwargs):
        super(ApplicationWithPersistencePolicies, self).__init__(**kwargs)
        self.entity_persistence_policy = self.construct_entity_persistence_policy()
        self.view_persistence_policy = self.construct_view_persistence_policy()

    def construct_entity_persistence_policy(self):
        if self.entity_event_store:
            return PersistencePolicy(
                event_store=self.entity_event_store,
                persist_event_type=VersionedEntity.Event,
            )

    def construct_view_persistence_policy(self):
        from heartbeat.domain.policy import ViewPersistencePolicy

        if self.entity_event_store:
            return ViewPersistencePolicy(
                event_store=self.entity_event_store,
                persist_event_type=Heartbeat.Created
            )

    def close(self):
        if self.entity_persistence_policy is not None:
            self.entity_persistence_policy.close()
            self.entity_persistence_policy = None
        if self.view_persistence_policy is not None:
            self.view_persistence_policy.close()
            self.view_persistence_policy = None
        super(ApplicationWithPersistencePolicies, self).close()


class Application(ApplicationWithPersistencePolicies):
    """
    Heartbeat event sourced application with entity factory and repository.
    """

    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        assert self.entity_event_store is not None
        self.application_repository = ApplicationRepository(event_store=self.entity_event_store)

    @staticmethod
    def create_ping(vehicle_id=''):
        """Entity object factory."""
        return create_new_hit(vehicle_id=vehicle_id)


def construct_application(**kwargs):
    """Application object factory."""
    return Application(**kwargs)


# "Global" variable for single instance of application.
_application = None


def init_application(**kwargs):
    """
    Constructs single global instance of application.

    To be called when initialising a worker process.
    """
    global _application
    if _application is not None:
        raise AssertionError("init_application() has already been called")
    _application = construct_application(**kwargs)


def get_application():
    """
    Returns single global instance of application.

    To be called when handling a worker request, if required.
    """
    if _application is None:
        raise AssertionError("init"
                             "_application() must be called first")
    assert isinstance(_application, Application)
    return _application


def close_application():
    """
    Shuts down single global instance of application.

    To be called when tearing down, perhaps between tests, in order to allow a
    subsequent call to init_application().
    """
    global _application
    if _application is not None:
        _application.close()
    _application = None
