import fastdds
import pytest
import time

class PublisherListener (fastdds.PublisherListener):
    def __init__(self):
        super().__init__()


class DataWriterListener (fastdds.DataWriterListener):
    def __init__(self):
        super().__init__()

@pytest.fixture(params=['no_module', 'module'], autouse=True)
def data_type(request):
    if request.param == 'no_module':
        pytest.dds_type = __import__("test_complete")
    else:
        pytest.dds_type = __import__("eprosima.test.test_modules",
                                    fromlist=[None])

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
def publisher(participant, topic):
    publisher = participant.create_publisher(
            fastdds.PUBLISHER_QOS_DEFAULT)

    yield publisher

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
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
def reader_participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)

@pytest.fixture
def reader_topic(reader_participant, test_type):
    reader_participant.register_type(test_type, test_type.get_type_name())
    return reader_participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def subscriber(reader_participant):
    return reader_participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)

def test_coherent_changes(publisher):
    """
    This test checks:
    - Publisher::begin_coherent_changes
    - Publisher::end_coherent_changes
    """
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.begin_coherent_changes())
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.end_coherent_changes())


def test_create_datawriter(topic, publisher):
    """
    This test checks:
    - Publisher::create_datawriter
    - Publisher::delete_datawriter
    - DataWriter::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = DataWriterListener()
    assert(listener is not None)

    # Overload 1
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))

    # Overload 2
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT, listener)
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT, listnr, status_mask_1)
        assert(datawriter is not None)
        assert(datawriter.is_enabled())
        assert(status_mask_1 == datawriter.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               publisher.delete_datawriter(datawriter))
        datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT, listnr, status_mask_2)
        assert(datawriter is not None)
        assert(datawriter.is_enabled())
        assert(status_mask_2 == datawriter.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               publisher.delete_datawriter(datawriter))

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


def test_create_datawriter_with_profile(topic, publisher):
    """
    This test checks:
    - Publisher::create_datawriter_with_profile
    - Publisher::delete_datawriter
    - DataWriter::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    listener = DataWriterListener()
    assert(listener is not None)

    # Failure
    datawriter = publisher.create_datawriter_with_profile(
            topic, 'no_exits_profile')
    assert(datawriter is None)

    # Overload 1
    datawriter = publisher.create_datawriter_with_profile(
            topic, 'test_datawriter_profile')
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    qos = datawriter.get_qos()
    assert(fastdds.VOLATILE_DURABILITY_QOS ==
           qos.durability().kind)
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))

    # Overload 2
    datawriter = publisher.create_datawriter_with_profile(
            topic, 'test_datawriter_profile', listener)
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    qos = datawriter.get_qos()
    assert(fastdds.VOLATILE_DURABILITY_QOS ==
           qos.durability().kind)
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        datawriter = publisher.create_datawriter_with_profile(
                topic, 'test_datawriter_profile', listnr, status_mask_1)
        assert(datawriter is not None)
        assert(datawriter.is_enabled())
        qos = datawriter.get_qos()
        assert(fastdds.VOLATILE_DURABILITY_QOS ==
               qos.durability().kind)
        assert(status_mask_1 == datawriter.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               publisher.delete_datawriter(datawriter))
        datawriter = publisher.create_datawriter_with_profile(
                topic, 'test_datawriter_profile', listnr, status_mask_2)
        assert(datawriter is not None)
        assert(datawriter.is_enabled())
        qos = datawriter.get_qos()
        assert(fastdds.VOLATILE_DURABILITY_QOS ==
               qos.durability().kind)
        assert(status_mask_2 == datawriter.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               publisher.delete_datawriter(datawriter))

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


def test_deleted_contained_entities(participant, topic, publisher):
    """
    This test checks:
    - Publisher::delete_contained_entities
    """
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    # Cannot delete publisher with datawriters
    assert(fastdds.ReturnCode_t.RETCODE_PRECONDITION_NOT_MET ==
           participant.delete_publisher(publisher))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_contained_entities())
    assert(publisher.has_datawriters() is False)


