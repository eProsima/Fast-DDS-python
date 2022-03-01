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

    # Overload 3
    # - StatusMask.none
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.none())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.none() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_none())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_none() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.data_available
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.data_available())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.data_available() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_data_available())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_data_available() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.data_on_readers
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.data_on_readers())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.data_on_readers() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_data_on_readers())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_data_on_readers() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.inconsistent_topic
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.inconsistent_topic())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.inconsistent_topic() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_inconsistent_topic())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_inconsistent_topic() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.liveliness_changed
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.liveliness_changed())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.liveliness_changed() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_liveliness_changed())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_liveliness_changed() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.liveliness_lost
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.liveliness_lost())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.liveliness_lost() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_liveliness_lost())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_liveliness_lost() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.offered_deadline_missed
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.offered_deadline_missed())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.offered_deadline_missed() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_offered_deadline_missed())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_offered_deadline_missed() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.offered_incompatible_qos
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.offered_incompatible_qos())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.offered_incompatible_qos() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_offered_incompatible_qos())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_offered_incompatible_qos() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.publication_matched
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.publication_matched())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.publication_matched() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_publication_matched())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_publication_matched() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.requested_deadline_missed
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.requested_deadline_missed())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.requested_deadline_missed() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_requested_deadline_missed())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_requested_deadline_missed() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.requested_incompatible_qos
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.requested_incompatible_qos())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.requested_incompatible_qos() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_requested_incompatible_qos())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_requested_incompatible_qos() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.sample_lost
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.sample_lost())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.sample_lost() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_sample_lost())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_sample_lost() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.sample_rejected
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.sample_rejected())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.sample_rejected() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_sample_rejected())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_sample_rejected() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.subscription_matched
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.subscription_matched())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.subscription_matched() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_subscription_matched())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_subscription_matched() ==
           datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - StatusMask.all
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask.all())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
            listener, fastdds.StatusMask_all())
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask_all() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    # - Mix all  values of StatusMask
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT,
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
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
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
    datareader = subscriber.create_datareader(
            topic, fastdds.DATAREADER_QOS_DEFAULT, listener, m)
    assert(datareader is not None)
    assert(datareader.is_enabled())
    assert(fastdds.StatusMask.all() == datareader.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           subscriber.delete_datareader(datareader))

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
