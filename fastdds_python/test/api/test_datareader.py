import fastdds
import test_complete


class DataReaderListener (fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()


def create_querycondition():
    """
    This test checks:
    - DataReader::create_querycondition
    - DataReader::delete_contained_entities
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    sv = fastdds.SampleStateKindVector()
    vv = fastdds.ViewStateKindVector()
    iv = fastdds.InstanceStateKindVector()
    qp = fastdds.StringVector()

    querycondition = datareader.create_querycondition(
               sv, vv, iv, "", qp)
    assert(querycondition is None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.delete_contained_entities())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_readcondition():
    """
    This test checks:
    - DataReader::create_readcondition
    - DataReader::delete_readcondition
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    sv = fastdds.SampleStateKindVector()
    vv = fastdds.ViewStateKindVector()
    iv = fastdds.InstanceStateKindVector()
    readcondition = datareader.create_readcondition(
               sv, vv, iv)
    assert(readcondition is None)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.delete_readcondition(readcondition))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_first_untaken():
    """
    This test checks:
    - DataReader::get_first_untaken_info
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader = subscriber.create_datareader(
            topic, datareader_qos)
    assert(datareader is not None)

    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.get_first_untaken_info(info))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_first_untaken_info(info))
    assert(info.valid_data)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_instance_handle():
    """
    This test checks:
    - DataReader::guid
    - DataReader::get_instance_handle
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)

    guid = datareader.guid()
    assert(fastdds.c_Guid_Unknown != guid)
    ih = datareader.get_instance_handle()
    assert(fastdds.c_InstanceHandle_Unknown != ih)

    for i in range(0, 12):
       assert(guid.guidPrefix.value[i] == ih.value[i])

    for i in range(0, 4):
       assert(guid.entityId.value[i] == ih.value[12+i])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_key_value():
    """
    This test checks:
    - DataReader::get_key_value
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    sample = test_complete.KeyedCompleteTestType()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_key_value(sample, ih))
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_listener():
    """
    This test checks:
    - DataReader::get_listener
    - DataReader::set_listener
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
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    # Overload 1
    listener = DataReaderListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.set_listener(listener))
    assert(datareader.get_listener() == listener)
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())

    def test(status_mask_1, status_mask_2):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        listener = DataReaderListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               datareader.set_listener(listener, status_mask_1))
        assert(datareader.get_listener() == listener)
        assert(status_mask_1 == datareader.get_status_mask())
        listener = DataReaderListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               datareader.set_listener(listener, status_mask_2))
        assert(datareader.get_listener() == listener)
        assert(status_mask_2 == datareader.get_status_mask())

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

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_listening_locators():
    """
    This test checks:
    - DataReader::get_listening_locators
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    locator_list = fastdds.LocatorList()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_listening_locators(locator_list))
    assert(0 < locator_list.size())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_liveliness_changed_status():
    """
    This test checks:
    - DataReader::get_liveliness_changed_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    status = fastdds.LivelinessChangedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_liveliness_changed_status(status))
    assert(0 == status.alive_count)
    assert(0 == status.alive_count_change)
    assert(0 == status.not_alive_count)
    assert(0 == status.not_alive_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_publication_handle)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_matched_publication_data():
    """
    This test checks:
    - DataWriter::get_matched_publication_data
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    pub_data = fastdds.PublicationBuiltinTopicData()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_matched_publication_data(pub_data, ih))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_matched_publications():
    """
    This test checks:
    - DataReader::get_matched_publications
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_matched_publications(ihs))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_requested_deadline_missed_status():
    """
    This test checks:
    - DataReader::get_requested_deadline_missed_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    status = fastdds.RequestedDeadlineMissedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_requested_deadline_missed_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_instance_handle)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_requested_incompatible_qos_status():
    """
    This test checks:
    - DataReader::get_requested_deadline_missed_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    status = fastdds.RequestedIncompatibleQosStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_requested_incompatible_qos_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.INVALID_QOS_POLICY_ID == status.last_policy_id)
    assert(fastdds.NEXT_QOS_POLICY_ID == status.policies.size())
    id = 0
    for policy in status.policies:
        assert(0 == policy.count)
        assert(id == policy.policy_id)
        id += 1

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_sample_lost_status():
    """
    This test checks:
    - DataReader::get_sample_lost_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    status = fastdds.SampleLostStatus()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_sample_lost_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_sample_rejected_status():
    """
    This test checks:
    - DataReader::get_sample_rejected_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    status = fastdds.SampleRejectedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_sample_rejected_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_subscription_matched_status():
    """
    This test checks:
    - DataReader::get_subscription_matched_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    status = fastdds.SubscriptionMatchedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_subscription_matched_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(0 == status.current_count)
    assert(0 == status.current_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_publication_handle)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_subscriber():
    """
    This test checks:
    - DataReader::get_subscriber
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    sub = datareader.get_subscriber()
    assert(sub == subscriber)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_topicdescription():
    """
    This test checks:
    - DataReader::get_topicdescription
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    topic_aux = datareader.get_topicdescription()
    assert(topic.get_impl() == topic_aux.get_impl())
    assert(topic.get_type_name() == topic_aux.get_type_name())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_unread_count():
    """
    This test checks:
    - DataReader::get_unread_count
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader = subscriber.create_datareader(
            topic, datareader_qos)
    assert(datareader is not None)

    assert(0 == datareader.get_unread_count())

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(1 == datareader.get_unread_count())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_is_sample_valid():
    """
    This test checks:
    - DataReader::is_sample_valid
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader = subscriber.create_datareader(
            topic, datareader_qos)
    assert(datareader is not None)

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    data = test_complete.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.read_next_sample(data, info))
    assert(datareader.is_sample_valid(data, info))
    assert(sample.int16_field() == data.int16_field())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_lookup_instance():
    """
    This test checks:
    - DataReader::lookup_instance
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    ih = datareader.lookup_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_read():
    """
    This test checks:
    - DataReader::wait_for_historical_data
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    #data_seq = test_complete.CompleteTestTypeSeq()
    #info_seq = fastdds.SampleInfoSeq()
    #assert(fastdds.ReturnCode_t.RETCODE_NO_DATA == datareader.read(
    #    data_seq, info_seq))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_read_next_sample():
    """
    This test checks:
    - DataReader::read_next_sample
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader = subscriber.create_datareader(
            topic, datareader_qos)
    assert(datareader is not None)

    data = test_complete.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA == datareader.read_next_sample(
        data, info))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.read_next_sample(data, info))
    assert(info.valid_data)
    assert(sample.int16_field() == data.int16_field())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_take_next_sample():
    """
    This test checks:
    - DataReader::take_next_sample
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader = subscriber.create_datareader(
            topic, datareader_qos)
    assert(datareader is not None)

    data = test_complete.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA == datareader.take_next_sample(
        data, info))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.take_next_sample(data, info))
    assert(info.valid_data)
    assert(sample.int16_field() == data.int16_field())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_type():
    """
    This test checks:
    - DataReader::type
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    test_type_aux = datareader.type()
    assert(test_type == test_type_aux)
    assert(test_type.get_type_name() == test_type_aux.get_type_name())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_wait_for_historical_data():
    """
    This test checks:
    - DataReader::wait_for_historical_data
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.wait_for_historical_data(fastdds.Duration_t(0, 100)))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_wait_for_unread_message():
    """
    This test checks:
    - DataReader::wait_for_unread_message
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT)
    assert(datareader is not None)

    assert(not datareader.wait_for_unread_message(fastdds.Duration_t(0, 100)))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))

