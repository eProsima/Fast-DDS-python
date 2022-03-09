import fastdds
import test_complete


class DomainParticipantListener (fastdds.DomainParticipantListener):
    def __init__(self):
        super().__init__()


class PublisherListener (fastdds.PublisherListener):
    def __init__(self):
        super().__init__()


class SubscriberListener (fastdds.SubscriberListener):
    def __init__(self):
        super().__init__()


class TopicListener (fastdds.TopicListener):
    def __init__(self):
        super().__init__()


def test_contains_entity():
    """
    This test checks:
    - DomainParticipant::contains_entity
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    assert(participant.contains_entity(publisher.get_instance_handle()))

    assert(participant.contains_entity(fastdds.InstanceHandle_t()) is False)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_and_delete_publisher():
    """
    This test checks:
    - DomainParticipant::create_publisher
    - DomainParticipant::delete_publisher
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    listener = PublisherListener()
    assert(listener is not None)

    # Overload 1
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    assert(publisher.is_enabled())
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))

    # Overload 2
    publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT, listener)
    assert(publisher is not None)
    assert(publisher.is_enabled())
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT, listnr, status_mask_1)
        assert(publisher is not None)
        assert(publisher.is_enabled())
        assert(status_mask_1 == publisher.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.delete_publisher(publisher))
        publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT, listnr, status_mask_2)
        assert(publisher is not None)
        assert(publisher.is_enabled())
        assert(status_mask_2 == publisher.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.delete_publisher(publisher))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), None)
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), listener)
    test(fastdds.StatusMask.none(), fastdds.StatusMask_none(), listener)
    test(fastdds.StatusMask.data_available(),
         fastdds.StatusMask_data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(),
         fastdds.StatusMask_data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(),
         fastdds.StatusMask_inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(),
         fastdds.StatusMask_liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(),
         fastdds.StatusMask_liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(),
         fastdds.StatusMask_offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(),
         fastdds.StatusMask_offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(),
         fastdds.StatusMask_publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(),
         fastdds.StatusMask_requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(),
         fastdds.StatusMask_requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(),
         fastdds.StatusMask_sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(),
         fastdds.StatusMask_sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(),
         fastdds.StatusMask_subscription_matched(), listener)

    m = fastdds.StatusMask_data_available() << \
        fastdds.StatusMask_data_on_readers() << \
        fastdds.StatusMask_inconsistent_topic() << \
        fastdds.StatusMask_liveliness_changed() << \
        fastdds.StatusMask_liveliness_lost() << \
        fastdds.StatusMask_offered_deadline_missed() << \
        fastdds.StatusMask_offered_incompatible_qos() << \
        fastdds.StatusMask_publication_matched() << \
        fastdds.StatusMask_requested_deadline_missed() << \
        fastdds.StatusMask_requested_incompatible_qos() << \
        fastdds.StatusMask_sample_lost() << \
        fastdds.StatusMask_sample_rejected() << \
        fastdds.StatusMask_subscription_matched()

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched(),
         m,
         listener)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_and_delete_subscriber():
    """
    This test checks:
    - DomainParticipant::create_subscriber
    - DomainParticipant::delete_subscriber
    - Subscriber::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    listener = SubscriberListener()
    assert(listener is not None)

    # Overload 1
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    assert(subscriber.is_enabled())
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))

    # Overload 2
    subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT, listener)
    assert(subscriber is not None)
    assert(subscriber.is_enabled())
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT, listnr, status_mask_1)
        assert(subscriber is not None)
        assert(subscriber.is_enabled())
        assert(status_mask_1 == subscriber.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.delete_subscriber(subscriber))
        subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT, listnr, status_mask_2)
        assert(subscriber is not None)
        assert(subscriber.is_enabled())
        assert(status_mask_2 == subscriber.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.delete_subscriber(subscriber))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), None)
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), listener)
    test(fastdds.StatusMask.none(), fastdds.StatusMask_none(), listener)
    test(fastdds.StatusMask.data_available(),
         fastdds.StatusMask_data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(),
         fastdds.StatusMask_data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(),
         fastdds.StatusMask_inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(),
         fastdds.StatusMask_liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(),
         fastdds.StatusMask_liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(),
         fastdds.StatusMask_offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(),
         fastdds.StatusMask_offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(),
         fastdds.StatusMask_publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(),
         fastdds.StatusMask_requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(),
         fastdds.StatusMask_requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(),
         fastdds.StatusMask_sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(),
         fastdds.StatusMask_sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(),
         fastdds.StatusMask_subscription_matched(), listener)

    m = fastdds.StatusMask_data_available() << \
        fastdds.StatusMask_data_on_readers() << \
        fastdds.StatusMask_inconsistent_topic() << \
        fastdds.StatusMask_liveliness_changed() << \
        fastdds.StatusMask_liveliness_lost() << \
        fastdds.StatusMask_offered_deadline_missed() << \
        fastdds.StatusMask_offered_incompatible_qos() << \
        fastdds.StatusMask_publication_matched() << \
        fastdds.StatusMask_requested_deadline_missed() << \
        fastdds.StatusMask_requested_incompatible_qos() << \
        fastdds.StatusMask_sample_lost() << \
        fastdds.StatusMask_sample_rejected() << \
        fastdds.StatusMask_subscription_matched()

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched(),
         m,
         listener)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_and_delete_topic():
    """
    This test checks:
    - DomainParticipant::create_topic
    - DomainParticipant::delete_topic
    - Topic::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    listener = TopicListener()
    assert(listener is not None)

    # Overload 1 - Failing (because the type is not registered yet)
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is None)

    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))

    # Overload 1 - Success
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    assert(topic.is_enabled())
    assert(fastdds.StatusMask.all() == topic.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))

    # Overload 2
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT,
            listener)
    assert(topic is not None)
    assert(topic.is_enabled())
    assert(fastdds.StatusMask.all() == topic.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        topic = participant.create_topic(
            "Complete", "CompleteTestType",
            fastdds.TOPIC_QOS_DEFAULT, listnr, status_mask_1)
        assert(topic is not None)
        assert(topic.is_enabled())
        assert(status_mask_1 == topic.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.delete_topic(topic))
        topic = participant.create_topic(
            "Complete", "CompleteTestType",
            fastdds.TOPIC_QOS_DEFAULT, listnr, status_mask_2)
        assert(topic is not None)
        assert(topic.is_enabled())
        assert(status_mask_2 == topic.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.delete_topic(topic))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), None)
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), listener)
    test(fastdds.StatusMask.none(), fastdds.StatusMask_none(), listener)
    test(fastdds.StatusMask.data_available(),
         fastdds.StatusMask_data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(),
         fastdds.StatusMask_data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(),
         fastdds.StatusMask_inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(),
         fastdds.StatusMask_liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(),
         fastdds.StatusMask_liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(),
         fastdds.StatusMask_offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(),
         fastdds.StatusMask_offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(),
         fastdds.StatusMask_publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(),
         fastdds.StatusMask_requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(),
         fastdds.StatusMask_requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(),
         fastdds.StatusMask_sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(),
         fastdds.StatusMask_sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(),
         fastdds.StatusMask_subscription_matched(), listener)

    m = fastdds.StatusMask_data_available() << \
        fastdds.StatusMask_data_on_readers() << \
        fastdds.StatusMask_inconsistent_topic() << \
        fastdds.StatusMask_liveliness_changed() << \
        fastdds.StatusMask_liveliness_lost() << \
        fastdds.StatusMask_offered_deadline_missed() << \
        fastdds.StatusMask_offered_incompatible_qos() << \
        fastdds.StatusMask_publication_matched() << \
        fastdds.StatusMask_requested_deadline_missed() << \
        fastdds.StatusMask_requested_incompatible_qos() << \
        fastdds.StatusMask_sample_lost() << \
        fastdds.StatusMask_sample_rejected() << \
        fastdds.StatusMask_subscription_matched()

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched(),
         m,
         listener)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_delete_contained_entities():
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)

    # Cannot delete participant without deleting its contained entities
    assert(fastdds.ReturnCode_t.RETCODE_PRECONDITION_NOT_MET ==
           factory.delete_participant(participant))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_contained_entities())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_enable():
    """
    This test checks:
    - DomainParticipant::enable
    - DomainParticipant::is_enabled
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    factory_qos = fastdds.DomainParticipantFactoryQos()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.get_qos(factory_qos))
    factory_qos.entity_factory().autoenable_created_entities = False
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.set_qos(factory_qos))
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    assert(not participant.is_enabled())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.enable())
    assert(participant.is_enabled())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
    factory_qos.entity_factory().autoenable_created_entities = True
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.set_qos(factory_qos))


def test_find_topic():
    """
    This test checks:
    - DomainParticipant::find_topic
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))

    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)

    topic_copy = participant.find_topic("Complete", fastdds.Duration_t(1, 0))
    assert(topic_copy is None)  # Not implemented yet
    # assert(topic.get_type_name() == topic_copy.get_type_name())
    # assert(topic.get_name() == topic_copy.get_name())
    # assert(fastdds.ReturnCode_t.RETCODE_OK ==
    #        participant.delete_topic(topic_copy))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_builtin_subscriber():
    """
    This test checks:
    - DomainParticipant::get_builtin_subscriber
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    builtin_subscriber = participant.get_builtin_subscriber()
    assert(builtin_subscriber is None)
    # assert(builtin_subscriber.is_enabled())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_discovered_participants():
    """
    This test checks:
    - DomainParticipant::get_discovered_participants
    - DomainParticipant::get_discovered_participant_data
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    participant2 = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant2 is not None)

    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           participant.get_discovered_participants(ihs))


