import fastdds
import test_complete


class PublisherListener (fastdds.PublisherListener):
    def __init__(self):
        super().__init__()


class DataWriterListener (fastdds.DataWriterListener):
    def __init__(self):
        super().__init__()


def test_coherent_changes():
    """
    This test checks:
    - Publisher::begin_coherent_changes
    - Publisher::end_coherent_changes
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.begin_coherent_changes())
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.end_coherent_changes())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_and_delete_datawriter():
    """
    This test checks:
    - Publisher::create_datawriter
    - Publisher::delete_datawriter
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
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    # Overload 1 - Success
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
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

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_deleted_contained_entities():
    """
    This test checks:
    - Publisher::delete_contained_entities
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_contained_entities())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_enable():
    """
    This test checks:
    - Publisher::enable
    - Publisher::is_enabled
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    qos = fastdds.DomainParticipantQos()
    qos.entity_factory().autoenable_created_entities = False
    participant = factory.create_participant(0, qos)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    assert(not publisher.is_enabled())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.enable())
    assert(publisher.is_enabled())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_datawriters():
    """
    This test checks:
    - Publisher::get_datawriters
    - Publisher::has_datawriters
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
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
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_instance_handle():
    """
    This test checks:
    - Publisher::get_instance_handle
    - Publisher::guid
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    ih = publisher.get_instance_handle()
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
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_participant():
    """
    This test checks:
    - Publisher::get_participant
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    participant2 = publisher.get_participant()
    assert(participant2 is not None)
    assert(participant == participant2)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_get_set_qos():
    """
    This test checks:
    - Publisher::get_qos
    - Publisher::set_qos
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    qos = fastdds.PublisherQos()
    publisher = participant.create_publisher(qos)
    assert(publisher is not None)

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

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
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
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    # Overload 1
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(listener))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())

    # Overload 2
    # - StatusMask.none
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.none()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.none() == publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_none()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_none() == publisher.get_status_mask())
    # - StatusMask.data_available
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.data_available()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.data_available() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_data_available()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_data_available() ==
           publisher.get_status_mask())
    # - StatusMask.data_on_readers
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.data_on_readers()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.data_on_readers() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_data_on_readers()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_data_on_readers() ==
           publisher.get_status_mask())
    # - StatusMask.inconsistent_topic
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.inconsistent_topic()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.inconsistent_topic() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_inconsistent_topic()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_inconsistent_topic() ==
           publisher.get_status_mask())
    # - StatusMask.liveliness_changed
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.liveliness_changed()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.liveliness_changed() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_liveliness_changed()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_liveliness_changed() ==
           publisher.get_status_mask())
    # - StatusMask.liveliness_lost
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.liveliness_lost()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.liveliness_lost() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_liveliness_lost()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_liveliness_lost() ==
           publisher.get_status_mask())
    # - StatusMask.offered_deadline_missed
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.offered_deadline_missed()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.offered_deadline_missed() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_offered_deadline_missed()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_offered_deadline_missed() ==
           publisher.get_status_mask())
    # - StatusMask.offered_incompatible_qos
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.offered_incompatible_qos()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.offered_incompatible_qos() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_offered_incompatible_qos()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_offered_incompatible_qos() ==
           publisher.get_status_mask())
    # - StatusMask.publication_matched
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.publication_matched()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.publication_matched() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_publication_matched()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_publication_matched() ==
           publisher.get_status_mask())
    # - StatusMask.requested_deadline_missed
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.requested_deadline_missed()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.requested_deadline_missed() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_requested_deadline_missed()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_requested_deadline_missed() ==
           publisher.get_status_mask())
    # - StatusMask.requested_incompatible_qos
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.requested_incompatible_qos()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.requested_incompatible_qos() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_requested_incompatible_qos()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_requested_incompatible_qos() ==
           publisher.get_status_mask())
    # - StatusMask.sample_lost
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.sample_lost()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.sample_lost() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_sample_lost()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_sample_lost() ==
           publisher.get_status_mask())
    # - StatusMask.sample_rejected
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.sample_rejected()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.sample_rejected() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_sample_rejected()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_sample_rejected() ==
           publisher.get_status_mask())
    # - StatusMask.subscription_matched
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.subscription_matched()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.subscription_matched() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_subscription_matched()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_subscription_matched() ==
           publisher.get_status_mask())
    # - StatusMask.all
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask.all()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.all() ==
           publisher.get_status_mask())
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
               listener, fastdds.StatusMask_all()))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_all() ==
           publisher.get_status_mask())
    # - Mix all  values of StatusMask
    listener = PublisherListener()
    assert(listener is not None)
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.set_listener(
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
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask.all() == publisher.get_status_mask())
    listener = PublisherListener()
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
           publisher.set_listener(listener, m))
    assert(publisher.get_listener() == listener)
    assert(fastdds.StatusMask_all() == publisher.get_status_mask())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_lookup_datawriter():
    """
    This test checks:
    - Publisher::lookup_datawriter
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    # Overload 1 - Success
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT)
    assert(datawriter is not None)

    datawriter2 = publisher.lookup_datawriter('Complete')
    assert(datawriter2 is not None)
    assert(datawriter == datawriter2)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_suspend_publications():
    """
    This test checks:
    - Publisher::suspend_publications
    - Publisher::resume_publications
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.suspend_publications())
    assert(fastdds.ReturnCode_t.RETCODE_UNSUPPORTED ==
           publisher.resume_publications())

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


def test_wait_for_acknowlegments():
    """
    This test checks:
    - Publisher::wait_for_acknowledgments
    """
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.wait_for_acknowledgments(fastdds.Duration_t(3, 0)))
    # TODO Test a timeout

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))


#
#    /**
#     * This operation creates a DataWriter. The returned DataWriter will be attached and belongs to the Publisher.
#     *
#     * @param topic Topic the DataWriter will be listening
#     * @param profile_name DataWriter profile name.
#     * @param listener Pointer to the listener (default: nullptr).
#     * @param mask StatusMask that holds statuses the listener responds to (default: all).
#     * @return Pointer to the created DataWriter. nullptr if failed.
#     */
#    RTPS_DllAPI DataWriter* create_datawriter_with_profile(
#            Topic* topic,
#            const std::string& profile_name,
#            DataWriterListener* listener = nullptr,
#            const StatusMask& mask = StatusMask::all());
#
#
#    /**
#     * @brief Copies TopicQos into the corresponding DataWriterQos
#     *
#     * @param[out] writer_qos
#     * @param[in] topic_qos
#     * @return RETCODE_OK if successful, an error code otherwise
#     */
#    RTPS_DllAPI ReturnCode_t copy_from_topic_qos(
#            fastdds::dds::DataWriterQos& writer_qos,
#            const fastdds::dds::TopicQos& topic_qos) const;
#
#    /**
#     * Fills the DataWriterQos with the values of the XML profile.
#     *
#     * @param profile_name DataWriter profile name.
#     * @param qos DataWriterQos object where the qos is returned.
#     * @return RETCODE_OK if the profile exists. RETCODE_BAD_PARAMETER otherwise.
#     */
#    RTPS_DllAPI ReturnCode_t get_datawriter_qos_from_profile(
#            const std::string& profile_name,
#            DataWriterQos& qos) const;
