# until https://bugs.python.org/issue46276 is not fixed we can apply this
# workaround on windows
import os
if os.name == 'nt':
    import win32api
    win32api.LoadLibrary('test_complete')

import fastdds
import pytest
import test_complete
import time


class DataReaderListener (fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()


@pytest.fixture
def participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)


@pytest.fixture
def subscriber(participant):
    return participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)


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
def datareader_qos():
    return fastdds.DataReaderQos()


@pytest.fixture
def transient_datareader_qos(datareader_qos):
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    return datareader_qos


@pytest.fixture
def datareader(participant, topic, subscriber, datareader_qos):
    datareader = subscriber.create_datareader(topic, datareader_qos)

    yield datareader

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


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


@pytest.fixture
def datawriter(writer_participant, writer_topic, publisher):
    datawriter = publisher.create_datawriter(
            writer_topic, fastdds.DATAWRITER_QOS_DEFAULT)

    yield datawriter

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           writer_participant.delete_topic(writer_topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           writer_participant.delete_publisher(publisher))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(writer_participant))


def test_create_querycondition(datareader):
    """
    This test checks:
    - DataReader::create_querycondition
    - DataReader::delete_contained_entities
    """
    sv = fastdds.ANY_SAMPLE_STATE
    vv = fastdds.ANY_VIEW_STATE
    iv = fastdds.ANY_INSTANCE_STATE
    qp = fastdds.StringVector()

    querycondition = datareader.create_querycondition(
               sv, vv, iv, "", qp)
    assert(querycondition is None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.delete_contained_entities())


def test_create_readcondition(datareader):
    """
    This test checks:
    - DataReader::create_readcondition
    - DataReader::delete_readcondition
    """
    sv = fastdds.ANY_SAMPLE_STATE
    vv = fastdds.ANY_VIEW_STATE
    iv = fastdds.ANY_INSTANCE_STATE

    readcondition = datareader.create_readcondition(
               sv, vv, iv)
    assert(readcondition is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.delete_readcondition(readcondition))


def test_get_first_untaken(transient_datareader_qos, datareader,
                           datawriter):
    """
    This test checks:
    - DataReader::get_first_untaken_info
    """
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.get_first_untaken_info(info))
    qos = datareader.get_qos()
    assert(fastdds.TRANSIENT_LOCAL_DURABILITY_QOS == qos.durability().kind)
    qos = datawriter.get_qos()
    assert(fastdds.TRANSIENT_LOCAL_DURABILITY_QOS == qos.durability().kind)

    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_first_untaken_info(info))
    assert(info.valid_data)


def test_get_instance_handle(datareader):
    """
    This test checks:
    - DataReader::guid
    - DataReader::get_instance_handle
    """
    guid = datareader.guid()
    assert(fastdds.c_Guid_Unknown != guid)
    ih = datareader.get_instance_handle()
    assert(fastdds.c_InstanceHandle_Unknown != ih)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])

    for i in range(0, 4):
        assert(guid.entityId.value[i] == ih.value[12+i])


def test_get_key_value(test_keyed_type, datareader):
    """
    This test checks:
    - DataReader::get_key_value
    """
    sample = test_complete.KeyedCompleteTestType()
    sample.id(255)
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_key_value(sample, ih))
    assert(fastdds.c_InstanceHandle_Unknown == ih)


