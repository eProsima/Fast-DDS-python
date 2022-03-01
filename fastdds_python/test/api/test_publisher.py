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

    # Overload 3
    # - StatusMask.none
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.none())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.none() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_none())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_none() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.data_available
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.data_available())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.data_available() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_data_available())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_data_available() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.data_on_readers
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.data_on_readers())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.data_on_readers() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_data_on_readers())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_data_on_readers() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.inconsistent_topic
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.inconsistent_topic())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.inconsistent_topic() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_inconsistent_topic())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_inconsistent_topic() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.liveliness_changed
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.liveliness_changed())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.liveliness_changed() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_liveliness_changed())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_liveliness_changed() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.liveliness_lost
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.liveliness_lost())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.liveliness_lost() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_liveliness_lost())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_liveliness_lost() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.offered_deadline_missed
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.offered_deadline_missed())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.offered_deadline_missed() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_offered_deadline_missed())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_offered_deadline_missed() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.offered_incompatible_qos
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.offered_incompatible_qos())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.offered_incompatible_qos() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_offered_incompatible_qos())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_offered_incompatible_qos() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.publication_matched
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.publication_matched())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.publication_matched() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_publication_matched())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_publication_matched() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.requested_deadline_missed
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.requested_deadline_missed())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.requested_deadline_missed() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_requested_deadline_missed())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_requested_deadline_missed() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.requested_incompatible_qos
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.requested_incompatible_qos())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.requested_incompatible_qos() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_requested_incompatible_qos())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_requested_incompatible_qos() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.sample_lost
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.sample_lost())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.sample_lost() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_sample_lost())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_sample_lost() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.sample_rejected
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.sample_rejected())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.sample_rejected() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_sample_rejected())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_sample_rejected() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.subscription_matched
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.subscription_matched())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.subscription_matched() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_subscription_matched())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_subscription_matched() ==
           datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - StatusMask.all
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.all())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask_all())
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask_all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    # - Mix all  values of StatusMask
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT,
            listener, fastdds.StatusMask.data_available() <<
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
            fastdds.StatusMask.subscription_matched()
            )
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
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
    datawriter = publisher.create_datawriter(
            topic, fastdds.DATAWRITER_QOS_DEFAULT, listener, m)
    assert(datawriter is not None)
    assert(datawriter.is_enabled())
    assert(fastdds.StatusMask.all() == datawriter.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))

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
#     * This operation blocks the calling thread until either all data written by the reliable DataWriter entities
#     * is acknowledged by all matched reliable DataReader entities, or else the duration specified by the max_wait
#     * parameter elapses, whichever happens first. A return value of true indicates that all the samples written
#     * have been acknowledged by all reliable matched data readers; a return value of false indicates that max_wait
#     * elapsed before all the data was acknowledged.
#     *
#     * @param max_wait Maximum blocking time for this operation
#     * @return RETCODE_TIMEOUT if the function takes more than the maximum blocking time established, RETCODE_OK if the
#     * Publisher receives the acknowledgments and RETCODE_ERROR otherwise.
#     */
#    RTPS_DllAPI ReturnCode_t wait_for_acknowledgments(
#            const fastrtps::Duration_t& max_wait);
#
#    /**
#     * This operation returns the DomainParticipant to which the Publisher belongs.
#     *
#     * @return Pointer to the DomainParticipant
#     */
#    RTPS_DllAPI const DomainParticipant* get_participant() const;
#
#    /**
#     * @brief Deletes all contained DataWriters
#     *
#     * @return RETCODE_OK if successful, an error code otherwise
#     */
#    RTPS_DllAPI ReturnCode_t delete_contained_entities();
#
#    /**
#     * This operation sets a default value of the DataWriter QoS policies which will be used for newly created
#     * DataWriter entities in the case where the QoS policies are defaulted in the create_datawriter operation.
#     *
#     * This operation will check that the resulting policies are self consistent; if they are not, the operation
#     * will have no effect and return false.
#     *
#     * The special value DATAWRITER_QOS_DEFAULT may be passed to this operation to indicate that the default QoS
#     * should be reset back to the initial values the factory would use, that is the values that would be used
#     * if the set_default_datawriter_qos operation had never been called.
#     *
#     * @param qos DataWriterQos to be set
#     * @return RETCODE_INCONSISTENT_POLICY if the Qos is not self consistent and RETCODE_OK if the qos is changed correctly.
#     */
#    RTPS_DllAPI ReturnCode_t set_default_datawriter_qos(
#            const DataWriterQos& qos);
#
#    /**
#     * This operation returns the default value of the DataWriter QoS, that is, the QoS policies which will be used
#     * for newly created DataWriter entities in the case where the QoS policies are defaulted in the
#     * create_datawriter operation.
#     *
#     * The values retrieved by get_default_datawriter_qos will match the set of values specified on the last
#     * successful call to set_default_datawriter_qos, or else, if the call was never made, the default values.
#     *
#     * @return Current default WriterQos
#     */
#    RTPS_DllAPI const DataWriterQos& get_default_datawriter_qos() const;
#
#    /**
#     * This operation retrieves the default value of the DataWriter QoS, that is, the QoS policies which will be used
#     * for newly created DataWriter entities in the case where the QoS policies are defaulted in the
#     * create_datawriter operation.
#     *
#     * The values retrieved by get_default_datawriter_qos will match the set of values specified on the last
#     * successful call to set_default_datawriter_qos, or else, if the call was never made, the default values.
#     *
#     * @param qos Reference to the current default WriterQos.
#     * @return RETCODE_OK
#     */
#    RTPS_DllAPI ReturnCode_t get_default_datawriter_qos(
#            DataWriterQos& qos) const;
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
#
#    /**
#     * Returns the Publisher's handle.
#     *
#     * @return InstanceHandle of this Publisher.
#     */
#    RTPS_DllAPI const InstanceHandle_t& get_instance_handle() const;
#
#    /**
#     * Fills the given vector with all the datawriters of this publisher.
#     *
#     * @param writers Vector where the DataWriters are returned
#     * @return true
#     */
#    RTPS_DllAPI bool get_datawriters(
#            std::vector<DataWriter*>& writers) const;
#
#    /**
#     * This operation checks if the publisher has DataWriters
#     *
#     * @return true if the publisher has one or several DataWriters, false otherwise
#     */
#    RTPS_DllAPI bool has_datawriters() const;
