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

    # .entity_factory
    participant_qos.entity_factory().autoenable_created_entities = False
    assert(False == participant_qos.entity_factory().autoenable_created_entities)

    # .flow_controllers
    flow = fastdds.FlowControllerDescriptor()
    flow.name = 'Flow1'
    flow.max_bytes_per_period = 3000
    flow.period_ms = 5000
    flow.scheduler = fastdds.FlowControllerSchedulerPolicy_ROUND_ROBIN
    participant_qos.flow_controllers().append(flow)
    flow = fastdds.FlowControllerDescriptor()
    flow.name = 'Flow2'
    flow.max_bytes_per_period = 5000
    flow.period_ms = 3000
    flow.scheduler = fastdds.FlowControllerSchedulerPolicy_HIGH_PRIORITY
    participant_qos.flow_controllers().append(flow)
    count = 1
    for flow_controller in participant_qos.flow_controllers():
        if 1 == count:
            assert('Flow1' == flow_controller.name)
            assert(3000 == flow_controller.max_bytes_per_period)
            assert(5000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_ROUND_ROBIN == flow_controller.scheduler)
        else:
            assert('Flow2' == flow_controller.name)
            assert(5000 == flow_controller.max_bytes_per_period)
            assert(3000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_HIGH_PRIORITY == flow_controller.scheduler)
        count += 1

    # .name
    participant_qos.name("test name")
    assert("test name" == participant_qos.name())

    # .properties
    property = fastdds.Property()
    property.name('Property1')
    property.value('Value1')
    participant_qos.properties().properties().append(property)
    property = fastdds.Property()
    property.name('Property2')
    property.value('Value2')
    participant_qos.properties().properties().append(property)
    count = 1
    for prop in participant_qos.properties().properties():
        if 1 == count:
            assert('Property1' == prop.name())
            assert('Value1' == prop.value())
        else:
            assert('Property2' == prop.name())
            assert('Value2' == prop.value())
        count += 1

    # .transports
    participant_qos.transport().listen_socket_buffer_size = 10000
    participant_qos.transport().send_socket_buffer_size = 20000
    participant_qos.transport().use_builtin_transports = False
    assert(10000 == participant_qos.transport().listen_socket_buffer_size)
    assert(20000 == participant_qos.transport().send_socket_buffer_size)
    assert(False == participant_qos.transport().use_builtin_transports)

    # Check agains default_participant_qos
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

    # .entity_factory
    assert(False == default_participant_qos.entity_factory().autoenable_created_entities)

    # .flow_controllers
    count = 1
    for flow_controller in default_participant_qos.flow_controllers():
        if 1 == count:
            assert('Flow1' == flow_controller.name)
            assert(3000 == flow_controller.max_bytes_per_period)
            assert(5000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_ROUND_ROBIN == flow_controller.scheduler)
        else:
            assert('Flow2' == flow_controller.name)
            assert(5000 == flow_controller.max_bytes_per_period)
            assert(3000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_HIGH_PRIORITY == flow_controller.scheduler)
        count += 1

    # .name
    assert("test name" == default_participant_qos.name())

    # .properties
    count = 1
    for prop in default_participant_qos.properties().properties():
        if 1 == count:
            assert('Property1' == prop.name())
            assert('Value1' == prop.value())
        else:
            assert('Property2' == prop.name())
            assert('Value2' == prop.value())
        count += 1

    # .transports
    assert(10000 == default_participant_qos.transport().listen_socket_buffer_size)
    assert(20000 == default_participant_qos.transport().send_socket_buffer_size)
    assert(False == default_participant_qos.transport().use_builtin_transports)