def test_get_set_listener(datareader):
    """
    This test checks:
    - DataReader::get_listener
    - DataReader::set_listener
    - DataReader::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    # Overload 1
    listener = DataReaderListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.set_listener(listener))
    assert(datareader.get_listener() == listener)
    assert(fastdds.StatusMask.all() ==
           datareader.get_status_mask())

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


def test_get_listening_locators(datareader):
    """
    This test checks:
    - DataReader::get_listening_locators
    """
    locator_list = fastdds.LocatorList()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_listening_locators(locator_list))
    assert(0 < locator_list.size())


def test_get_liveliness_changed_status(datareader):
    """
    This test checks:
    - DataReader::get_liveliness_changed_status
    """
    status = fastdds.LivelinessChangedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_liveliness_changed_status(status))
    assert(0 == status.alive_count)
    assert(0 == status.alive_count_change)
    assert(0 == status.not_alive_count)
    assert(0 == status.not_alive_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_publication_handle)


def test_get_matched_publication_data(datareader):
    """
    This test checks:
    - DataWriter::get_matched_publication_data
    """
    pub_data = fastdds.PublicationBuiltinTopicData()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_matched_publication_data(pub_data, ih))


def test_get_matched_publications(datareader):
    """
    This test checks:
    - DataReader::get_matched_publications
    """
    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.get_matched_publications(ihs))


def test_get_requested_deadline_missed_status(datareader):
    """
    This test checks:
    - DataReader::get_requested_deadline_missed_status
    """
    status = fastdds.RequestedDeadlineMissedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_requested_deadline_missed_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_instance_handle)


def test_get_requested_incompatible_qos_status(datareader):
    """
    This test checks:
    - DataReader::get_requested_deadline_missed_status
    """
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


def test_get_sample_lost_status(datareader):
    """
    This test checks:
    - DataReader::get_sample_lost_status
    """
    status = fastdds.SampleLostStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_sample_lost_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)


def test_get_sample_rejected_status(datareader):
    """
    This test checks:
    - DataReader::get_sample_rejected_status
    """
    status = fastdds.SampleRejectedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_sample_rejected_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)


def test_get_subscription_matched_status(datareader):
    """
    This test checks:
    - DataReader::get_subscription_matched_status
    """
    status = fastdds.SubscriptionMatchedStatus()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.get_subscription_matched_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(0 == status.current_count)
    assert(0 == status.current_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_publication_handle)


def test_get_subscriber(subscriber, datareader):
    """
    This test checks:
    - DataReader::get_subscriber
    """
    sub = datareader.get_subscriber()
    assert(sub == subscriber)


def test_get_topicdescription(topic, datareader):
    """
    This test checks:
    - DataReader::get_topicdescription
    """
    topic_aux = datareader.get_topicdescription()
    assert(topic.get_impl() == topic_aux.get_impl())
    assert(topic.get_type_name() == topic_aux.get_type_name())


def test_get_unread_count(transient_datareader_qos, datareader,
                          datawriter):
    """
    This test checks:
    - DataReader::get_unread_count
    """
    assert(0 == datareader.get_unread_count())

    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(1 == datareader.get_unread_count())


def test_is_sample_valid(transient_datareader_qos, datareader,
                         datawriter):
    """
    This test checks:
    - DataReader::is_sample_valid
    """
    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    data = test_complete.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.read_next_sample(data, info))
    assert(datareader.is_sample_valid(data, info))
    assert(sample.int16_field() == data.int16_field())


def test_lookup_instance(transient_datareader_qos, test_keyed_type, datareader,
                         datawriter):
    """
    This test checks:
    - DataReader::lookup_instance
    """

    # Test when parameter is None
    ih = datareader.lookup_instance(None)
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    # Test when instance is not registered
    sample = test_complete.KeyedCompleteTestType()
    sample.id(3)
    ih = datareader.lookup_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    # Test when instance is registered
    writer_ih = datawriter.register_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown != writer_ih)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.write(sample, writer_ih))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    ih = datareader.lookup_instance(sample)
    assert(writer_ih == ih)


def test_read(transient_datareader_qos, datareader,
              datawriter):
    """
    This test checks:
    - DataReader::read
    - DataReader::return_loan
    """
    data_seq = test_complete.CompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.read(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
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


def test_read_instance(transient_datareader_qos, test_keyed_type,
                       datareader, datawriter):
    """
    This test checks:
    - DataReader::read_instance
    - DataReader::return_loan
    """
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

    sample = test_complete.KeyedCompleteTestType()
    sample.id(255)
    ih = datawriter.register_instance(sample)
    assert(datawriter.write(sample, ih))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.read_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.id() == data_seq[0].id())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_read_next_instance(transient_datareader_qos, test_keyed_type,
                            datareader, datawriter):
    """
    This test checks:
    - DataReader::read_next_instance
    - DataReader::return_loan
    """
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

    sample = test_complete.KeyedCompleteTestType()
    sample.id(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.read_next_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.id() == data_seq[0].id())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_read_next_sample(transient_datareader_qos, datareader,
                          datawriter):
    """
    This test checks:
    - DataReader::read_next_sample
    """
    data = test_complete.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.read_next_sample(
                data, info))

    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.read_next_sample(data, info))
    assert(info.valid_data)
    assert(sample.int16_field() == data.int16_field())


def test_take(transient_datareader_qos, datareader,
              datawriter):
    """
    This test checks:
    - DataReader::take
    - DataReader::return_loan
    """
    data_seq = test_complete.CompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.take(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
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


def test_take_instance(transient_datareader_qos, test_keyed_type,
                       datareader, datawriter):
    """
    This test checks:
    - DataReader::take_instance
    - DataReader::return_loan
    """
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

    sample = test_complete.KeyedCompleteTestType()
    sample.id(255)
    ih = datawriter.register_instance(sample)
    assert(datawriter.write(sample, ih))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.take_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.id() == data_seq[0].id())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_take_next_instance(transient_datareader_qos, test_keyed_type,
                            datareader, datawriter):
    """
    This test checks:
    - DataReader::take_next_instance
    - DataReader::return_loan
    """
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

    sample = test_complete.KeyedCompleteTestType()
    sample.id(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.take_next_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(sample.id() == data_seq[0].id())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_take_next_sample(transient_datareader_qos, datareader,
                          datawriter):
    """
    This test checks:
    - DataReader::take_next_sample
    """
    data = test_complete.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.ReturnCode_t.RETCODE_NO_DATA ==
           datareader.take_next_sample(
                data, info))

    sample = test_complete.CompleteTestType()
    sample.int16_field(255)
    assert(datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.take_next_sample(data, info))
    assert(info.valid_data)
    assert(sample.int16_field() == data.int16_field())


def test_get_type(test_type, datareader):
    """
    This test checks:
    - DataReader::type
    """
    test_type_aux = datareader.type()
    assert(test_type == test_type_aux)
    assert(test_type.get_type_name() == test_type_aux.get_type_name())


def test_wait_for_historical_data(datareader):
    """
    This test checks:
    - DataReader::wait_for_historical_data
    """
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           datareader.wait_for_historical_data(
               fastdds.Duration_t(0, 100)))


def test_wait_for_unread_message(datareader):
    """
    This test checks:
    - DataReader::wait_for_unread_message
    """
    assert(not datareader.wait_for_unread_message(fastdds.Duration_t(0, 100)))


def test_listener_ownership(participant, writer_participant, topic,
                            writer_topic, subscriber, publisher):

    def create_datareader():
        listener = DataReaderListener()
        return subscriber.create_datareader(
                topic, fastdds.DATAREADER_QOS_DEFAULT, listener)

    datareader = create_datareader()
    datawriter = publisher.create_datawriter(
                writer_topic, fastdds.DATAWRITER_QOS_DEFAULT)
    time.sleep(1)
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           writer_participant.delete_topic(writer_topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           writer_participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(writer_participant))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