def test_enable(not_autoenable_participant_qos, publisher):
    """
    This test checks:
    - Publisher::enable
    - Publisher::is_enabled
    """
    assert(not publisher.is_enabled())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.enable())
    assert(publisher.is_enabled())


def test_get_datawriters(topic, publisher):
    """
    This test checks:
    - Publisher::get_datawriters
    - Publisher::has_datawriters
    """
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    assert(publisher.has_datawriters())
    datawriters = fastdds.DataWriterVector()
    assert(publisher.get_datawriters(datawriters))
    assert(1 == len(datawriters))
    assert(datawriter == datawriters[0])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))


def test_get_instance_handle(participant, publisher):
    """
    This test checks:
    - Publisher::get_instance_handle
    - Publisher::guid
    """
    ih = publisher.get_instance_handle()
    assert(ih is not None)
    assert(ih.isDefined())
    guid = participant.guid()
    assert(guid is not None)

    assert(ih != fastdds.c_InstanceHandle_Unknown)
    assert(guid != fastdds.c_Guid_Unknown)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])


def test_get_participant(participant, publisher):
    """
    This test checks:
    - Publisher::get_participant
    """
    participant2 = publisher.get_participant()
    assert(participant2 is not None)
    assert(participant == participant2)


def test_get_set_qos(publisher):
    """
    This test checks:
    - Publisher::get_qos
    - Publisher::set_qos
    """
    qos = fastdds.PublisherQos()

    qos.partition().push_back('PartitionTest')
    qos.partition().push_back('PartitionTest2')
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_qos(qos))

    qos2 = fastdds.PublisherQos()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.get_qos(qos2))

    assert(2 == len(qos.partition()))
    assert('PartitionTest' == qos.partition()[0])
    assert('PartitionTest2' == qos.partition()[1])


def test_get_set_listener(publisher):
    """
    This test checks:
    - Publisher::get_listener
    - Publisher::set_listener
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    # Overload 1
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(listener))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())

    def test(status_mask_1, status_mask_2):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        listener = PublisherListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               publisher.set_listener(listener, status_mask_1))
        assert(publisher.get_listener() == listener)
        assert(status_mask_1 == publisher.get_status_mask())
        listener = PublisherListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               publisher.set_listener(listener, status_mask_2))
        assert(publisher.get_listener() == listener)
        assert(status_mask_2 == publisher.get_status_mask())

    # Overload 2: Different status masks
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


def test_lookup_datawriter(topic, publisher):
    """
    This test checks:
    - Publisher::lookup_datawriter
    """
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    datawriter2 = publisher.lookup_datawriter('Complete')
    assert(datawriter2 is not None)
    assert(datawriter == datawriter2)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))


def test_suspend_publications(publisher):
    """
    This test checks:
    - Publisher::suspend_publications
    - Publisher::resume_publications
    """
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.suspend_publications())
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.resume_publications())


def test_wait_for_acknowlegments(publisher):
    """
    This test checks:
    - Publisher::wait_for_acknowledgments
    """
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.wait_for_acknowledgments(fastdds.Duration_t(3, 0)))
    # TODO Test a timeout


def test_listener_ownership(participant, reader_participant, topic,
                            reader_topic, subscriber):

    def create_publisher():
        listener = PublisherListener()
        return participant.create_publisher(
                fastdds.PUBLISHER_QOS_DEFAULT, listener)

    publisher = create_publisher()
    datawriter = publisher.create_datawriter(
                topic, fastdds.DATAWRITER_QOS_DEFAULT)
    datareader = subscriber.create_datareader(
                reader_topic, fastdds.DATAREADER_QOS_DEFAULT)
    time.sleep(1)
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           reader_participant.delete_topic(reader_topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           reader_participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(reader_participant))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))