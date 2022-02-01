import fastdds

def test_participant_qos():
    # DomainParticipantQos
    participant_qos = fastdds.DomainParticipantQos()

    # .allocation
    participant_qos.allocation().data_limits.max_properties = 10
    participant_qos.allocation().data_limits.max_user_data = 20
    participant_qos.allocation().data_limits.max_partitions = 30
    participant_qos.allocation().data_limits.max_datasharing_domains = 40
    assert(10 == participant_qos.allocation().data_limits.max_properties)
    assert(20 == participant_qos.allocation().data_limits.max_user_data)
    assert(30 == participant_qos.allocation().data_limits.max_partitions)
    assert(40 == participant_qos.allocation().data_limits.max_datasharing_domains)
    participant_qos.allocation().locators.max_unicast_locators = 10
    participant_qos.allocation().locators.max_multicast_locators = 20
    assert(10 == participant_qos.allocation().locators.max_unicast_locators)
    assert(20 == participant_qos.allocation().locators.max_multicast_locators)
    participant_qos.allocation().participants.initial = 10
    participant_qos.allocation().participants.maximum = 20
    participant_qos.allocation().participants.increment = 3
    assert(10 == participant_qos.allocation().participants.initial)
    assert(20 == participant_qos.allocation().participants.maximum)
    assert(3 == participant_qos.allocation().participants.increment)
    participant_qos.allocation().writers.initial = 10
    participant_qos.allocation().writers.maximum = 20
    participant_qos.allocation().writers.increment = 3
    assert(10 == participant_qos.allocation().writers.initial)
    assert(20 == participant_qos.allocation().writers.maximum)
    assert(3 == participant_qos.allocation().writers.increment)
    participant_qos.allocation().readers.initial = 10
    participant_qos.allocation().readers.maximum = 20
    participant_qos.allocation().readers.increment = 3
    assert(10 == participant_qos.allocation().readers.initial)
    assert(20 == participant_qos.allocation().readers.maximum)
    assert(3 == participant_qos.allocation().readers.increment)
    participant_qos.allocation().send_buffers.preallocated_number = 10
    participant_qos.allocation().send_buffers.dynamic = True
    assert(10 == participant_qos.allocation().send_buffers.preallocated_number)
    assert(True == participant_qos.allocation().send_buffers.dynamic)
    assert(100 == participant_qos.allocation().total_readers().initial)
    assert(400 == participant_qos.allocation().total_readers().maximum)
    assert(3 == participant_qos.allocation().total_readers().increment)
    assert(100 == participant_qos.allocation().total_writers().initial)
    assert(400 == participant_qos.allocation().total_writers().maximum)
    assert(3 == participant_qos.allocation().total_writers().increment)

    # .name
    participant_qos.name("test name")
    assert("test name" == participant_qos.name())

    factory = fastdds.DomainParticipantFactory.get_instance()
    factory.set_default_participant_qos(participant_qos)

    default_participant_qos = fastdds.DomainParticipantQos()
    factory.get_default_participant_qos(default_participant_qos)

    # .allocation
    assert(10 == default_participant_qos.allocation().data_limits.max_properties)
    assert(20 == default_participant_qos.allocation().data_limits.max_user_data)
    assert(30 == default_participant_qos.allocation().data_limits.max_partitions)
    assert(40 == default_participant_qos.allocation().data_limits.max_datasharing_domains)
    assert(10 == default_participant_qos.allocation().locators.max_unicast_locators)
    assert(20 == default_participant_qos.allocation().locators.max_multicast_locators)
    assert(10 == default_participant_qos.allocation().participants.initial)
    assert(20 == default_participant_qos.allocation().participants.maximum)
    assert(3 == default_participant_qos.allocation().participants.increment)
    assert(10 == default_participant_qos.allocation().writers.initial)
    assert(20 == default_participant_qos.allocation().writers.maximum)
    assert(3 == default_participant_qos.allocation().writers.increment)
    assert(10 == default_participant_qos.allocation().readers.initial)
    assert(20 == default_participant_qos.allocation().readers.maximum)
    assert(3 == default_participant_qos.allocation().readers.increment)
    assert(10 == default_participant_qos.allocation().send_buffers.preallocated_number)
    assert(True == default_participant_qos.allocation().send_buffers.dynamic)
    assert(100 == default_participant_qos.allocation().total_readers().initial)
    assert(400 == default_participant_qos.allocation().total_readers().maximum)
    assert(3 == default_participant_qos.allocation().total_readers().increment)
    assert(100 == default_participant_qos.allocation().total_writers().initial)
    assert(400 == default_participant_qos.allocation().total_writers().maximum)
    assert(3 == default_participant_qos.allocation().total_writers().increment)

    # .name
    assert("test name" == default_participant_qos.name())
