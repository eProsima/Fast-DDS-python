import fastdds
import test_complete


class SubscriberListener (fastdds.SubscriberListener):
    def __init__(self):
        super().__init__()


class DataReaderListener (fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()


def test_access():
    """
    This test checks:
    - ::resume_publications
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)

    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           subscriber.begin_access())
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           subscriber.end_access())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_and_delete_datareader():
    """
    This test checks:
    - Subscriber::create_datareader
    - Subscriber::delete_datareader
    - DataReader::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    # Overload 1 - Success
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    listener = DataReaderListener()
    assert(listener is not None)

    # Overload 1
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

    # Overload 2
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT, listener)
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT, listnr, status_mask_1)
        assert(datareader is not None)
        assert(datareader.is_enabled())
        assert(status_mask_1 == datareader.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               subscriber.delete_datareader(datareader))
        datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT, listnr, status_mask_2)
        assert(datareader is not None)
        assert(datareader.is_enabled())
        assert(status_mask_2 == datareader.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               subscriber.delete_datareader(datareader))

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
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_deleted_contained_entities():
    """
    This test checks:
    - Subscriber::delete_contained_entities
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_contained_entities())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_enable():
    """
    This test checks:
    - Subscriber::enable
    - Subscriber::is_enabled
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    qos = fastdds.DomainParticipantQos()
    qos.entity_factory().autoenable_created_entities = False
    participant = factory.create_participant(0, qos)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)

    assert(not subscriber.is_enabled())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.enable())
    assert(subscriber.is_enabled())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_datareaders():
    """
    This test checks:
    - Subscriber::get_datareaders
    - Subscriber::has_datareaders
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    assert(subscriber.has_datareaders())
    datareaders = fastdds.DataReaderVector()
    assert(subscriber.get_datareaders(datareaders))
    assert(1 == len(datareaders))
    assert(datareader == datareaders[0])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_instance_handle():
    """
    This test checks:
    - Subscriber::get_instance_handle
    - Subscriber::guid
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)

    ih = subscriber.get_instance_handle()
    assert(ih is not None)
    assert(ih.isDefined())
    guid = participant.guid()
    assert(guid is not None)

    assert(ih != fastdds.c_InstanceHandle_Unknown)
    assert(guid != fastdds.c_Guid_Unknown)

    assert(guid.guidPrefix.value[0] == ih.value[0])
    assert(guid.guidPrefix.value[1] == ih.value[1])
    assert(guid.guidPrefix.value[2] == ih.value[2])
    assert(guid.guidPrefix.value[3] == ih.value[3])
    assert(guid.guidPrefix.value[4] == ih.value[4])
    assert(guid.guidPrefix.value[5] == ih.value[5])
    assert(guid.guidPrefix.value[6] == ih.value[6])
    assert(guid.guidPrefix.value[7] == ih.value[7])
    assert(guid.guidPrefix.value[8] == ih.value[8])
    assert(guid.guidPrefix.value[9] == ih.value[9])
    assert(guid.guidPrefix.value[10] == ih.value[10])
    assert(guid.guidPrefix.value[11] == ih.value[11])
    # assert(guid.entityId.value[0] == ih.value[12])
    # assert(guid.entityId.value[1] == ih.value[13])
    # assert(guid.entityId.value[2] == ih.value[14])
    # assert(guid.entityId.value[3] == ih.value[15])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_participant():
    """
    This test checks:
    - Subscriber::get_participant
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)

    participant2 = subscriber.get_participant()
    assert(participant2 is not None)
    assert(participant == participant2)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_qos():
    """
    This test checks:
    - Subscriber::get_qos
    - Subscriber::set_qos
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    qos = fastdds.SubscriberQos()
    subscriber = participant.create_subscriber(qos)
    assert(subscriber is not None)

    qos.partition().push_back('PartitionTest')
    qos.partition().push_back('PartitionTest2')
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_qos(qos))

    qos2 = fastdds.SubscriberQos()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.get_qos(qos2))

    assert(2 == len(qos.partition()))
    assert('PartitionTest' == qos.partition()[0])
    assert('PartitionTest2' == qos.partition()[1])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_listener():
    """
    This test checks:
    - Publisher::get_listener
    - Publisher::set_listener
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)

    # Overload 1
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(listener))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())

    # Overload 2
    # - StatusMask.none
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.none()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.none() == subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_none()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_none() == subscriber.get_status_mask())
    # - StatusMask.data_available
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.data_available()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.data_available() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_data_available()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_data_available() ==
           subscriber.get_status_mask())
    # - StatusMask.data_on_readers
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.data_on_readers()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.data_on_readers() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_data_on_readers()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_data_on_readers() ==
           subscriber.get_status_mask())
    # - StatusMask.inconsistent_topic
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.inconsistent_topic()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.inconsistent_topic() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_inconsistent_topic()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_inconsistent_topic() ==
           subscriber.get_status_mask())
    # - StatusMask.liveliness_changed
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.liveliness_changed()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.liveliness_changed() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_liveliness_changed()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_liveliness_changed() ==
           subscriber.get_status_mask())
    # - StatusMask.liveliness_lost
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.liveliness_lost()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.liveliness_lost() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_liveliness_lost()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_liveliness_lost() ==
           subscriber.get_status_mask())
    # - StatusMask.offered_deadline_missed
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.offered_deadline_missed()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.offered_deadline_missed() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_offered_deadline_missed()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_offered_deadline_missed() ==
           subscriber.get_status_mask())
    # - StatusMask.offered_incompatible_qos
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.offered_incompatible_qos()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.offered_incompatible_qos() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_offered_incompatible_qos()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_offered_incompatible_qos() ==
           subscriber.get_status_mask())
    # - StatusMask.publication_matched
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.publication_matched()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.publication_matched() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_publication_matched()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_publication_matched() ==
           subscriber.get_status_mask())
    # - StatusMask.requested_deadline_missed
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.requested_deadline_missed()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.requested_deadline_missed() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_requested_deadline_missed()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_requested_deadline_missed() ==
           subscriber.get_status_mask())
    # - StatusMask.requested_incompatible_qos
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.requested_incompatible_qos()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.requested_incompatible_qos() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_requested_incompatible_qos()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_requested_incompatible_qos() ==
           subscriber.get_status_mask())
    # - StatusMask.sample_lost
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.sample_lost()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.sample_lost() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_sample_lost()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_sample_lost() ==
           subscriber.get_status_mask())
    # - StatusMask.sample_rejected
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.sample_rejected()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.sample_rejected() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_sample_rejected()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_sample_rejected() ==
           subscriber.get_status_mask())
    # - StatusMask.subscription_matched
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.subscription_matched()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.subscription_matched() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_subscription_matched()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_subscription_matched() ==
           subscriber.get_status_mask())
    # - StatusMask.all
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask.all()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.all() ==
           subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener, fastdds.StatusMask_all()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_all() ==
           subscriber.get_status_mask())
    # - Mix all  values of StatusMask
    listener = SubscriberListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(
               listener,
               fastdds.StatusMask.data_available() <<
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
               fastdds.StatusMask.subscription_matched()))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask.all() == subscriber.get_status_mask())
    listener = SubscriberListener()
    assert(listener is not None)
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
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.set_listener(listener, m))
    assert(subscriber.get_listener() == listener)
    assert(fastdds.StatusMask_all() == subscriber.get_status_mask())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_lookup_datareader():
    """
    This test checks:
    - subscriber::lookup_datareader
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    # Overload 1 - Success
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    datareader2 = subscriber.lookup_datareader('Complete')
    assert(datareader2 is not None)
    assert(datareader == datareader2)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