def test_get_domain_id():
    """
    This test checks:
    - DomainParticipant::get_domain_id
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            32, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    assert(32 == participant.get_domain_id())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_instance_handle():
    """
    This test checks:
    - DomainParticipant::get_instance_handle
    - DomainParticipant::guid
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    ih = participant.get_instance_handle()
    assert(ih is not None)
    # assert(ih.isDefined())
    guid = participant.guid()
    assert(guid is not None)

    assert(ih != fastdds.c_InstanceHandle_Unknown)
    assert(guid != fastdds.c_Guid_Unknown)

    assert(guid.get_instance_handle() == ih)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])

    for i in range(0, 4):
        assert(guid.entityId.value[i] == ih.value[12+i])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_listener():
    """
    This test checks:
    - DomainParticipant::get_listener
    - DomainParticipant::set_listener
    - DomainParticipant::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            7, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    # Overload 1
    listener = DomainParticipantListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.set_listener(listener))
    assert(participant.get_listener() == listener)
    assert(fastdds.StatusMask.all() == participant.get_status_mask())

    def test(status_mask_1, status_mask_2):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        listener = DomainParticipantListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.set_listener(listener, status_mask_1))
        assert(participant.get_listener() == listener)
        assert(status_mask_1 == participant.get_status_mask())
        listener = DomainParticipantListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               participant.set_listener(listener, status_mask_2))
        assert(participant.get_listener() == listener)
        assert(status_mask_2 == participant.get_status_mask())

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all())
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all())
    test(fastdds.StatusMask.none(), fastdds.StatusMask_none())
    test(fastdds.StatusMask.data_available(),
         fastdds.StatusMask_data_available())
    test(fastdds.StatusMask.data_on_readers(),
         fastdds.StatusMask_data_on_readers())
    test(fastdds.StatusMask.inconsistent_topic(),
         fastdds.StatusMask_inconsistent_topic())
    test(fastdds.StatusMask.liveliness_changed(),
         fastdds.StatusMask_liveliness_changed())
    test(fastdds.StatusMask.liveliness_lost(),
         fastdds.StatusMask_liveliness_lost())
    test(fastdds.StatusMask.offered_deadline_missed(),
         fastdds.StatusMask_offered_deadline_missed())
    test(fastdds.StatusMask.offered_incompatible_qos(),
         fastdds.StatusMask_offered_incompatible_qos())
    test(fastdds.StatusMask.publication_matched(),
         fastdds.StatusMask_publication_matched())
    test(fastdds.StatusMask.requested_deadline_missed(),
         fastdds.StatusMask_requested_deadline_missed())
    test(fastdds.StatusMask.requested_incompatible_qos(),
         fastdds.StatusMask_requested_incompatible_qos())
    test(fastdds.StatusMask.sample_lost(),
         fastdds.StatusMask_sample_lost())
    test(fastdds.StatusMask.sample_rejected(),
         fastdds.StatusMask_sample_rejected())
    test(fastdds.StatusMask.subscription_matched(),
         fastdds.StatusMask_subscription_matched())

    m = fastdds.StatusMask_data_available() << \
        fastdds.StatusMask_data_on_readers() << \
        fastdds.StatusMask_inconsistent_topic() << \
        fastdds.StatusMask_liveliness_changed() << \
        fastdds.StatusMask_liveliness_lost() << \
        fastdds.StatusMask_offered_deadline_missed() << \
        fastdds.StatusMask_offered_incompatible_qos() << \
        fastdds.StatusMask_publication_matched() << \
        fastdds.StatusMask_requested_deadline_missed() << \
        fastdds.StatusMask_requested_incompatible_qos() << \
        fastdds.StatusMask_sample_lost() << \
        fastdds.StatusMask_sample_rejected() << \
        fastdds.StatusMask_subscription_matched()

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched(),
         m)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_partitipant_names():
    """
    This test checks:
    - DomainParticipant::get_participant_names
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    qos = fastdds.DomainParticipantQos()
    qos.name('TestName')
    participant = factory.create_participant(0, qos)
    assert(participant is not None)

    names = participant.get_participant_names()
    assert('TestName' == names[0])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_qos():
    """
    This test checks:
    - DomainParticipant::get_qos
    - DomainParticipant::set_qos
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    qos = fastdds.DomainParticipantQos()
    participant = factory.create_participant(0, qos)
    assert(participant is not None)

    qos.user_data().push_back(1)
    qos.user_data().push_back(2)
    assert(2 == len(qos.user_data()))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.set_qos(qos))

    qos2 = fastdds.DomainParticipantQos()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.get_qos(qos2))
    assert(2 == len(qos2.user_data()))
    assert(1 == qos2.user_data()[0])
    assert(2 == qos2.user_data()[1])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_ignore_participant():
    """
    This test checks:
    - DomainParticipant::ignore_participant
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           participant.ignore_participant(ih))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_ignore_publication():
    """
    This test checks:
    - DomainParticipant::ignore_publication
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           participant.ignore_publication(ih))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_ignore_subscription():
    """
    This test checks:
    - DomainParticipant::ignore_subscription
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           participant.ignore_subscription(ih))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_ignore_topic():
    """
    This test checks:
    - DomainParticipant::ignore_topic
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           participant.ignore_topic(ih))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_lookup_topicdescription():
    """
    This test checks:
    - DomainParticipant::lookup_topicdescription
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)

    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))

    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)

    topic_desc = participant.lookup_topicdescription("Complete")
    assert(topic_desc is not None)
    assert(topic.get_type_name() == topic_desc.get_type_name())
    assert(topic.get_name() == topic_desc.get_name())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))



