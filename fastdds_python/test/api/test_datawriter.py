from audioop import ratecv
import datetime

import fastdds
import test_complete


class DataWriterListener (fastdds.DataWriterListener):
    def __init__(self):
        super().__init__()


def test_assert_liveliness():
    """
    This test checks:
    - DataWriter::assert_liveliness
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter_qos = fastdds.DataWriterQos()
    datawriter_qos.liveliness().kind = \
        fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
    datawriter = publisher.create_datawriter(topic, datawriter_qos)
    assert(datawriter is not None)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.assert_liveliness())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_clear_history():
    """
    This test checks:
    - DataWriter::clear_history
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter_qos = fastdds.DataWriterQos()
    datawriter_qos.history().kind = \
        fastdds.KEEP_ALL_HISTORY_QOS
    datawriter = publisher.create_datawriter(topic, datawriter_qos)
    assert(datawriter is not None)

    sample = test_complete.KeyedCompleteTestType()
    sample.id(4)
    assert(datawriter.write(sample))
    assert([fastdds.ReturnCode_t.RETCODE_OK, 1] ==
           datawriter.clear_history())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_dispose():
    """
    This test checks:
    - DataWriter::dispose
    - DataWriter::dispose_w_timestamp
    - DataWriter::unregister_instance
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    # Overload 1
    sample = test_complete.KeyedCompleteTestType()
    sample.id(1)
    ih = datawriter.register_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown != ih)
    sample2 = test_complete.KeyedCompleteTestType()
    sample2.id(2)
    ih2 = datawriter.register_instance(sample2)
    assert(fastdds.c_InstanceHandle_Unknown != ih2)
    assert(ih2 != ih)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.dispose(sample, ih))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.dispose(sample2, ih2))

    # Overload 2
    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    now = datetime.datetime.now().time()
    timestamp = fastdds.Time_t()
    timestamp.seconds = now.second
    ih = datawriter.register_instance_w_timestamp(sample, timestamp)
    assert(fastdds.c_InstanceHandle_Unknown == ih)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.dispose_w_timestamp(sample, ih, timestamp))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_instance_handle():
    """
    This test checks:
    - DataWriter::guid
    - DataWriter::get_instance_handle
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)

    guid = datawriter.guid()
    assert(fastdds.c_Guid_Unknown != guid)
    ih = datawriter.get_instance_handle()
    assert(fastdds.c_InstanceHandle_Unknown != ih)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])

    for i in range(0, 4):
        assert(guid.entityId.value[i] == ih.value[12+i])

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_key_value():
    """
    This test checks:
    - DataWriter::get_key_value
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    sample = test_complete.KeyedCompleteTestType()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.get_key_value(sample, ih))
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_sending_locators():
    """
    This test checks:
    - DataWriter::get_sending_locators
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    locator_list = fastdds.LocatorList()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_sending_locators(locator_list))
    assert(0 < locator_list.size())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_listener():
    """
    This test checks:
    - DataWriter::get_listener
    - DataWriter::set_listener
    - DataWriter::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    # Overload 1
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(listener))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())

    def test(status_mask_1, status_mask_2):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        listener = DataWriterListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
              datawriter.set_listener(listener, status_mask_1))
        assert(datawriter.get_listener() == listener)
        assert(status_mask_1 == datawriter.get_status_mask())
        listener = DataWriterListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               datawriter.set_listener(listener, status_mask_2))
        assert(datawriter.get_listener() == listener)
        assert(status_mask_2 == datawriter.get_status_mask())

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
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_liveliness_lost_status():
    """
    This test checks:
    - DataWriter::get_liveliness_lost_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    status = fastdds.LivelinessLostStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_liveliness_lost_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_matched_subscription_data():
    """
    This test checks:
    - DataWriter::get_matched_subscription_data
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    sub_data = fastdds.SubscriptionBuiltinTopicData()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.get_matched_subscription_data(sub_data, ih))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_matched_subscriptions():
    """
    This test checks:
    - DataWriter::get_matched_subscriptions
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.get_matched_subscriptions(ihs))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_offered_deadline_missed_status():
    """
    This test checks:
    - DataWriter::get_offered_deadline_missed_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    status = fastdds.OfferedDeadlineMissedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_offered_deadline_missed_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_instance_handle)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_offered_incompatible_qos_status():
    """
    This test checks:
    - DataWriter::get_offered_deadline_missed_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    status = fastdds.OfferedIncompatibleQosStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_offered_incompatible_qos_status(status))
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
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_publication_matched_status():
    """
    This test checks:
    - DataWriter::get_publication_matched_status
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    status = fastdds.PublicationMatchedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_publication_matched_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(0 == status.current_count)
    assert(0 == status.current_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_subscription_handle)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_publisher():
    """
    This test checks:
    - DataWriter::get_publisher
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    pub = datawriter.get_publisher()
    assert(pub == publisher)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_type():
    """
    This test checks:
    - DataWriter::get_type
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    test_type_aux = datawriter.get_type()
    assert(test_type == test_type_aux)
    assert(test_type.get_type_name() == test_type_aux.get_type_name())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_topic():
    """
    This test checks:
    - DataWriter::get_topic
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    topic_aux = datawriter.get_topic()
    assert(topic == topic_aux)
    assert(topic.get_type_name() == topic_aux.get_type_name())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_lookup_instance():
    """
    This test checks:
    - DataWriter::lookup_instance
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    ih = datawriter.lookup_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_register_instance():
    """
    This test checks:
    - DataWriter::register_instance
    - DataWriter::register_instance_w_timestamp
    - DataWriter::unregister_instance
    - DataWriter::unregister_instance_w_timestamp
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    # Overload 1
    sample = test_complete.KeyedCompleteTestType()
    sample.id(1)
    ih = datawriter.register_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown != ih)
    sample2 = test_complete.KeyedCompleteTestType()
    sample2.id(2)
    ih2 = datawriter.register_instance(sample2)
    assert(fastdds.c_InstanceHandle_Unknown != ih2)
    assert(ih2 != ih)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.unregister_instance(sample, ih))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.unregister_instance(sample2, ih2))
    assert(fastdds.ReturnCode_t.RETCODE_PRECONDITION_NOT_MET ==
           datawriter.unregister_instance(
               sample, fastdds.c_InstanceHandle_Unknown))

    # Overload 2
    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    now = datetime.datetime.now().time()
    timestamp = fastdds.Time_t()
    timestamp.seconds = now.second
    ih = datawriter.register_instance_w_timestamp(sample, timestamp)
    assert(fastdds.c_InstanceHandle_Unknown == ih)
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.unregister_instance_w_timestamp(sample, ih, timestamp))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_wait_for_acknowledgments():
    """
    This test checks:
    - DataWriter::wait_for_acknowledgments
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    # Overload 1
    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    assert(datawriter.write(sample))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.wait_for_acknowledgments(fastdds.Duration_t(1, 0)))

    # Overload 2
    ih = datawriter.register_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown != ih)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.wait_for_acknowledgments(
               sample, ih, fastdds.Duration_t(1, 0)))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_write():
    """
    This test checks:
    - DataWriter::write
    - DataWriter::write_w_timestamp
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(
            test_complete.KeyedCompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    # Overload 1
    sample = test_complete.KeyedCompleteTestType()
    assert(datawriter.write(sample))

    # Overload 2
    sample = test_complete.KeyedCompleteTestType()
    params = fastdds.WriteParams()
    guid = fastdds.GUID_t()
    guid.guidPrefix.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    guid.entityId.value = (13, 14, 15, 16)
    sequence_number = fastdds.SequenceNumber_t()
    sequence_number.high = 0
    sequence_number.low = 1
    params.related_sample_identity().writer_guid(guid)
    params.related_sample_identity().sequence_number(sequence_number)
    assert(datawriter.write(sample, params))

    # Overload 3
    sample = test_complete.KeyedCompleteTestType()
    sample.id(1)
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.write(sample, ih))
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.ReturnCode_t.RETCODE_PRECONDITION_NOT_MET ==
           datawriter.write(sample, ih))

    # Overload 4
    sample = test_complete.KeyedCompleteTestType()
    sample.id(1)
    ih = fastdds.InstanceHandle_t()
    now = datetime.datetime.now().time()
    timestamp = fastdds.Time_t()
    timestamp.seconds = now.second
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.write_w_timestamp(sample, ih, timestamp))
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
