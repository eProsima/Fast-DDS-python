import fastdds
import pytest
import time


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

@pytest.fixture(params=['no_module', 'module'], autouse=True)
def data_type(request):
    if request.param == 'no_module':
        pytest.dds_type = __import__("test_complete")
    else:
        pytest.dds_type = __import__("eprosima.test.test_modules",
                                    fromlist=["test_modules"])

@pytest.fixture
def not_autoenable_factory():
    factory = fastdds.DomainParticipantFactory.get_instance()
    factory_qos = fastdds.DomainParticipantFactoryQos()
    factory.get_qos(factory_qos)
    factory_qos.entity_factory().autoenable_created_entities = False
    factory.set_qos(factory_qos)
    return factory


@pytest.fixture
def participant_qos():
    return fastdds.DomainParticipantQos()


@pytest.fixture
def testname_participant_qos(participant_qos):
    participant_qos.name('TestName')
    return participant_qos


@pytest.fixture
def participant(participant_qos):
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(0, participant_qos)

    yield participant

    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))


def test_contains_entity(participant):
    """
    This test checks:
    - DomainParticipant::contains_entity
    """
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    assert(participant.contains_entity(publisher.get_instance_handle()))

    assert(participant.contains_entity(fastdds.InstanceHandle_t()) is False)

    assert(fastdds.RETCODE_OK ==
           participant.delete_publisher(publisher))