#
#
#    /**
#     * Create a Publisher in this Participant.
#     *
#     * @param profile_name Publisher profile name.
#     * @param listener Pointer to the listener (default: nullptr)
#     * @param mask StatusMask that holds statuses the listener responds to (default: all)
#     * @return Pointer to the created Publisher.
#     */
#    RTPS_DllAPI Publisher* create_publisher_with_profile(
#            const std::string& profile_name,
#            PublisherListener* listener = nullptr,
#            const StatusMask& mask = StatusMask::all());
#
#    /**
#     * Create a Subscriber in this Participant.
#     *
#     * @param profile_name Subscriber profile name.
#     * @param listener Pointer to the listener (default: nullptr)
#     * @param mask StatusMask that holds statuses the listener responds to (default: all)
#     * @return Pointer to the created Subscriber.
#     */
#    RTPS_DllAPI Subscriber* create_subscriber_with_profile(
#            const std::string& profile_name,
#            SubscriberListener* listener = nullptr,
#            const StatusMask& mask = StatusMask::all());
#
#
#     * Create a Topic in this Participant.
#     *
#     * @param topic_name Name of the Topic.
#     * @param type_name Data type of the Topic.
#     * @param profile_name Topic profile name.
#     * @param listener Pointer to the listener (default: nullptr)
#     * @param mask StatusMask that holds statuses the listener responds to (default: all)
#     * @return Pointer to the created Topic.
#     */
#    RTPS_DllAPI Topic* create_topic_with_profile(
#            const std::string& topic_name,
#            const std::string& type_name,
#            const std::string& profile_name,
#            TopicListener* listener = nullptr,
#            const StatusMask& mask = StatusMask::all());
#
#    /**
#     * Create a ContentFilteredTopic in this Participant.
#     *
#     * @param name Name of the ContentFilteredTopic
#     * @param related_topic Related Topic to being subscribed
#     * @param filter_expression Logic expression to create filter
#     * @param expression_parameters Parameters to filter content
#     * @return Pointer to the created ContentFilteredTopic.
#     * @return nullptr if @c related_topic does not belong to this participant.
#     * @return nullptr if a topic with the specified @c name has already been created.
#     * @return nullptr if a filter cannot be created with the specified @c filter_expression and
#     *                 @c expression_parameters.
#     */
#    RTPS_DllAPI ContentFilteredTopic* create_contentfilteredtopic(
#            const std::string& name,
#            Topic* related_topic,
#            const std::string& filter_expression,
#            const std::vector<std::string>& expression_parameters);
#
#    /**
#     * Create a ContentFilteredTopic in this Participant using a custom filter.
#     *
#     * @param name Name of the ContentFilteredTopic
#     * @param related_topic Related Topic to being subscribed
#     * @param filter_expression Logic expression to create filter
#     * @param expression_parameters Parameters to filter content
#     * @param filter_class_name Name of the filter class to use
#     *
#     * @return Pointer to the created ContentFilteredTopic.
#     * @return nullptr if @c related_topic does not belong to this participant.
#     * @return nullptr if a topic with the specified @c name has already been created.
#     * @return nullptr if a filter cannot be created with the specified @c filter_expression and
#     *                 @c expression_parameters.
#     * @return nullptr if the specified @c filter_class_name has not been registered.
#     */
#    RTPS_DllAPI ContentFilteredTopic* create_contentfilteredtopic(
#            const std::string& name,
#            Topic* related_topic,
#            const std::string& filter_expression,
#            const std::vector<std::string>& expression_parameters,
#            const char* filter_class_name);
#
#    /**
#     * Deletes an existing ContentFilteredTopic.
#     *
#     * @param a_contentfilteredtopic ContentFilteredTopic to be deleted
#     * @return RETCODE_BAD_PARAMETER if the topic passed is a nullptr, RETCODE_PRECONDITION_NOT_MET if the topic does not belong to
#     * this participant or if it is referenced by any entity and RETCODE_OK if the ContentFilteredTopic was deleted.
#     */
#    RTPS_DllAPI ReturnCode_t delete_contentfilteredtopic(
#            const ContentFilteredTopic* a_contentfilteredtopic);
#
#    /**
#     * Create a MultiTopic in this Participant.
#     *
#     * @param name Name of the MultiTopic
#     * @param type_name Result type of the MultiTopic
#     * @param subscription_expression Logic expression to combine filter
#     * @param expression_parameters Parameters to subscription content
#     * @return Pointer to the created ContentFilteredTopic, nullptr in error case
#     */
#    RTPS_DllAPI MultiTopic* create_multitopic(
#            const std::string& name,
#            const std::string& type_name,
#            const std::string& subscription_expression,
#            const std::vector<std::string>& expression_parameters);
#
#    /**
#     * Deletes an existing MultiTopic.
#     *
#     * @param a_multitopic MultiTopic to be deleted
#     * @return RETCODE_BAD_PARAMETER if the topic passed is a nullptr, RETCODE_PRECONDITION_NOT_MET if the topic does not belong to
#     * this participant or if it is referenced by any entity and RETCODE_OK if the Topic was deleted.
#     */
#    RTPS_DllAPI ReturnCode_t delete_multitopic(
#            const MultiTopic* a_multitopic);
#
#    /**
#     * This operation manually asserts the liveliness of the DomainParticipant.
#     * This is used in combination with the LIVELINESS QoS policy to indicate to the Service that the entity
#     * remains active.
#     *
#     * This operation needs to only be used if the DomainParticipant contains DataWriter entities with
#     * the LIVELINESS set to MANUAL_BY_PARTICIPANT and it only affects the liveliness of those DataWriter entities.
#     * Otherwise, it has no effect.
#     *
#     * @note Writing data via the write operation on a DataWriter asserts liveliness on the DataWriter itself and its
#     * DomainParticipant. Consequently the use of assert_liveliness is only needed if the application is not
#     * writing data regularly.
#     *
#     * @return RETCODE_OK if the liveliness was asserted, RETCODE_ERROR otherwise.
#     */
#    RTPS_DllAPI ReturnCode_t assert_liveliness();
#
#    /**
#     * Fills the PublisherQos with the values of the XML profile.
#     *
#     * @param profile_name Publisher profile name.
#     * @param qos PublisherQos object where the qos is returned.
#     * @return RETCODE_OK if the profile exists. RETCODE_BAD_PARAMETER otherwise.
#     */
#    RTPS_DllAPI ReturnCode_t get_publisher_qos_from_profile(
#            const std::string& profile_name,
#            PublisherQos& qos) const;
#
#
#    /**
#     * Fills the SubscriberQos with the values of the XML profile.
#     *
#     * @param profile_name Subscriber profile name.
#     * @param qos SubscriberQos object where the qos is returned.
#     * @return RETCODE_OK if the profile exists. RETCODE_BAD_PARAMETER otherwise.
#     */
#    RTPS_DllAPI ReturnCode_t get_subscriber_qos_from_profile(
#            const std::string& profile_name,
#            SubscriberQos& qos) const;
#
#
#    /**
#     * Fills the TopicQos with the values of the XML profile.
#     *
#     * @param profile_name Topic profile name.
#     * @param qos TopicQos object where the qos is returned.
#     * @return RETCODE_OK if the profile exists. RETCODE_BAD_PARAMETER otherwise.
#     */
#    RTPS_DllAPI ReturnCode_t get_topic_qos_from_profile(
#            const std::string& profile_name,
#            TopicQos& qos) const;
#
#    /**
#     * Retrieves the list of topics that have been discovered in the domain and are not "ignored".
#     *
#     * @param[out]  topic_handles Reference to the vector where discovered topics will be returned
#     * @return RETCODE_OK if everything correct, error code otherwise
#     */
#    RTPS_DllAPI ReturnCode_t get_discovered_topics(
#            std::vector<InstanceHandle_t>& topic_handles) const;
#
#    /**
#     * Retrieves the Topic data of a discovered not ignored topic.
#     *
#     * @param[out]  topic_data Reference to the TopicBuiltinTopicData object to return the data
#     * @param topic_handle InstanceHandle of Topic to retrieve the data from
#     * @return RETCODE_OK if everything correct, PRECONDITION_NOT_MET if topic does not exist
#     */
#    RTPS_DllAPI ReturnCode_t get_discovered_topic_data(
#            builtin::TopicBuiltinTopicData& topic_data,
#            const InstanceHandle_t& topic_handle) const;
#
#    /**
#     * This operation checks whether or not the given handle represents an Entity that was created from the
#     * DomainParticipant.
#     *
#     * @param a_handle InstanceHandle of the entity to look for.
#     * @param recursive The containment applies recursively. That is, it applies both to entities
#     * (TopicDescription, Publisher, or Subscriber) created directly using the DomainParticipant as well as
#     * entities created using a contained Publisher, or Subscriber as the factory, and so forth. (default: true)
#     * @return True if entity is contained. False otherwise.
#     */
#    RTPS_DllAPI bool contains_entity(
#            const InstanceHandle_t& a_handle,
#            bool recursive = true) const;
#
#    /**
#     * This operation returns the current value of the time that the service uses to time-stamp data-writes
#     * and to set the reception-timestamp for the data-updates it receives.
#     *
#     * @param current_time Time_t reference where the current time is returned
#     * @return RETCODE_OK
#     */
#    RTPS_DllAPI ReturnCode_t get_current_time(
#            fastrtps::Time_t& current_time) const;
#
#    // DomainParticipant methods specific from Fast-DDS
#
#    /**
#     * Register a type in this participant.
#     *
#     * @param type TypeSupport.
#     * @param type_name The name that will be used to identify the Type.
#     * @return RETCODE_BAD_PARAMETER if the size of the name is 0, RERCODE_PRECONDITION_NOT_MET if there is another TypeSupport
#     * with the same name and RETCODE_OK if it is correctly registered.
#     */
#    RTPS_DllAPI ReturnCode_t register_type(
#            TypeSupport type,
#            const std::string& type_name);
#
#    /**
#     * Register a type in this participant.
#     *
#     * @param type TypeSupport.
#     * @return RETCODE_BAD_PARAMETER if the size of the name is 0, RERCODE_PRECONDITION_NOT_MET if there is another TypeSupport
#     * with the same name and RETCODE_OK if it is correctly registered.
#     */
#    RTPS_DllAPI ReturnCode_t register_type(
#            TypeSupport type);
#
#    /**
#     * Unregister a type in this participant.
#     *
#     * @param typeName Name of the type
#     * @return RETCODE_BAD_PARAMETER if the size of the name is 0, RERCODE_PRECONDITION_NOT_MET if there are entities using that
#     * TypeSupport and RETCODE_OK if it is correctly unregistered.
#     */
#    RTPS_DllAPI ReturnCode_t unregister_type(
#            const std::string& typeName);
#
#    /**
#     * This method gives access to a registered type based on its name.
#     *
#     * @param type_name Name of the type
#     * @return TypeSupport corresponding to the type_name
#     */
#    RTPS_DllAPI TypeSupport find_type(
#            const std::string& type_name) const;
#
#    /**
#     * @brief Getter for the participant names
#     *
#     * @return Vector with the names
#     */
#    RTPS_DllAPI std::vector<std::string> get_participant_names() const;
#
#    /**
#     * This method can be used when using a StaticEndpointDiscovery mechanism different that the one
#     * included in FastRTPS, for example when communicating with other implementations.
#     * It indicates the Participant that an Endpoint from the XML has been discovered and
#     * should be activated.
#     *
#     * @param partguid Participant GUID_t.
#     * @param userId User defined ID as shown in the XML file.
#     * @param kind EndpointKind (WRITER or READER)
#     * @return True if correctly found and activated.
#     */
#    RTPS_DllAPI bool new_remote_endpoint_discovered(
#            const fastrtps::rtps::GUID_t& partguid,
#            uint16_t userId,
#            fastrtps::rtps::EndpointKind_t kind);
#
#    /**
#     * @brief Getter for the resource event
#     *
#     * @return A reference to the resource event
#     */
#    RTPS_DllAPI fastrtps::rtps::ResourceEvent& get_resource_event() const;
#
#    /**
#     * When a DomainParticipant receives an incomplete list of TypeIdentifiers in a
#     * PublicationBuiltinTopicData or SubscriptionBuiltinTopicData, it may request the additional type
#     * dependencies by invoking the getTypeDependencies operation.
#     *
#     * @param in TypeIdentifier sequence
#     * @return SampleIdentity
#     */
#    RTPS_DllAPI fastrtps::rtps::SampleIdentity get_type_dependencies(
#            const fastrtps::types::TypeIdentifierSeq& in) const;
#
#    /**
#     * A DomainParticipant may invoke the operation getTypes to retrieve the TypeObjects associated with a
#     * list of TypeIdentifiers.
#     *
#     * @param in TypeIdentifier sequence
#     * @return SampleIdentity
#     */
#    RTPS_DllAPI fastrtps::rtps::SampleIdentity get_types(
#            const fastrtps::types::TypeIdentifierSeq& in) const;
#
#    /**
#     * Helps the user to solve all dependencies calling internally to the typelookup service
#     * and registers the resulting dynamic type.
#     * The registration will be perform asynchronously and the user will be notified through the
#     * given callback, which receives the type_name as unique argument.
#     * If the type is already registered, the function will return true, but the callback will not be called.
#     * If the given type_information is enough to build the type without using the typelookup service,
#     * it will return true and the callback will be never called.
#     *
#     * @param type_information
#     * @param type_name
#     * @param callback
#     * @return true if type is already available (callback will not be called). false if type isn't available yet
#     * (the callback will be called if negotiation is success, and ignored in other case).
#     */
#    RTPS_DllAPI ReturnCode_t register_remote_type(
#            const fastrtps::types::TypeInformation& type_information,
#            const std::string& type_name,
#            std::function<void(const std::string& name, const fastrtps::types::DynamicType_ptr type)>& callback);
#
#    /**
#     * Register a custom content filter factory, which can be used to create a ContentFilteredTopic.
#     *
#     * DDS specifies a SQL-like content filter to be used by content filtered topics.
#     * If this filter does not meet your filtering requirements, you can register a custom filter factory.
#     *
#     * To use a custom filter, a factory for it must be registered in the following places:
#     *
#     * - In any application that uses the custom filter factory to create a ContentFilteredTopic and the corresponding
#     *   DataReader.
#     *
#     * - In each application that writes the data to the applications mentioned above.
#     *
#     * For example, suppose Application A on the subscription side creates a Topic named X and a ContentFilteredTopic
#     * named filteredX (and a corresponding DataReader), using a previously registered content filter factory, myFilterFactory.
#     * With only that, you will have filtering at the subscription side.
#     * If you also want to perform filtering in any application that publishes Topic X, then you also need to register
#     * the same definition of the ContentFilterFactory myFilterFactory in that application.
#     *
#     * Each @c filter_class_name can only be used to register a content filter factory once per DomainParticipant.
#     *
#     * @param filter_class_name Name of the filter class. Cannot be nullptr, must not exceed 255 characters, and must
#     *                          be unique within this DomainParticipant.
#     * @param filter_factory    Factory of content filters to be registered. Cannot be nullptr.
#     *
#     * @return RETCODE_BAD_PARAMETER if any parameter is nullptr, or the filter_class_name exceeds 255 characters.
#     * @return RETCODE_PRECONDITION_NOT_MET if the filter_class_name has been already registered.
#     * @return RETCODE_PRECONDITION_NOT_MET if filter_class_name is FASTDDS_SQLFILTER_NAME.
#     * @return RETCODE_OK if the filter is correctly registered.
#     */
#    RTPS_DllAPI ReturnCode_t register_content_filter_factory(
#            const char* filter_class_name,
#            IContentFilterFactory* const filter_factory);
#
#    /**
#     * Lookup a custom content filter factory previously registered with register_content_filter_factory.
#     *
#     * @param filter_class_name Name of the filter class. Cannot be nullptr.
#     *
#     * @return nullptr if the given filter_class_name has not been previously registered on this DomainParticipant.
#     *         Otherwise, the content filter factory previously registered with the given filter_class_name.
#     */
#    RTPS_DllAPI IContentFilterFactory* lookup_content_filter_factory(
#            const char* filter_class_name);
#
#    /**
#     * Unregister a custom content filter factory previously registered with register_content_filter_factory.
#     *
#     * A filter_class_name can be unregistered only if it has been previously registered to the DomainParticipant with
#     * register_content_filter_factory.
#     *
#     * The unregistration of filter is not allowed if there are any existing ContentFilteredTopic objects that are
#     * using the filter.
#     *
#     * If there is any existing discovered DataReader with the same filter_class_name, filtering on the writer side will be
#     * stopped, but this operation will not fail.
#     *
#     * @param filter_class_name Name of the filter class. Cannot be nullptr.
#     *
#     * @return RETCODE_BAD_PARAMETER if the filter_class_name is nullptr.
#     * @return RERCODE_PRECONDITION_NOT_MET if the filter_class_name has not been previously registered.
#     * @return RERCODE_PRECONDITION_NOT_MET if there is any ContentFilteredTopic referencing the filter.
#     * @return RETCODE_OK if the filter is correctly unregistered.
#     */
#    RTPS_DllAPI ReturnCode_t unregister_content_filter_factory(
#            const char* filter_class_name);
#
#    /**
#     * @brief Check if the Participant has any Publisher, Subscriber or Topic
#     *
#     * @return true if any, false otherwise.
#     */
#    bool has_active_entities();