#    /** @name Read or take data methods.
#     * Methods to read or take data from the History.
#     */
#
#    ///@{
#
#    /**
#     * Access a collection of data samples from the DataReader.
#     *
#     * This operation accesses a collection of Data values from the DataReader. The caller can limit the size
#     * of the returned collection with the @c max_samples parameter.
#     *
#     * The properties of the @c data_values collection and the setting of the @ref PresentationQosPolicy may
#     * impose further limits on the size of the returned ‘list.’
#     *
#     * 1. If @ref PresentationQosPolicy::access_scope is @ref INSTANCE_PRESENTATION_QOS, then the returned
#     *    collection is a 'list' where samples belonging to the same data-instance are consecutive.
#     *
#     * 2. If @ref PresentationQosPolicy::access_scope is @ref TOPIC_PRESENTATION_QOS and
#     *    @ref PresentationQosPolicy::ordered_access is set to @c false, then the returned collection is a
#     *    'list' where samples belonging to the same data-instance are consecutive.
#     *
#     * 3. If @ref PresentationQosPolicy::access_scope is @ref TOPIC_PRESENTATION_QOS and
#     *    @ref PresentationQosPolicy::ordered_access is set to @c true, then the returned collection is a
#     *    'list' where samples belonging to the same instance may or may not be consecutive. This is because to
#     *    preserve order it may be necessary to mix samples from different instances.
#     *
#     * 4. If @ref PresentationQosPolicy::access_scope is @ref GROUP_PRESENTATION_QOS and
#     *    @ref PresentationQosPolicy::ordered_access is set to @c false, then the returned collection is a
#     *    'list' where samples belonging to the same data instance are consecutive.
#     *
#     * 5. If @ref PresentationQosPolicy::access_scope is @ref GROUP_PRESENTATION_QOS and
#     *    @ref PresentationQosPolicy::ordered_access is set to @c true, then the returned collection contains at
#     *    most one sample. The difference in this case is due to the fact that it is required that the application
#     *    is able to read samples belonging to different DataReader objects in a specific order.
#     *
#     * In any case, the relative order between the samples of one instance is consistent with the
#     * @ref eprosima::fastdds::dds::DestinationOrderQosPolicy "DestinationOrderQosPolicy":
#     *
#     * - If @ref DestinationOrderQosPolicy::kind is @ref BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS, samples
#     *   belonging to the same instances will appear in the relative order in which there were received (FIFO,
#     *   earlier samples ahead of the later samples).
#     *
#     * - If @ref DestinationOrderQosPolicy::kind is @ref BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS, samples
#     *   belonging to the same instances will appear in the relative order implied by the source_timestamp (FIFO,
#     *   smaller values of source_timestamp ahead of the larger values).
#     *
#     * The actual number of samples returned depends on the information that has been received by the middleware
#     * as well as the @ref HistoryQosPolicy, @ref ResourceLimitsQosPolicy, and
#     * @ref eprosima::fastdds::dds::ReaderResourceLimitsQos "ReaderResourceLimitsQos":
#     *
#     * - In the case where the @ref HistoryQosPolicy::kind is KEEP_LAST_HISTORY_QOS, the call will return at most
#     *   @ref HistoryQosPolicy::depth samples per instance.
#     *
#     * - The maximum number of samples returned is limited by @ref ResourceLimitsQosPolicy::max_samples, and by
#     *   @ref ReaderResourceLimitsQos::max_samples_per_read.
#     *
#     * - For multiple instances, the number of samples returned is additionally limited by the product
#     *   (@ref ResourceLimitsQosPolicy::max_samples_per_instance * @ref ResourceLimitsQosPolicy::max_instances).
#     *
#     * - If ReaderResourceLimitsQos::sample_infos_allocation has a maximum limit, the number of samples returned
#     *   may also be limited if insufficient @ref SampleInfo resources are available.
#     *
#     * If the operation succeeds and the number of samples returned has been limited (by means of a maximum limit,
#     * as listed above, or insufficient @ref SampleInfo resources), the call will complete successfully and provide
#     * those samples the reader is able to return. The user may need to make additional calls, or return outstanding
#     * loaned buffers in the case of insufficient resources, in order to access remaining samples.
#     *
#     * In addition to the collection of samples, the read operation also uses a collection of @ref SampleInfo
#     * structures (@c sample_infos).
#     *
#     * The initial (input) properties of the @c data_values and @c sample_infos collections will determine the
#     * precise behavior of this operation. For the purposes of this description the collections are modeled as having
#     * three properties:
#     *
#     * - the current length (@c len, see @ref LoanableCollection::length())
#     *
#     * - the maximum length (@c max_len, see @ref LoanableCollection::maximum())
#     *
#     * - whether the collection container owns the memory of the elements within
#     *   (@c owns, see @ref LoanableCollection::has_ownership())
#     *
#     * The initial (input) values of the @c len, @c max_len, and @c owns properties for the @c data_values and
#     * @c sample_infos collections govern the behavior of the read operation as specified by the following rules:
#     *
#     * 1. The values of @c len, @c max_len, and @c owns for the two collections must be identical. Otherwise read
#     *    will fail with RETCODE_PRECONDITION_NOT_MET.
#     *
#     * 2. On successful output, the values of @c len, @c max_len, and @c owns will be the same for both collections.
#     *
#     * 3. If the input <tt> max_len == 0 </tt>, then the @c data_values and @c sample_infos collections will be
#     *    filled with elements that are 'loaned' by the DataReader. On output, @c owns will be @c false, @c len will
#     *    be set to the number of values returned, and @c max_len will be set to a value
#     *    verifying <tt> max_len >= len </tt>. The use of this variant allows for zero-copy access to the data and the
#     *    application will need to return the loan to the DataReader using the @ref return_loan operation.
#     *
#     * 4. If the input <tt> max_len > 0 </tt> and the input <tt> owns == false </tt>, then the read operation will
#     *    fail with RETCODE_PRECONDITION_NOT_MET. This avoids the potential hard-to-detect memory leaks caused by an
#     *    application forgetting to return the loan.
#     *
#     * 5. If input <tt> max_len > 0 </tt> and the input <tt> owns == true </tt>, then the read operation will copy
#     *    the Data values and SampleInfo values into the elements already inside the collections. On output, @c owns
#     *    will be @c true, @c len will be set to the number of values copied, and @c max_len will remain unchanged.
#     *    The use of this variant forces a copy but the application can control where the copy is placed and the
#     *    application will not need to return the loan. The number of samples copied depends on the values of
#     *    @c max_len and @c max_samples:
#     *
#     *    - If <tt> max_samples == LENGTH_UNLIMITED </tt>, then at most @c max_len values will be copied. The use of
#     *      this variant lets the application limit the number of samples returned to what the sequence can
#     *      accommodate.
#     *
#     *    - If <tt> max_samples <= max_len </tt>, then at most @c max_samples values will be copied. The use of this
#     *      variant lets the application limit the number of samples returned to fewer that what the sequence can
#     *      accommodate.
#     *
#     *    - If <tt> max_samples > max_len </tt>, then the read operation will fail with RETCODE_PRECONDITION_NOT_MET.
#     *      This avoids the potential confusion where the application expects to be able to access up to
#     *      @c max_samples, but that number can never be returned, even if they are available in the DataReader,
#     *      because the output sequence cannot accommodate them.
#     *
#     * As described above, upon return the @c data_values and @c sample_infos collections may contain elements
#     * 'loaned' from the DataReader. If this is the case, the application will need to use the @ref return_loan
#     * operation to return the loan once it is no longer using the Data in the collection. Upon return from
#     * @ref return_loan, the collection will have <tt> max_len == 0 </tt> and <tt> owns == false </tt>.
#     *
#     * The application can determine whether it is necessary to return the loan or not based on the state of the
#     * collections when the read operation was called, or by accessing the @c owns property. However, in many cases
#     * it may be simpler to always call @ref return_loan, as this operation is harmless (i.e., leaves all elements
#     * unchanged) if the collection does not have a loan.
#     *
#     * On output, the collection of Data values and the collection of SampleInfo structures are of the same length
#     * and are in a one-to-one correspondence. Each SampleInfo provides information, such as the @c source_timestamp,
#     * the @c sample_state, @c view_state, and @c instance_state, etc., about the corresponding sample.
#     *
#     * Some elements in the returned collection may not have valid data. If the @c instance_state in the SampleInfo is
#     * @ref NOT_ALIVE_DISPOSED_INSTANCE_STATE or @ref NOT_ALIVE_NO_WRITERS_INSTANCE_STATE, then the last sample for
#     * that instance in the collection, that is, the one whose SampleInfo has <tt> sample_rank == 0 </tt> does not
#     * contain valid data. Samples that contain no data do not count towards the limits imposed by the
#     * @ref ResourceLimitsQosPolicy.
#     *
#     * The act of reading a sample changes its @c sample_state to @ref READ_SAMPLE_STATE. If the sample belongs
#     * to the most recent generation of the instance, it will also set the @c view_state of the instance to be
#     * @ref NOT_NEW_VIEW_STATE. It will not affect the @c instance_state of the instance.
#     *
#     * If the DataReader has no samples that meet the constraints, the operations fails with RETCODE_NO_DATA.
#     *
#     * @em Important: If the samples "returned" by this method are loaned from the middleware (see @ref take
#     * for more information on memory loaning), it is important that their contents not be changed. Because the
#     * memory in which the data is stored belongs to the middleware, any modifications made to the data will be
#     * seen the next time the same samples are read or taken; the samples will no longer reflect the state that
#     * was received from the network.
#     *
#     * @param [in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param [in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param [in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                 @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                 available, up to the limits described above.
#     * @param [in]     sample_states   Only data samples with @c sample_state matching one of these will be returned.
#     * @param [in]     view_states     Only data samples with @c view_state matching one of these will be returned.
#     * @param [in]     instance_states Only data samples with @c instance_state matching one of these will be returned.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t read(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            SampleStateMask sample_states = ANY_SAMPLE_STATE,
#            ViewStateMask view_states = ANY_VIEW_STATE,
#            InstanceStateMask instance_states = ANY_INSTANCE_STATE);
#
#    /**
#     * NOT YET IMPLEMENTED
#     *
#     * This operation accesses via ‘read’ the samples that match the criteria specified in the ReadCondition.
#     * This operation is especially useful in combination with QueryCondition to filter data samples based on the
#     * content.
#     *
#     * The specified ReadCondition must be attached to the DataReader; otherwise the operation will fail and return
#     * RETCODE_PRECONDITION_NOT_MET.
#     *
#     * In case the ReadCondition is a ‘plain’ ReadCondition and not the specialized QueryCondition, the
#     * operation is equivalent to calling read and passing as @c sample_states, @c view_states and @c instance_states
#     * the value of the corresponding attributes in @c a_condition. Using this operation the application can avoid
#     * repeating the same parameters specified when creating the ReadCondition.
#     *
#     * The samples are accessed with the same semantics as the read operation. If the DataReader has no samples that
#     * meet the constraints, the return value will be RETCODE_NO_DATA.
#     *
#     * @param[in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param[in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param[in]     max_samples     The maximum number of samples to be returned.
#     * @param[in]     a_condition     A ReadCondition that returned @c sample_states must pass
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t read_w_condition(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            ReadCondition* a_condition = nullptr);
#
#    /**
#     * Access a collection of data samples from the DataReader.
#     *
#     * This operation accesses a collection of data values from the DataReader. The behavior is identical to
#     * @ref read, except that all samples returned belong to the single specified instance whose handle is
#     * @c a_handle.
#     *
#     * Upon successful completion, the data collection will contain samples all belonging to the same instance.
#     * The corresponding @ref SampleInfo verifies @ref SampleInfo::instance_handle == @c a_handle.
#     *
#     * This operation is semantically equivalent to the @ref read operation, except in building the collection.
#     * The DataReader will check that the sample belongs to the specified instance and otherwise it will not place
#     * the sample in the returned collection.
#     *
#     * The behavior of this operation follows the same rules as the @ref read operation regarding the pre-conditions and
#     * post-conditions for the @c data_values and @c sample_infos. Similar to @ref read, this operation may 'loan'
#     * elements to the output collections, which must then be returned by means of @ref return_loan.
#     *
#     * If the DataReader has no samples that meet the constraints, the operations fails with RETCODE_NO_DATA.
#     *
#     * @param [in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param [in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param [in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                 @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                 available, up to the limits described in the documentation for @ref read().
#     * @param [in]     a_handle        The specified instance to return samples for. The method will fail with
#     *                                 RETCODE_BAD_PARAMETER if the handle does not correspond to an existing
#     *                                 data-object known to the DataReader.
#     * @param [in]     sample_states   Only data samples with @c sample_state matching one of these will be returned.
#     * @param [in]     view_states     Only data samples with @c view_state matching one of these will be returned.
#     * @param [in]     instance_states Only data samples with @c instance_state matching one of these will be returned.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t read_instance(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            const InstanceHandle_t& a_handle = HANDLE_NIL,
#            SampleStateMask sample_states = ANY_SAMPLE_STATE,
#            ViewStateMask view_states = ANY_VIEW_STATE,
#            InstanceStateMask instance_states = ANY_INSTANCE_STATE);
#
#    /**
#     * Access a collection of data samples from the DataReader.
#     *
#     * This operation accesses a collection of data values from the DataReader where all the samples belong to a
#     * single instance. The behavior is similar to @ref read_instance, except that the actual instance is not
#     * directly specified. Rather, the samples will all belong to the 'next' instance with @c instance_handle
#     * 'greater' than the specified 'previous_handle' that has available samples.
#     *
#     * This operation implies the existence of a total order 'greater-than' relationship between the instance
#     * handles. The specifics of this relationship are not all important and are implementation specific. The
#     * important thing is that, according to the middleware, all instances are ordered relative to each other.
#     * This ordering is between the instance handles, and should not depend on the state of the instance (e.g.
#     * whether it has data or not) and must be defined even for instance handles that do not correspond to instances
#     * currently managed by the DataReader. For the purposes of the ordering, it should be 'as if' each instance
#     * handle was represented as an integer.
#     *
#     * The behavior of this operation is 'as if' the DataReader invoked @ref read_instance, passing the smallest
#     * @c instance_handle among all the ones that: (a) are greater than @c previous_handle, and (b) have available
#     * samples (i.e. samples that meet the constraints imposed by the specified states).
#     *
#     * The special value @ref HANDLE_NIL is guaranteed to be 'less than' any valid @c instance_handle. So the use
#     * of the parameter value @c previous_handle == @ref HANDLE_NIL will return the samples for the instance which
#     * has the smallest @c instance_handle among all the instances that contain available samples.
#     *
#     * This operation is intended to be used in an application-driven iteration, where the application starts by
#     * passing @c previous_handle == @ref HANDLE_NIL, examines the samples returned, and then uses the
#     * @c instance_handle returned in the @ref SampleInfo as the value of the @c previous_handle argument to the
#     * next call to @ref read_next_instance. The iteration continues until @ref read_next_instance fails with
#     * RETCODE_NO_DATA.
#     *
#     * Note that it is possible to call the @ref read_next_instance operation with a @c previous_handle that does not
#     * correspond to an instance currently managed by the DataReader. This is because as stated earlier the
#     * 'greater-than' relationship is defined even for handles not managed by the DataReader. One practical situation
#     * where this may occur is when an application is iterating through all the instances, takes all the samples of a
#     * @ref NOT_ALIVE_NO_WRITERS_INSTANCE_STATE instance, returns the loan (at which point the instance information
#     * may be removed, and thus the handle becomes invalid), and tries to read the next instance.
#     *
#     * The behavior of this operation follows the same rules as the @ref read operation regarding the pre-conditions and
#     * post-conditions for the @c data_values and @c sample_infos. Similar to @ref read, this operation may 'loan'
#     * elements to the output collections, which must then be returned by means of @ref return_loan.
#     *
#     * If the DataReader has no samples that meet the constraints, the operations fails with RETCODE_NO_DATA.
#     *
#     * @param [in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param [in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param [in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                 @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                 available, up to the limits described in the documentation for @ref read().
#     * @param [in]     previous_handle The 'next smallest' instance with a value greater than this value that has
#     *                                 available samples will be returned.
#     * @param [in]     sample_states   Only data samples with @c sample_state matching one of these will be returned.
#     * @param [in]     view_states     Only data samples with @c view_state matching one of these will be returned.
#     * @param [in]     instance_states Only data samples with @c instance_state matching one of these will be returned.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t read_next_instance(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            const InstanceHandle_t& previous_handle = HANDLE_NIL,
#            SampleStateMask sample_states = ANY_SAMPLE_STATE,
#            ViewStateMask view_states = ANY_VIEW_STATE,
#            InstanceStateMask instance_states = ANY_INSTANCE_STATE);
#
#    /**
#     * NOT YET IMPLEMENTED
#     *
#     * This operation accesses a collection of Data values from the DataReader. The behavior is identical to
#     * @ref read_next_instance except that all samples returned satisfy the specified condition. In other words, on
#     * success all returned samples belong to the same instance, and the instance is the instance with
#     * ‘smallest’ @c instance_handle among the ones that verify (a) @c instance_handle >= @c previous_handle and (b) have samples
#     * for which the specified ReadCondition evaluates to TRUE.
#     *
#     * Similar to the operation @ref read_next_instance it is possible to call
#     * @ref read_next_instance_w_condition with a @c previous_handle that does not correspond to an instance currently
#     * managed by the DataReader.
#     *
#     * The behavior of the @ref read_next_instance_w_condition operation follows the same rules than the read operation
#     * regarding the pre-conditions and post-conditions for the @c data_values and @c sample_infos collections. Similar
#     * to read, the @ref read_next_instance_w_condition operation may ‘loan’ elements to the output collections which
#     * must then be returned by means of @ref return_loan.
#     *
#     * If the DataReader has no samples that meet the constraints, the return value will be RETCODE_NO_DATA.
#     *
#     * @param[in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param[in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param[in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                available, up to the limits described in the documentation for @ref read().
#     * @param[in]     previous_handle The 'next smallest' instance with a value greater than this value that has
#     *                                available samples will be returned.
#     * @param[in]     a_condition     A ReadCondition that returned @c sample_states must pass
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t read_next_instance_w_condition(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            const InstanceHandle_t& previous_handle = HANDLE_NIL,
#            ReadCondition* a_condition = nullptr);
#
#    /**
#     * Access a collection of data samples from the DataReader.
#     *
#     * This operation accesses a collection of data-samples from the DataReader and a corresponding collection of
#     * SampleInfo structures, and 'removes' them from the DataReader. The operation will return either a 'list' of
#     * samples or else a single sample. This is controlled by the @ref PresentationQosPolicy using the same logic
#     * as for the @ref read operation.
#     *
#     * The act of taking a sample removes it from the DataReader so it cannot be 'read' or 'taken' again. If the
#     * sample belongs to the most recent generation of the instance, it will also set the @c view_state of the
#     * instance to NOT_NEW. It will not affect the @c instance_state of the instance.
#     *
#     * The behavior of the take operation follows the same rules than the @ref read operation regarding the
#     * pre-conditions and post-conditions for the @c data_values and @c sample_infos collections. Similar to
#     * @ref read, the take operation may 'loan' elements to the output collections which must then be returned by
#     * means of @ref return_loan. The only difference with @ref read is that, as stated, the samples returned by
#     * take will no longer be accessible to successive calls to read or take.
#     *
#     * If the DataReader has no samples that meet the constraints, the operations fails with RETCODE_NO_DATA.
#     *
#     * @param [in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param [in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param [in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                 @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                 available, up to the limits described in the documentation for @ref read().
#     * @param [in]     sample_states   Only data samples with @c sample_state matching one of these will be returned.
#     * @param [in]     view_states     Only data samples with @c view_state matching one of these will be returned.
#     * @param [in]     instance_states Only data samples with @c instance_state matching one of these will be returned.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t take(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            SampleStateMask sample_states = ANY_SAMPLE_STATE,
#            ViewStateMask view_states = ANY_VIEW_STATE,
#            InstanceStateMask instance_states = ANY_INSTANCE_STATE);
#
#    /**
#     * NOT YET IMPLEMENTED
#     *
#     * This operation is analogous to @ref read_w_condition except it accesses samples via the ‘take’ operation.
#     *
#     * The specified ReadCondition must be attached to the DataReader; otherwise the operation will fail and return
#     * RETCODE_PRECONDITION_NOT_MET.
#     *
#     * The samples are accessed with the same semantics as the @ref take operation.
#     *
#     * This operation is especially useful in combination with QueryCondition to filter data samples based on the
#     * content.
#     *
#     * If the DataReader has no samples that meet the constraints, the return value will be RETCODE_NO_DATA.
#     *
#     * @param[in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param[in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param[in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are.
#     * @param[in]     a_condition     A ReadCondition that returned @c sample_states must pass
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t take_w_condition(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            ReadCondition* a_condition = nullptr);
#
#    /**
#     * Access a collection of data samples from the DataReader.
#     *
#     * This operation accesses a collection of data values from the DataReader and 'removes' them from the DataReader.
#     *
#     * This operation has the same behavior as @ref read_instance, except that the samples are 'taken' from the
#     * DataReader such that they are no longer accessible via subsequent 'read' or 'take' operations.
#     *
#     * The behavior of this operation follows the same rules as the @ref read operation regarding the pre-conditions and
#     * post-conditions for the @c data_values and @c sample_infos. Similar to @ref read, this operation may 'loan'
#     * elements to the output collections, which must then be returned by means of @ref return_loan.
#     *
#     * If the DataReader has no samples that meet the constraints, the operations fails with RETCODE_NO_DATA.
#     *
#     * @param[in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param[in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param[in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                available, up to the limits described in the documentation for @ref read().
#     * @param[in]     a_handle        The specified instance to return samples for. The method will fail with
#     *                                RETCODE_BAD_PARAMETER if the handle does not correspond to an existing
#     *                                data-object known to the DataReader.
#     * @param[in]     sample_states   Only data samples with @c sample_state matching one of these will be returned.
#     * @param[in]     view_states     Only data samples with @c view_state matching one of these will be returned.
#     * @param[in]     instance_states Only data samples with @c instance_state matching one of these will be returned.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t take_instance(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            const InstanceHandle_t& a_handle = HANDLE_NIL,
#            SampleStateMask sample_states = ANY_SAMPLE_STATE,
#            ViewStateMask view_states = ANY_VIEW_STATE,
#            InstanceStateMask instance_states = ANY_INSTANCE_STATE);
#
#    /**
#     * Access a collection of data samples from the DataReader.
#     *
#     * This operation accesses a collection of data values from the DataReader and 'removes' them from the DataReader.
#     *
#     * This operation has the same behavior as @ref read_next_instance, except that the samples are 'taken' from the
#     * DataReader such that they are no longer accessible via subsequent 'read' or 'take' operations.
#     *
#     * Similar to the operation @ref read_next_instance, it is possible to call this operation with a
#     * @c previous_handle that does not correspond to an instance currently managed by the DataReader.
#     *
#     * The behavior of this operation follows the same rules as the @ref read operation regarding the pre-conditions and
#     * post-conditions for the @c data_values and @c sample_infos. Similar to @ref read, this operation may 'loan'
#     * elements to the output collections, which must then be returned by means of @ref return_loan.
#     *
#     * If the DataReader has no samples that meet the constraints, the operations fails with RETCODE_NO_DATA.
#     *
#     * @param[in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param[in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param[in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                available, up to the limits described in the documentation for @ref read().
#     * @param[in]     previous_handle The 'next smallest' instance with a value greater than this value that has
#     *                                available samples will be returned.
#     * @param[in]     sample_states   Only data samples with @c sample_state matching one of these will be returned.
#     * @param[in]     view_states     Only data samples with @c view_state matching one of these will be returned.
#     * @param[in]     instance_states Only data samples with @c instance_state matching one of these will be returned.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t take_next_instance(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            const InstanceHandle_t& previous_handle = HANDLE_NIL,
#            SampleStateMask sample_states = ANY_SAMPLE_STATE,
#            ViewStateMask view_states = ANY_VIEW_STATE,
#            InstanceStateMask instance_states = ANY_INSTANCE_STATE);
#
#    /**
#     * NOT YET IMPLEMENTED
#     *
#     * This operation accesses a collection of Data values from the DataReader. The behavior is identical to
#     * @ref read_next_instance except that all samples returned satisfy the specified condition. In other words, on
#     * success all returned samples belong to the same instance, and the instance is the instance with ‘smallest’
#     * @c instance_handle among the ones that verify (a) @c instance_handle >= @c previous_handle and (b) have
#     * samples for which the specified ReadCondition evaluates to TRUE.
#     *
#     * Similar to the operation @ref read_next_instance it is possible to call @ref read_next_instance_w_condition with
#     * a @c previous_handle that does not correspond to an instance currently managed by the DataReader.
#     *
#     * The behavior of the @ref read_next_instance_w_condition operation follows the same rules than the read operation
#     * regarding the pre-conditions and post-conditions for the @c data_values and @c sample_infos collections. Similar
#     * to read, the @ref read_next_instance_w_condition operation may ‘loan’ elements to the output collections which
#     * must then be returned by means of @ref return_loan.
#     *
#     * If the DataReader has no samples that meet the constraints, the return value will be RETCODE_NO_DATA
#     *
#     * @param[in,out] data_values     A LoanableCollection object where the received data samples will be returned.
#     * @param[in,out] sample_infos    A SampleInfoSeq object where the received sample info will be returned.
#     * @param[in]     max_samples     The maximum number of samples to be returned. If the special value
#     *                                @ref LENGTH_UNLIMITED is provided, as many samples will be returned as are
#     *                                available, up to the limits described in the documentation for @ref read().
#     * @param[in]     previous_handle The 'next smallest' instance with a value greater than this value that has
#     *                                available samples will be returned.
#     * @param[in]     a_condition     A ReadCondition that returned @c sample_states must pass
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t take_next_instance_w_condition(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos,
#            int32_t max_samples = LENGTH_UNLIMITED,
#            const InstanceHandle_t& previous_handle = HANDLE_NIL,
#            ReadCondition* a_condition = nullptr);
#
#
#    ///@}
#
#    /**
#     * This operation indicates to the DataReader that the application is done accessing the collection of
#     * @c data_values and @c sample_infos obtained by some earlier invocation of @ref read or @ref take on the
#     * DataReader.
#     *
#     * The @c data_values and @c sample_infos must belong to a single related ‘pair’; that is, they should correspond
#     * to a pair returned from a single call to read or take. The @c data_values and @c sample_infos must also have
#     * been obtained from the same DataReader to which they are returned. If either of these conditions is not met,
#     * the operation will fail and return RETCODE_PRECONDITION_NOT_MET.
#     *
#     * This operation allows implementations of the @ref read and @ref take operations to "loan" buffers from the
#     * DataReader to the application and in this manner provide "zero-copy" access to the data. During the loan, the
#     * DataReader will guarantee that the data and sample-information are not modified.
#     *
#     * It is not necessary for an application to return the loans immediately after the read or take calls. However,
#     * as these buffers correspond to internal resources inside the DataReader, the application should not retain them
#     * indefinitely.
#     *
#     * The use of the @ref return_loan operation is only necessary if the read or take calls "loaned" buffers to the
#     * application. This only occurs if the @c data_values and @c sample_infos collections had <tt> max_len == 0 </tt>
#     * at the time read or take was called. The application may also examine the @c owns property of the collection to
#     * determine if there is an outstanding loan. However, calling @ref return_loan on a collection that does not have
#     * a loan is safe and has no side effects.
#     *
#     * If the collections had a loan, upon return from return_loan the collections will have <tt> max_len == 0 </tt>.
#     *
#     * @param [in,out] data_values   A LoanableCollection object where the received data samples were obtained from
#     *                               an earlier invocation of read or take on this DataReader.
#     * @param [in,out] sample_infos  A SampleInfoSeq object where the received sample infos were obtained from
#     *                               an earlier invocation of read or take on this DataReader.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t return_loan(
#            LoanableCollection& data_values,
#            SampleInfoSeq& sample_infos);
#
#    /**
#     * This operation deletes all the entities that were created by means of the “create” operations on the DataReader.
#     * That is, it deletes all contained ReadCondition and QueryCondition objects.
#     *
#     * The operation will return PRECONDITION_NOT_MET if the any of the contained entities is in a state where it cannot
#     * be deleted.
#     *
#     * @return Any of the standard return codes.
#     */
#    RTPS_DllAPI ReturnCode_t delete_contained_entities();
