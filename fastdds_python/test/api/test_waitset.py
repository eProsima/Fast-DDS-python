#!/usr/bin/python3

# until https://bugs.python.org/issue46276 is not fixed we can apply this
# workaround on windows
import os
if os.name == 'nt':
    import win32api
    win32api.LoadLibrary('_fastdds_python.pyd')
    win32api.LoadLibrary('_test_completeWrapper.pyd')

import fastdds
import test_complete

def test_waitset():
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(factory is not None)
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    test_type = fastdds.TypeSupport(test_complete.CompleteTestTypePubSubType())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.register_type(test_type, test_type.get_type_name()))
    topic = participant.create_topic(
            "Complete", "CompleteTestType", fastdds.TOPIC_QOS_DEFAULT)
    assert(topic is not None)
    datawriter_qos = fastdds.DataWriterQos()
    datawriter_qos.reliability().kind = fastdds.BEST_EFFORT_RELIABILITY_QOS
    datawriter = publisher.create_datawriter(topic, datawriter_qos)
    assert(datawriter is not None)
    datareader_qos = fastdds.DataReaderQos()
    datareader_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    datareader = subscriber.create_datareader(topic, datareader_qos)
    assert(datareader is not None)

    status_cond = datareader.get_statuscondition()
    guard_cond = fastdds.GuardCondition()
    waitset = fastdds.WaitSet()
    attached_conds = fastdds.ConditionSeq()
    conds = fastdds.ConditionSeq()

    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.attach_condition(status_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.attach_condition(guard_cond))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           waitset.get_conditions(attached_conds))
    assert(2 == len(attached_conds))
    for c in attached_conds:
        if ('StatusCondition' == str(c)):
            try:
                attached_status_cond = c.to_guard_condition()
                assert(False)
            except TypeError:
                pass
            attached_status_cond = c.to_status_condition()
            assert(status_cond == attached_status_cond)
        elif ('GuardCondition' == str(c)):
            try:
                attached_guard_cond = c.to_status_condition()
                assert(False)
            except TypeError:
                pass
            attached_guard_cond = c.to_guard_condition()
            assert(guard_cond == attached_guard_cond)

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
           subscriber.delete_datareader(datareader))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_publisher(publisher))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
