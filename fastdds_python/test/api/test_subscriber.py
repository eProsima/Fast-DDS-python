import fastdds
import pytest
import time


class SubscriberListener (fastdds.SubscriberListener):
    def __init__(self):
        super().__init__()


class DataReaderListener (fastdds.DataReaderListener):
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
def participant_qos():
    return fastdds.DomainParticipantQos()


@pytest.fixture
def not_autoenable_participant_qos(participant_qos):
    participant_qos.entity_factory().autoenable_created_entities = False
    return participant_qos


@pytest.fixture
def participant(participant_qos):
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(0, participant_qos)


@pytest.fixture
def subscriber(participant, topic):
    subscriber = participant.create_subscriber(
            fastdds.SUBSCRIBER_QOS_DEFAULT)

    yield subscriber

    assert(fastdds.RETCODE_OK ==
           subscriber.delete_contained_entities())
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))


@pytest.fixture
def topic(participant):
    test_type = fastdds.TypeSupport(
            pytest.dds_type.CompleteTestTypePubSubType())
    participant.register_type(test_type, test_type.get_type_name())
    return participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)

@pytest.fixture
def test_type():
    return fastdds.TypeSupport(
            pytest.dds_type.CompleteTestTypePubSubType())

@pytest.fixture
def writer_participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)


@pytest.fixture
def writer_topic(writer_participant, test_type):
    writer_participant.register_type(test_type, test_type.get_type_name())
    return writer_participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def publisher(writer_participant):
    return writer_participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)

def test_access(subscriber):
    """
    This test checks:
    - ::resume_publications
    """
    assert(fastdds.RETCODE_UNSUPPORTED ==
           subscriber.begin_access())
    assert(fastdds.RETCODE_UNSUPPORTED ==
           subscriber.end_access())


def test_create_datareader(topic, subscriber):
    """
    This test checks:
    - Subscriber::create_datareader
    - Subscriber::delete_datareader
    - DataReader::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = DataReaderListener()
    assert(listener is not None)

    # Overload 1
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

    # Overload 2
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT, listener)
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

    def test(status_mask, listnr=None):
        """
        Test the entity creation using the type of StatusMask.
        """
        datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT, listnr, status_mask)
        assert(datareader is not None)
        assert(datareader.is_enabled())
        assert(status_mask == datareader.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               subscriber.delete_datareader(datareader))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), None)
    test(fastdds.StatusMask.all(), listener)
    test(fastdds.StatusMask.none(), listener)
    test(fastdds.StatusMask.data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(), listener)

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
         listener)


def test_create_datareader_with_profile(topic, subscriber):
    """
    This test checks:
    - Subscriber::create_datareader
    - Subscriber::delete_datareader
    - DataReader::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = DataReaderListener()
    assert(listener is not None)

    # Failure
    datareader = subscriber.create_datareader_with_profile(
            topic, 'no_exists_profile')
    assert(datareader is None)

    # Overload 1
    datareader = subscriber.create_datareader_with_profile(
            topic, 'test_datareader_profile')
    assert(datareader is not None)
    assert(datareader.is_enabled())
    qos = datareader.get_qos()
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           qos.reliability().kind)
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

    # Overload 2
    datareader = subscriber.create_datareader_with_profile(
            topic, 'test_datareader_profile', listener)
    assert(datareader is not None)
    assert(datareader.is_enabled())
    qos = datareader.get_qos()
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           qos.reliability().kind)
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

    def test(status_mask, listnr=None):
        """
        Test the entity creation using the type of StatusMask.
        """
        datareader = subscriber.create_datareader_with_profile(
                topic, 'test_datareader_profile', listnr, status_mask)
        assert(datareader is not None)
        assert(datareader.is_enabled())
        qos = datareader.get_qos()
        assert(fastdds.RELIABLE_RELIABILITY_QOS ==
               qos.reliability().kind)
        assert(status_mask == datareader.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               subscriber.delete_datareader(datareader))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), None)
    test(fastdds.StatusMask.all(), listener)
    test(fastdds.StatusMask.none(), listener)
    test(fastdds.StatusMask.data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(), listener)

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
         listener)


def test_delete_contained_entities(participant, topic, subscriber):
    """
    This test checks:
    - Subscriber::delete_contained_entities
    """
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    # Cannot delete subscriber with datareaders
    assert(fastdds.RETCODE_PRECONDITION_NOT_MET ==
           participant.delete_subscriber(subscriber))

    assert(fastdds.RETCODE_OK ==
           subscriber.delete_contained_entities())

    assert(subscriber.has_datareaders() is False)


