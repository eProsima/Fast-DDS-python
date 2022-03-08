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

    # Overlay 1
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

    # Overlay 2
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
    assert(guid.entityId.value[0] == ih.value[12])
    assert(guid.entityId.value[1] == ih.value[13])
    assert(guid.entityId.value[2] == ih.value[14])
    assert(guid.entityId.value[3] == ih.value[15])

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

    # Overload 2
    # - StatusMask.none
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.none()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.none() == datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_none()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_none() == datawriter.get_status_mask())
    # - StatusMask.data_available
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.data_available()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.data_available() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_data_available()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_data_available() ==
           datawriter.get_status_mask())
    # - StatusMask.data_on_readers
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.data_on_readers()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.data_on_readers() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_data_on_readers()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_data_on_readers() ==
           datawriter.get_status_mask())
    # - StatusMask.inconsistent_topic
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.inconsistent_topic()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.inconsistent_topic() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_inconsistent_topic()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_inconsistent_topic() ==
           datawriter.get_status_mask())
    # - StatusMask.liveliness_changed
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.liveliness_changed()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.liveliness_changed() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_liveliness_changed()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_liveliness_changed() ==
           datawriter.get_status_mask())
    # - StatusMask.liveliness_lost
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.liveliness_lost()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.liveliness_lost() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_liveliness_lost()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_liveliness_lost() ==
           datawriter.get_status_mask())
    # - StatusMask.offered_deadline_missed
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.offered_deadline_missed()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.offered_deadline_missed() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_offered_deadline_missed()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_offered_deadline_missed() ==
           datawriter.get_status_mask())
    # - StatusMask.offered_incompatible_qos
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.offered_incompatible_qos()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.offered_incompatible_qos() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_offered_incompatible_qos()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_offered_incompatible_qos() ==
           datawriter.get_status_mask())
    # - StatusMask.publication_matched
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.publication_matched()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.publication_matched() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_publication_matched()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_publication_matched() ==
           datawriter.get_status_mask())
    # - StatusMask.requested_deadline_missed
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.requested_deadline_missed()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.requested_deadline_missed() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_requested_deadline_missed()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_requested_deadline_missed() ==
           datawriter.get_status_mask())
    # - StatusMask.requested_incompatible_qos
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.requested_incompatible_qos()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.requested_incompatible_qos() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_requested_incompatible_qos()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_requested_incompatible_qos() ==
           datawriter.get_status_mask())
    # - StatusMask.sample_lost
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.sample_lost()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.sample_lost() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_sample_lost()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_sample_lost() ==
           datawriter.get_status_mask())
    # - StatusMask.sample_rejected
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.sample_rejected()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.sample_rejected() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_sample_rejected()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_sample_rejected() ==
           datawriter.get_status_mask())
    # - StatusMask.subscription_matched
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.subscription_matched()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.subscription_matched() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_subscription_matched()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_subscription_matched() ==
           datawriter.get_status_mask())
    # - StatusMask.all
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask.all()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.all() ==
           datawriter.get_status_mask())
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
               listener, fastdds.StatusMask_all()))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_all() ==
           datawriter.get_status_mask())
    # - Mix all  values of StatusMask
    listener = DataWriterListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.set_listener(
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
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    listener = DataWriterListener()
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
           datawriter.set_listener(listener, m))
    assert(datawriter.get_listener() == listener)
    assert(fastdds.StatusMask_all() == datawriter.get_status_mask())

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


def test_matched_subscription_data():
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


def test_matched_subscription_data():
    """
    This test checks:
    - DataWriter::get_matched_subscriptions
    """
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

    # Overlay 1
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

    # Overlay 2
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

    # Overlay 1
    sample = test_complete.KeyedCompleteTestType()
    assert(datawriter.write(sample))

    # Overlay 2
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

    # Overlay 3
    sample = test_complete.KeyedCompleteTestType()
    sample.id(1)
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datawriter.write(sample, ih))
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert(fastdds.ReturnCode_t.RETCODE_PRECONDITION_NOT_MET ==
           datawriter.write(sample, ih))

    # Overlay 4
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
#
#    /**
#     * @brief Get a pointer to the internal pool where the user could directly write.
#     *
#     * This method can only be used on a DataWriter for a plain data type. It will provide the
#     * user with a pointer to an internal buffer where the data type can be prepared for sending.
#     *
#     * When using NO_LOAN_INITIALIZATION on the initialization parameter, which is the default,
#     * no assumptions should be made on the contents where the pointer points to, as it may be an
#     * old pointer being reused. See @ref LoanInitializationKind for more details.
#     *
#     * Once the sample has been prepared, it can then be published by calling @ref write.
#     * After a successful call to @ref write, the middleware takes ownership of the loaned pointer again,
#     * and the user should not access that memory again.
#     *
#     * If, for whatever reason, the sample is not published, the loan can be returned by calling
#     * @ref discard_loan.
#     *
#     * @param [out] sample          Pointer to the sample on the internal pool.
#     * @param [in]  initialization  How to initialize the loaned sample.
#     *
#     * @return ReturnCode_t::RETCODE_ILLEGAL_OPERATION when the data type does not support loans.
#     * @return ReturnCode_t::RETCODE_NOT_ENABLED if the writer has not been enabled.
#     * @return ReturnCode_t::RETCODE_OUT_OF_RESOURCES if the pool has been exhausted.
#     * @return ReturnCode_t::RETCODE_OK if a pointer to a sample is successfully obtained.
#     */
#    RTPS_DllAPI ReturnCode_t loan_sample(
#            void*& sample,
#            LoanInitializationKind initialization = LoanInitializationKind::NO_LOAN_INITIALIZATION);
#
#    /**
#     * @brief Discards a loaned sample pointer.
#     *
#     * See the description on @ref loan_sample for how and when to call this method.
#     *
#     * @param [in,out] sample  Pointer to the previously loaned sample.
#     *
#     * @return ReturnCode_t::RETCODE_ILLEGAL_OPERATION when the data type does not support loans.
#     * @return ReturnCode_t::RETCODE_NOT_ENABLED if the writer has not been enabled.
#     * @return ReturnCode_t::RETCODE_BAD_PARAMETER if the pointer does not correspond to a loaned sample.
#     * @return ReturnCode_t::RETCODE_OK if the loan is successfully discarded.
#     */
#    RTPS_DllAPI ReturnCode_t discard_loan(
#            void*& sample);
#
#    /**
#     * @brief Get the list of locators from which this DataWriter may send data.
#     *
#     * @param [out] locators  LocatorList where the list of locators will be stored.
#     *
#     * @return NOT_ENABLED if the reader has not been enabled.
#     * @return OK if a list of locators is returned.
#     */
#    RTPS_DllAPI ReturnCode_t get_sending_locators(
#            rtps::LocatorList& locators) const;
