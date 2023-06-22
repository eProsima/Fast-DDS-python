# until https://bugs.python.org/issue46276 is not fixed we can apply this
# workaround on windows
import os
if os.name == 'nt':
    import win32api
    win32api.LoadLibrary('test_complete')
    win32api.LoadLibrary('eprosima/test/test_modules')

import fastdds
import pytest


@pytest.fixture(params=['no_module', 'module'], autouse=True)
def data_type(request):
    if request.param == 'no_module':
        pytest.dds_type = __import__("test_complete")
    else:
        pytest.dds_type = __import__("eprosima.test.test_modules",
                                    fromlist=[None])

@pytest.fixture
def participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)


@pytest.fixture
def subscriber(participant):
    return participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)


@pytest.fixture
def topic(participant):
    test_type = fastdds.TypeSupport(
            pytest.dds_type.CompleteTestTypePubSubType())
    participant.register_type(test_type, test_type.get_type_name())
    return participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def datareader(participant, topic, subscriber):
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
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
def writer_topic(writer_participant):
    test_type = fastdds.TypeSupport(
            pytest.dds_type.CompleteTestTypePubSubType())
    writer_participant.register_type(test_type, test_type.get_type_name())
    return writer_participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def publisher(writer_participant):
    return writer_participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)


@pytest.fixture
def datawriter(writer_participant, writer_topic, publisher):
    datawriter_qos = fastdds.DataWriterQos()
    datawriter_qos.reliability().kind = fastdds.BEST_EFFORT_RELIABILITY_QOS
    datawriter = publisher.create_datawriter(writer_topic, datawriter_qos)

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


def test_waitset(datareader, datawriter):
    status_cond = datareader.get_statuscondition()
    guard_cond = fastdds.GuardCondition()
    read_cond = datareader.create_readcondition(
            fastdds.ANY_SAMPLE_STATE,
            fastdds.ANY_VIEW_STATE,
            fastdds.ANY_INSTANCE_STATE)
    assert(read_cond is not None)

    waitset = fastdds.WaitSet()
    attached_conds = fastdds.ConditionSeq()
    conds = fastdds.ConditionSeq()

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.attach_condition(status_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.attach_condition(guard_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.attach_condition(read_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.get_conditions(attached_conds))
    assert(3 == len(attached_conds))
    for c in attached_conds:
        if ('StatusCondition' == str(c)):
            for m in [c.to_guard_condition, c.to_read_condition]:
                try:
                    m()
                    assert(False)
                except TypeError:
                    pass

            attached_status_cond = c.to_status_condition()
            assert(status_cond == attached_status_cond)
        elif ('GuardCondition' == str(c)):
            for m in [c.to_status_condition, c.to_read_condition]:
                try:
                    m()
                    assert(False)
                except TypeError:
                    pass

            attached_guard_cond = c.to_guard_condition()
            assert(guard_cond == attached_guard_cond)
        elif ('ReadCondition' == str(c)):
            for m in [c.to_status_condition, c.to_guard_condition]:
                try:
                    m()
                    assert(False)
                except TypeError:
                    pass

            attached_read_cond = c.to_read_condition()
            assert(read_cond == attached_read_cond)

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.wait(conds, fastdds.Duration_t(1, 0)))

    assert(1 == len(conds))
    assert('StatusCondition' == str(conds[0]))
    attached_status_cond = conds[0].to_status_condition()
    assert(attached_status_cond is not None)
    entity = attached_status_cond.get_entity()
    assert(entity is not None)
    changed_statuses = entity.get_status_changes()
    assert(changed_statuses.is_active(
        fastdds.StatusMask.requested_incompatible_qos()))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.detach_condition(status_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.detach_condition(guard_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.detach_condition(read_cond))

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           datareader.delete_readcondition(read_cond))