def test_enable(not_autoenable_participant_qos, subscriber):
    """
    This test checks:
    - Subscriber::enable
    - Subscriber::is_enabled
    """
    assert(not subscriber.is_enabled())
    assert(fastdds.RETCODE_OK ==
           subscriber.enable())
    assert(subscriber.is_enabled())


def test_get_datareaders(topic, subscriber):
    """
    This test checks:
    - Subscriber::get_datareaders
    - Subscriber::has_datareaders
    """
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    assert(subscriber.has_datareaders())
    datareaders = fastdds.DataReaderVector()
    assert(fastdds.RETCODE_OK == subscriber.get_datareaders(datareaders))
    assert(1 == len(datareaders))
    assert(datareader == datareaders[0])

    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))


def test_get_instance_handle(participant, subscriber):
    """
    This test checks:
    - Subscriber::get_instance_handle
    - Subscriber::guid
    """
    ih = subscriber.get_instance_handle()
    assert(ih is not None)
    assert(ih.isDefined())
    guid = participant.guid()
    assert(guid is not None)

    assert(ih != fastdds.c_InstanceHandle_Unknown)
    assert(guid != fastdds.c_Guid_Unknown)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])


def test_get_participant(participant, subscriber):
    """
    This test checks:
    - Subscriber::get_participant
    """
    participant2 = subscriber.get_participant()
    assert(participant2 is not None)
    assert(participant == participant2)


def test_get_set_qos(subscriber):
    """
    This test checks:
    - Subscriber::get_qos
    - Subscriber::set_qos
    """
    qos = fastdds.SubscriberQos()
    qos.partition().push_back('PartitionTest')
    qos.partition().push_back('PartitionTest2')
    assert(fastdds.RETCODE_OK ==
           subscriber.set_qos(qos))

    qos2 = fastdds.SubscriberQos()
    assert(fastdds.RETCODE_OK ==
           subscriber.get_qos(qos2))


def test_get_set_listener(subscriber):
    """
    This test checks:
    - Publisher::get_listener
    - Publisher::set_listener
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    # Overload 1
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.RETCODE_OK ==
           subscriber.set_listener(listener))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())

    def test(status_mask):
        """
        Test the entity creation using the type of StatusMask.
        """
        listener = SubscriberListener()
        assert(listener is not None)
        assert(fastdds.RETCODE_OK ==
               subscriber.set_listener(listener, status_mask))
        assert(subscriber.get_listener() == listener)
        assert(status_mask == subscriber.get_status_mask())

    # Overload 2: Different status masks
    test(fastdds.StatusMask.all())
    test(fastdds.StatusMask.none())
    test(fastdds.StatusMask.data_available())
    test(fastdds.StatusMask.data_on_readers())
    test(fastdds.StatusMask.inconsistent_topic())
    test(fastdds.StatusMask.liveliness_changed())
    test(fastdds.StatusMask.liveliness_lost())
    test(fastdds.StatusMask.offered_deadline_missed())
    test(fastdds.StatusMask.offered_incompatible_qos())
    test(fastdds.StatusMask.publication_matched())
    test(fastdds.StatusMask.requested_deadline_missed())
    test(fastdds.StatusMask.requested_incompatible_qos())
    test(fastdds.StatusMask.sample_lost())
    test(fastdds.StatusMask.sample_rejected())
    test(fastdds.StatusMask.subscription_matched())

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
         fastdds.StatusMask.subscription_matched())


def test_lookup_datareader(topic, subscriber):
    """
    This test checks:
    - subscriber::lookup_datareader
    """
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    datareader2 = subscriber.lookup_datareader('Complete')
    assert(datareader2 is not None)
    assert(datareader == datareader2)

    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))


def test_listener_ownership(participant, writer_participant, topic,
                            writer_topic, publisher):

    def create_subcriber():
        listener = SubscriberListener()
        return participant.create_subscriber(
                fastdds.SUBSCRIBER_QOS_DEFAULT, listener)

    subscriber = create_subcriber()
    datareader = subscriber.create_datareader(
                topic, fastdds.DATAREADER_QOS_DEFAULT)
    datawriter = publisher.create_datawriter(
                writer_topic, fastdds.DATAWRITER_QOS_DEFAULT)
    time.sleep(1)
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.RETCODE_OK ==
           writer_participant.delete_topic(writer_topic))
    assert(fastdds.RETCODE_OK ==
           writer_participant.delete_publisher(publisher))
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(writer_participant))
    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))
