import fastdds


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
