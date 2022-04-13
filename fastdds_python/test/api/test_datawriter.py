import datetime

import fastdds
import pytest
import test_complete


class DataWriterListener (fastdds.DataWriterListener):
    def __init__(self):
        super().__init__()


@pytest.fixture
def participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)


@pytest.fixture
def publisher(participant):
    return participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)


@pytest.fixture
def test_type():
    return fastdds.TypeSupport(
            test_complete.CompleteTestTypePubSubType())


@pytest.fixture
def test_keyed_type(test_type):
    test_type.set(test_complete.KeyedCompleteTestTypePubSubType())


@pytest.fixture
def topic(participant, test_type):
    participant.register_type(test_type, test_type.get_type_name())
    return participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def datawriter_qos():
    return fastdds.DataWriterQos()


@pytest.fixture
def manual_liveliness_datawriter_qos(datawriter_qos):
    datawriter_qos.liveliness().kind = \
        fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
    return datawriter_qos


@pytest.fixture
def keep_all_datawriter_qos(datawriter_qos):
    datawriter_qos.history().kind = \
        fastdds.KEEP_ALL_HISTORY_QOS
    return datawriter_qos


@pytest.fixture
def datawriter(participant, topic, publisher, datawriter_qos):
    datawriter = publisher.create_datawriter(topic, datawriter_qos)

    yield datawriter

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_assert_liveliness(manual_liveliness_datawriter_qos, datawriter):
    """
    This test checks:
    - DataWriter::assert_liveliness
    """
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.assert_liveliness())


def test_clear_history(keep_all_datawriter_qos, datawriter):
    """
    This test checks:
    - DataWriter::clear_history
    """
    sample = test_complete.CompleteTestType()
    sample.int16_field(4)
    assert(datawriter.write(sample))
    assert([fastdds.ReturnCode_t.RETCODE_OK, 1] ==
           datawriter.clear_history())


def test_dispose(test_keyed_type, datawriter):
    """
    This test checks:
    - DataWriter::dispose
    - DataWriter::dispose_w_timestamp
    - DataWriter::unregister_instance
    """
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


def test_get_instance_handle(datawriter):
    """
    This test checks:
    - DataWriter::guid
    - DataWriter::get_instance_handle
    """
    guid = datawriter.guid()
    assert(fastdds.c_Guid_Unknown != guid)
    ih = datawriter.get_instance_handle()
    assert(fastdds.c_InstanceHandle_Unknown != ih)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])

    for i in range(0, 4):
        assert(guid.entityId.value[i] == ih.value[12+i])


def test_get_key_value(test_keyed_type, datawriter):
    """
    This test checks:
    - DataWriter::get_key_value
    """
    sample = test_complete.KeyedCompleteTestType()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.get_key_value(sample, ih))
    assert(fastdds.c_InstanceHandle_Unknown == ih)


def test_get_sending_locators(datawriter):
    """
    This test checks:
    - DataWriter::get_sending_locators
    """
    locator_list = fastdds.LocatorList()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_sending_locators(locator_list))
    assert(0 < locator_list.size())


def test_get_set_listener(datawriter):
    """
    This test checks:
    - DataWriter::get_listener
    - DataWriter::set_listener
    - DataWriter::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    # Overload 1
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(listener))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    datawriter.set_listener(None)

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
        datawriter.set_listener(None)
        listener = DataWriterListener()
        assert(listener is not None)
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               datawriter.set_listener(listener, status_mask_2))
        assert(datawriter.get_listener() == listener)
        assert(status_mask_2 == datawriter.get_status_mask())
        datawriter.set_listener(None)

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


def test_get_liveliness_lost_status(datawriter):
    """
    This test checks:
    - DataWriter::get_liveliness_lost_status
    """
    status = fastdds.LivelinessLostStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_liveliness_lost_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)


def test_get_matched_subscription_data(datawriter):
    """
    This test checks:
    - DataWriter::get_matched_subscription_data
    """
    sub_data = fastdds.SubscriptionBuiltinTopicData()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.get_matched_subscription_data(sub_data, ih))


def test_get_matched_subscriptions(datawriter):
    """
    This test checks:
    - DataWriter::get_matched_subscriptions
    """
    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datawriter.get_matched_subscriptions(ihs))


def test_get_offered_deadline_missed_status(datawriter):
    """
    This test checks:
    - DataWriter::get_offered_deadline_missed_status
    """
    status = fastdds.OfferedDeadlineMissedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_offered_deadline_missed_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_instance_handle)


def test_get_offered_incompatible_qos_status(datawriter):
    """
    This test checks:
    - DataWriter::get_offered_deadline_missed_status
    """
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


def test_get_publication_matched_status(datawriter):
    """
    This test checks:
    - DataWriter::get_publication_matched_status
    """
    status = fastdds.PublicationMatchedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.get_publication_matched_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(0 == status.current_count)
    assert(0 == status.current_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_subscription_handle)


def test_get_publisher(publisher, datawriter):
    """
    This test checks:
    - DataWriter::get_publisher
    """
    pub = datawriter.get_publisher()
    assert(pub == publisher)


def test_get_type(test_type, datawriter):
    """
    This test checks:
    - DataWriter::get_type
    """
    test_type_aux = datawriter.get_type()
    assert(test_type == test_type_aux)
    assert(test_type.get_type_name() == test_type_aux.get_type_name())


def test_get_topic(topic, datawriter):
    """
    This test checks:
    - DataWriter::get_topic
    """
    topic_aux = datawriter.get_topic()
    assert(topic == topic_aux)
    assert(topic.get_type_name() == topic_aux.get_type_name())


def test_lookup_instance(test_keyed_type, datawriter):
    """
    This test checks:
    - DataWriter::lookup_instance
    """
    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    ih = datawriter.lookup_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown == ih)


def test_register_instance(test_keyed_type, datawriter):
    """
    This test checks:
    - DataWriter::register_instance
    - DataWriter::register_instance_w_timestamp
    - DataWriter::unregister_instance
    - DataWriter::unregister_instance_w_timestamp
    """
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


def test_wait_for_acknowledgments(test_keyed_type, datawriter):
    """
    This test checks:
    - DataWriter::wait_for_acknowledgments
    """
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


def test_write(test_keyed_type, datawriter):
    """
    This test checks:
    - DataWriter::write
    - DataWriter::write_w_timestamp
    """
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
