# until https://bugs.python.org/issue46276 is not fixed we can apply this
# workaround on windows
import os
if os.name == 'nt':
    import win32api
    win32api.LoadLibrary('test_complete')

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
    - DataReader::read
    - DataReader::return_loan
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

    data_seq = test_complete.CompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA == datareader.read(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK == datareader.read(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.int16_field() == data_seq[0].int16_field())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))

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


def test_read_instance():
    """
    This test checks:
    - DataReader::read_instance
    - DataReader::return_loan
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

    data_seq = test_complete.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_BAD_PARAMETER ==
           datareader.read_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.KeyedCompleteTestType()
    sample.int16_field(255)
    ih = datawriter.register_instance(sample)
    assert(datawriter.write(sample, ih))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK == datareader.read_instance(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.int16_field() == data_seq[0].int16_field())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))

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


def test_read_next_instance():
    """
    This test checks:
    - DataReader::read_next_instance
    - DataReader::return_loan
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

    data_seq = test_complete.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.read_next_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.KeyedCompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK == datareader.read_next_instance(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.int16_field() == data_seq[0].int16_field())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))

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


def test_take():
    """
    This test checks:
    - DataReader::take
    - DataReader::return_loan
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

    data_seq = test_complete.CompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA == datareader.take(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK == datareader.take(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.int16_field() == data_seq[0].int16_field())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))

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


def test_take_instance():
    """
    This test checks:
    - DataReader::take_instance
    - DataReader::return_loan
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

    data_seq = test_complete.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_BAD_PARAMETER ==
           datareader.take_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.KeyedCompleteTestType()
    sample.int16_field(255)
    ih = datawriter.register_instance(sample)
    assert(datawriter.write(sample, ih))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK == datareader.take_instance(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.int16_field() == data_seq[0].int16_field())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))

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


def test_take_next_instance():
    """
    This test checks:
    - DataReader::take_next_instance
    - DataReader::return_loan
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

    data_seq = test_complete.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.take_next_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)
    sample = test_complete.KeyedCompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK == datareader.take_next_instance(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.int16_field() == data_seq[0].int16_field())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))

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