def test_create_publisher(participant):
    """
    This test checks:
    - DomainParticipant::create_publisher
    - DomainParticipant::delete_publisher
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = PublisherListener()
    assert(listener is not None)

    # Overload 1
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    assert(publisher.is_enabled())
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_publisher(publisher))

    # Overload 2
    publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT, listener)
    assert(publisher is not None)
    assert(publisher.is_enabled())
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    assert(fastdds.RETCODE_OK ==
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
        assert(fastdds.RETCODE_OK ==
               participant.delete_publisher(publisher))
        publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT, listnr, status_mask_2)
        assert(publisher is not None)
        assert(publisher.is_enabled())
        assert(status_mask_2 == publisher.get_status_mask())
        assert(fastdds.RETCODE_OK ==
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


def test_create_publisher_with_profile(participant):
    """
    This test checks:
    - DomainParticipant::create_publisher_with_profile
    - DomainParticipant::delete_publisher
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = PublisherListener()
    assert(listener is not None)

    # Failure
    publisher = participant.create_publisher_with_profile(
            'no_exits_profile')
    assert(publisher is None)

    # Overload 1
    publisher = participant.create_publisher_with_profile(
            'test_publisher_profile')
    assert(publisher is not None)
    assert(publisher.is_enabled())
    qos = publisher.get_qos()
    assert('partition_name_c' == qos.partition()[0])
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_publisher(publisher))

    # Overload 2
    publisher = participant.create_publisher_with_profile(
            'test_publisher_profile', listener)
    assert(publisher is not None)
    assert(publisher.is_enabled())
    qos = publisher.get_qos()
    assert('partition_name_c' == qos.partition()[0])
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_publisher(publisher))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        publisher = participant.create_publisher_with_profile(
            'test_publisher_profile', listnr, status_mask_1)
        assert(publisher is not None)
        assert(publisher.is_enabled())
        qos = publisher.get_qos()
        assert('partition_name_c' == qos.partition()[0])
        assert(status_mask_1 == publisher.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               participant.delete_publisher(publisher))
        publisher = participant.create_publisher_with_profile(
            'test_publisher_profile', listnr, status_mask_2)
        assert(publisher is not None)
        assert(publisher.is_enabled())
        qos = publisher.get_qos()
        assert('partition_name_c' == qos.partition()[0])
        assert(status_mask_2 == publisher.get_status_mask())
        assert(fastdds.RETCODE_OK ==
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


def test_create_subscriber(participant):
    """
    This test checks:
    - DomainParticipant::create_subscriber
    - DomainParticipant::delete_subscriber
    - Subscriber::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = SubscriberListener()
    assert(listener is not None)

    # Overload 1
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    assert(subscriber.is_enabled())
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))

    # Overload 2
    subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT, listener)
    assert(subscriber is not None)
    assert(subscriber.is_enabled())
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    assert(fastdds.RETCODE_OK ==
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
        assert(fastdds.RETCODE_OK ==
               participant.delete_subscriber(subscriber))
        subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT, listnr, status_mask_2)
        assert(subscriber is not None)
        assert(subscriber.is_enabled())
        assert(status_mask_2 == subscriber.get_status_mask())
        assert(fastdds.RETCODE_OK ==
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


def test_create_subscriber_with_profile(participant):
    """
    This test checks:
    - DomainParticipant::create_subscriber_with_profile
    - DomainParticipant::delete_subscriber
    - Subscriber::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = SubscriberListener()
    assert(listener is not None)

    # Failure
    subscriber = participant.create_subscriber_with_profile(
            'no_exits_profile')
    assert(subscriber is None)

    # Overload 1
    subscriber = participant.create_subscriber_with_profile(
            'test_subscriber_profile')
    assert(subscriber is not None)
    assert(subscriber.is_enabled())
    qos = subscriber.get_qos()
    assert('partition_name_b' == qos.partition()[0])
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))

    # Overload 2
    subscriber = participant.create_subscriber_with_profile(
            'test_subscriber_profile', listener)
    assert(subscriber is not None)
    assert(subscriber.is_enabled())
    qos = subscriber.get_qos()
    assert('partition_name_b' == qos.partition()[0])
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        subscriber = participant.create_subscriber_with_profile(
            'test_subscriber_profile', listnr, status_mask_1)
        assert(subscriber is not None)
        assert(subscriber.is_enabled())
        qos = subscriber.get_qos()
        assert('partition_name_b' == qos.partition()[0])
        assert(status_mask_1 == subscriber.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               participant.delete_subscriber(subscriber))
        subscriber = participant.create_subscriber_with_profile(
            'test_subscriber_profile', listnr, status_mask_2)
        assert(subscriber is not None)
        assert(subscriber.is_enabled())
        qos = subscriber.get_qos()
        assert('partition_name_b' == qos.partition()[0])
        assert(status_mask_2 == subscriber.get_status_mask())
        assert(fastdds.RETCODE_OK ==
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


def test_create_and_delete_topic(participant):
    """
    This test checks:
    - DomainParticipant::create_topic
    - DomainParticipant::delete_topic
    - Topic::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = TopicListener()
    assert(listener is not None)

    test_type = fastdds.TypeSupport(
        pytest.dds_type.CompleteTestTypePubSubType())

    # Overload 1 - Failing (because the type is not registered yet)
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is None)

    # Now register the type
    assert(fastdds.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))

    # Overload 1 - Success
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    assert(topic.is_enabled())
    assert(fastdds.StatusMask.all() == topic.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))

    # Overload 2
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT,
            listener)
    assert(topic is not None)
    assert(topic.is_enabled())
    assert(fastdds.StatusMask.all() == topic.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        topic = participant.create_topic(
            "Complete", test_type.get_type_name(),
            fastdds.TOPIC_QOS_DEFAULT, listnr, status_mask_1)
        assert(topic is not None)
        assert(topic.is_enabled())
        assert(status_mask_1 == topic.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               participant.delete_topic(topic))
        topic = participant.create_topic(
            "Complete", test_type.get_type_name(),
            fastdds.TOPIC_QOS_DEFAULT, listnr, status_mask_2)
        assert(topic is not None)
        assert(topic.is_enabled())
        assert(status_mask_2 == topic.get_status_mask())
        assert(fastdds.RETCODE_OK ==
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


def test_delete_contained_entities(participant):
    publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(pytest.dds_type.CompleteTestTypePubSubType())
    assert(fastdds.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)

    # Cannot delete participant without deleting its contained entities
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.RETCODE_PRECONDITION_NOT_MET ==
           factory.delete_participant(participant))

    assert(fastdds.RETCODE_OK ==
           participant.delete_contained_entities())


def test_enable(not_autoenable_factory, participant):
    """
    This test checks:
    - DomainParticipant::enable
    - DomainParticipant::is_enabled
    """
    assert(not participant.is_enabled())
    assert(fastdds.RETCODE_OK ==
           participant.enable())
    assert(participant.is_enabled())
    factory_qos = fastdds.DomainParticipantFactoryQos()
    factory_qos.entity_factory().autoenable_created_entities = True
    assert(fastdds.RETCODE_OK ==
           not_autoenable_factory.set_qos(factory_qos))


def test_find_topic(participant):
    """
    This test checks:
    - DomainParticipant::find_topic
    """
    test_type = fastdds.TypeSupport(pytest.dds_type.CompleteTestTypePubSubType())
    assert(fastdds.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))

    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)

    topic_copy = participant.find_topic("Complete", fastdds.Duration_t(1, 0))
    assert(topic.get_type_name() == topic_copy.get_type_name())
    assert(topic.get_name() == topic_copy.get_name())
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic_copy))

    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))


def test_get_builtin_subscriber(participant):
    """
    This test checks:
    - DomainParticipant::get_builtin_subscriber
    """
    builtin_subscriber = participant.get_builtin_subscriber()
    assert(builtin_subscriber is None)
    # assert(builtin_subscriber.is_enabled())


def test_get_discovered_participants(participant):
    """
    This test checks:
    - DomainParticipant::get_discovered_participants
    - DomainParticipant::get_discovered_participant_data
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant2 = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant2 is not None)

    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.RETCODE_UNSUPPORTED ==
           participant.get_discovered_participants(ihs))

    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant2))


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

    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_instance_handle(participant):
    """
    This test checks:
    - DomainParticipant::get_instance_handle
    - DomainParticipant::guid
    """
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


def test_get_set_listener(participant):
    """
    This test checks:
    - DomainParticipant::get_listener
    - DomainParticipant::set_listener
    - DomainParticipant::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    # Overload 1
    listener = DomainParticipantListener()
    assert(listener is not None)
    assert(fastdds.RETCODE_OK ==
           participant.set_listener(listener))
    assert(participant.get_listener() == listener)
    assert(fastdds.StatusMask.all() == participant.get_status_mask())

    def test(status_mask_1, status_mask_2):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        listener = DomainParticipantListener()
        assert(listener is not None)
        assert(fastdds.RETCODE_OK ==
               participant.set_listener(listener, status_mask_1))
        assert(participant.get_listener() == listener)
        assert(status_mask_1 == participant.get_status_mask())
        listener = DomainParticipantListener()
        assert(listener is not None)
        assert(fastdds.RETCODE_OK ==
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


def test_get_partitipant_names(testname_participant_qos, participant):
    """
    This test checks:
    - DomainParticipant::get_participant_names
    """
    names = participant.get_participant_names()
    assert('TestName' == names[0])


def test_get_set_qos(participant):
    """
    This test checks:
    - DomainParticipant::get_qos
    - DomainParticipant::set_qos
    """
    qos = fastdds.DomainParticipantQos()
    assert(fastdds.RETCODE_OK == participant.get_qos(qos))
    qos.user_data().push_back(1)
    qos.user_data().push_back(2)
    assert(2 == len(qos.user_data()))

    assert(fastdds.RETCODE_OK ==
           participant.set_qos(qos))

    qos2 = fastdds.DomainParticipantQos()
    assert(fastdds.RETCODE_OK ==
           participant.get_qos(qos2))
    assert(2 == len(qos2.user_data()))
    assert(1 == qos2.user_data()[0])
    assert(2 == qos2.user_data()[1])


def test_ignore_participant(participant):
    """
    This test checks:
    - DomainParticipant::ignore_participant
    """
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.RETCODE_OK ==
           participant.ignore_participant(ih))

def test_ignore_publication(participant):
    """
    This test checks:
    - DomainParticipant::ignore_publication
    """
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.RETCODE_UNSUPPORTED ==
           participant.ignore_publication(ih))


def test_ignore_subscription(participant):
    """
    This test checks:
    - DomainParticipant::ignore_subscription
    """
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.RETCODE_UNSUPPORTED ==
           participant.ignore_subscription(ih))


def test_ignore_topic(participant):
    """
    This test checks:
    - DomainParticipant::ignore_topic
    """
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.RETCODE_UNSUPPORTED ==
           participant.ignore_topic(ih))


def test_lookup_topicdescription(participant):
    """
    This test checks:
    - DomainParticipant::lookup_topicdescription
    """
    test_type = fastdds.TypeSupport(pytest.dds_type.CompleteTestTypePubSubType())
    assert(fastdds.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))

    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)

    topic_desc = participant.lookup_topicdescription("Complete")
    assert(topic_desc is not None)
    assert(topic.get_type_name() == topic_desc.get_type_name())
    assert(topic.get_name() == topic_desc.get_name())

    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))


def test_listener_ownership():
    factory = fastdds.DomainParticipantFactory.get_instance()

    def second_participant():
        listener = DomainParticipantListener()
        return factory.create_participant(0, fastdds.PARTICIPANT_QOS_DEFAULT,
                                          listener, fastdds.StatusMask.all())

    participant2 = second_participant()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    time.sleep(1)
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant2))
