import fastdds

import inspect


def test_topic_qos():
    # TopicQos
    topic_qos = fastdds.TopicQos()

    # .topic_data
    topic_qos.topic_data().push_back(0)
    topic_qos.topic_data().push_back(1)
    topic_qos.topic_data().push_back(2)
    topic_qos.topic_data().push_back(3)
    count = 1
    for topic_value in topic_qos.topic_data():
        if 1 == count:
            assert(0 == topic_value)
        elif 2 == count:
            assert(1 == topic_value)
        elif 3 == count:
            assert(2 == topic_value)
        else:
            assert(3 == topic_value)
        count += 1

    # .durability
    topic_qos.durability().kind = fastdds.TRANSIENT_DURABILITY_QOS
    assert(fastdds.TRANSIENT_DURABILITY_QOS == topic_qos.durability().kind)

    # .durability_service
    topic_qos.durability_service().history_kind = fastdds.KEEP_ALL_HISTORY_QOS
    topic_qos.durability_service().history_depth = 10
    topic_qos.durability_service().max_samples = 5
    topic_qos.durability_service().max_instances = 20
    topic_qos.durability_service().max_samples_per_instance = 30
    assert(fastdds.KEEP_ALL_HISTORY_QOS == topic_qos.durability_service().history_kind)
    assert(10 == topic_qos.durability_service().history_depth)
    assert(5 == topic_qos.durability_service().max_samples)
    assert(20 == topic_qos.durability_service().max_instances)
    assert(30 == topic_qos.durability_service().max_samples_per_instance)

    # .deadline
    topic_qos.deadline().period.seconds = 10
    topic_qos.deadline().period.nanosec = 20
    assert(10 == topic_qos.deadline().period.seconds)
    assert(20 == topic_qos.deadline().period.nanosec)

    # .latency_budget
    topic_qos.latency_budget().duration.seconds = 20
    topic_qos.latency_budget().duration.nanosec = 30
    assert(20 == topic_qos.latency_budget().duration.seconds)
    assert(30 == topic_qos.latency_budget().duration.nanosec)

    # .liveliness
    topic_qos.liveliness().kind = fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
    topic_qos.liveliness().lease_duration.seconds = 40
    topic_qos.liveliness().lease_duration.nanosec = 61
    topic_qos.liveliness().announcement_period.seconds = 30
    topic_qos.liveliness().announcement_period.nanosec = 50
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS == topic_qos.liveliness().kind)
    assert(40 == topic_qos.liveliness().lease_duration.seconds)
    assert(61 == topic_qos.liveliness().lease_duration.nanosec)
    assert(30 == topic_qos.liveliness().announcement_period.seconds)
    assert(50 == topic_qos.liveliness().announcement_period.nanosec)

    # .reliability
    topic_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    topic_qos.reliability().max_blocking_time.seconds = 100
    #TODO topic_qos.reliability().max_blocking_time.nanosec = fastdds.TIME_T_INFINITE_NANOSECONDS
    topic_qos.reliability().max_blocking_time.nanosec = 1000
    assert(fastdds.RELIABLE_RELIABILITY_QOS == topic_qos.reliability().kind)
    assert(100 == topic_qos.reliability().max_blocking_time.seconds)
    assert(1000 == topic_qos.reliability().max_blocking_time.nanosec)


    # .destination_order
    topic_qos.destination_order().kind = fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS == topic_qos.destination_order().kind)

    # .history
    topic_qos.history().kind = fastdds.KEEP_ALL_HISTORY_QOS
    topic_qos.history().depth = 1000
    assert(fastdds.KEEP_ALL_HISTORY_QOS == topic_qos.history().kind)
    assert(1000 == topic_qos.history().depth)

    # .resource_limits
    topic_qos.resource_limits().max_samples = 3000
    topic_qos.resource_limits().max_instances = 100
    topic_qos.resource_limits().max_samples_per_instance = 500
    topic_qos.resource_limits().allocated_samples = 50
    topic_qos.resource_limits().extra_samples = 2
    assert(3000 == topic_qos.resource_limits().max_samples)
    assert(100 == topic_qos.resource_limits().max_instances)
    assert(500 == topic_qos.resource_limits().max_samples_per_instance)
    assert(50 == topic_qos.resource_limits().allocated_samples)
    assert(2 == topic_qos.resource_limits().extra_samples)

    # .transport_priority
    topic_qos.transport_priority().value = 10
    assert(10 == topic_qos.transport_priority().value)

    # .lifespan
    topic_qos.lifespan().duration.seconds = 10
    topic_qos.lifespan().duration.nanosec = 33
    assert(10 == topic_qos.lifespan().duration.seconds)
    assert(33 == topic_qos.lifespan().duration.nanosec)

    # .ownership
    topic_qos.ownership().kind = fastdds.EXCLUSIVE_OWNERSHIP_QOS
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS == topic_qos.ownership().kind)

    # Check agains default_topic_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(None != participant)
    participant.set_default_topic_qos(topic_qos)

    default_topic_qos = fastdds.TopicQos()
    participant.get_default_topic_qos(default_topic_qos)
    factory.delete_participant(participant)

    # .topic_data
    count = 1
    for topic_value in default_topic_qos.topic_data():
        if 1 == count:
            assert(0 == topic_value)
        elif 2 == count:
            assert(1 == topic_value)
        elif 3 == count:
            assert(2 == topic_value)
        else:
            assert(3 == topic_value)
        count += 1

    # .durability
    assert(fastdds.TRANSIENT_DURABILITY_QOS == default_topic_qos.durability().kind)

    # .durability_service
    assert(fastdds.KEEP_ALL_HISTORY_QOS == default_topic_qos.durability_service().history_kind)
    assert(10 == default_topic_qos.durability_service().history_depth)
    assert(5 == default_topic_qos.durability_service().max_samples)
    assert(20 == default_topic_qos.durability_service().max_instances)
    assert(30 == default_topic_qos.durability_service().max_samples_per_instance)

    # .deadline
    assert(10 == default_topic_qos.deadline().period.seconds)
    assert(20 == default_topic_qos.deadline().period.nanosec)

    # .latency_budget
    assert(20 == default_topic_qos.latency_budget().duration.seconds)
    assert(30 == default_topic_qos.latency_budget().duration.nanosec)

    # .liveliness
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS == default_topic_qos.liveliness().kind)
    assert(40 == default_topic_qos.liveliness().lease_duration.seconds)
    assert(61 == default_topic_qos.liveliness().lease_duration.nanosec)
    assert(30 == default_topic_qos.liveliness().announcement_period.seconds)
    assert(50 == default_topic_qos.liveliness().announcement_period.nanosec)

    # .reliability
    assert(fastdds.RELIABLE_RELIABILITY_QOS == default_topic_qos.reliability().kind)
    assert(100 == default_topic_qos.reliability().max_blocking_time.seconds)
    assert(1000 == default_topic_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS == default_topic_qos.destination_order().kind)

    # .history
    assert(fastdds.KEEP_ALL_HISTORY_QOS == default_topic_qos.history().kind)
    assert(1000 == default_topic_qos.history().depth)

    # .resource_limits
    assert(3000 == default_topic_qos.resource_limits().max_samples)
    assert(100 == default_topic_qos.resource_limits().max_instances)
    assert(500 == default_topic_qos.resource_limits().max_samples_per_instance)
    assert(50 == default_topic_qos.resource_limits().allocated_samples)
    assert(2 == default_topic_qos.resource_limits().extra_samples)

    # .transport_priority
    assert(10 == default_topic_qos.transport_priority().value)

    # .lifespan
    assert(10 == default_topic_qos.lifespan().duration.seconds)
    assert(33 == default_topic_qos.lifespan().duration.nanosec)

    # .ownership
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS == default_topic_qos.ownership().kind)


def test_subscriber_qos():
    # SubscriberQos
    subscriber_qos = fastdds.SubscriberQos()


    # .presentation
    subscriber_qos.presentation().access_scope = fastdds.TOPIC_PRESENTATION_QOS
    subscriber_qos.presentation().coherent_access = True
    subscriber_qos.presentation().ordered_access = True
    assert(fastdds.TOPIC_PRESENTATION_QOS == subscriber_qos.presentation().access_scope)
    assert(True == subscriber_qos.presentation().coherent_access)
    assert(True == subscriber_qos.presentation().ordered_access)

    # .partition
    subscriber_qos.partition().push_back('Partition1')
    subscriber_qos.partition().push_back('Partition2')
    assert('Partition1' == subscriber_qos.partition()[0])
    assert('Partition2' == subscriber_qos.partition()[1])

    # .group_data
    subscriber_qos.group_data().push_back(0)
    subscriber_qos.group_data().push_back(1)
    subscriber_qos.group_data().push_back(2)
    subscriber_qos.group_data().push_back(3)
    count = 1
    for group_value in subscriber_qos.group_data():
        if 1 == count:
            assert(0 == group_value)
        elif 2 == count:
            assert(1 == group_value)
        elif 3 == count:
            assert(2 == group_value)
        else:
            assert(3 == group_value)
        count += 1

    # .entity_factory
    subscriber_qos.entity_factory().autoenable_created_entities = False
    assert(False == subscriber_qos.entity_factory().autoenable_created_entities)

    # Check agains default_subscriber_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(None != participant)
    participant.set_default_subscriber_qos(subscriber_qos)

    default_subscriber_qos = fastdds.SubscriberQos()
    participant.get_default_subscriber_qos(default_subscriber_qos)
    factory.delete_participant(participant)

    # .presentation
    assert(fastdds.TOPIC_PRESENTATION_QOS == default_subscriber_qos.presentation().access_scope)
    assert(True == default_subscriber_qos.presentation().coherent_access)
    assert(True == default_subscriber_qos.presentation().ordered_access)

    # .partition
    assert('Partition1' == default_subscriber_qos.partition()[0])
    assert('Partition2' == default_subscriber_qos.partition()[1])

    # . group_data
    count = 1
    for group_value in default_subscriber_qos.group_data():
        if 1 == count:
            assert(0 == group_value)
        elif 2 == count:
            assert(1 == group_value)
        elif 3 == count:
            assert(2 == group_value)
        else:
            assert(3 == group_value)
        count += 1

    # .entity_factory
    assert(False == default_subscriber_qos.entity_factory().autoenable_created_entities)


def test_publisher_qos():
    # PublisherQos
    publisher_qos = fastdds.PublisherQos()


    # .presentation
    publisher_qos.presentation().access_scope = fastdds.TOPIC_PRESENTATION_QOS
    publisher_qos.presentation().coherent_access = True
    publisher_qos.presentation().ordered_access = True
    assert(fastdds.TOPIC_PRESENTATION_QOS == publisher_qos.presentation().access_scope)
    assert(True == publisher_qos.presentation().coherent_access)
    assert(True == publisher_qos.presentation().ordered_access)

    # .partition
    publisher_qos.partition().push_back('Partition1')
    publisher_qos.partition().push_back('Partition2')
    assert('Partition1' == publisher_qos.partition()[0])
    assert('Partition2' == publisher_qos.partition()[1])

    # .group_data
    publisher_qos.group_data().push_back(0)
    publisher_qos.group_data().push_back(1)
    publisher_qos.group_data().push_back(2)
    publisher_qos.group_data().push_back(3)
    count = 1
    for group_value in publisher_qos.group_data():
        if 1 == count:
            assert(0 == group_value)
        elif 2 == count:
            assert(1 == group_value)
        elif 3 == count:
            assert(2 == group_value)
        else:
            assert(3 == group_value)
        count += 1

    # .entity_factory
    publisher_qos.entity_factory().autoenable_created_entities = False
    assert(False == publisher_qos.entity_factory().autoenable_created_entities)

    # Check agains default_publisher_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(None != participant)
    participant.set_default_publisher_qos(publisher_qos)

    default_publisher_qos = fastdds.PublisherQos()
    participant.get_default_publisher_qos(default_publisher_qos)
    factory.delete_participant(participant)

    # .presentation
    assert(fastdds.TOPIC_PRESENTATION_QOS == default_publisher_qos.presentation().access_scope)
    assert(True == default_publisher_qos.presentation().coherent_access)
    assert(True == default_publisher_qos.presentation().ordered_access)

    # .partition
    assert('Partition1' == default_publisher_qos.partition()[0])
    assert('Partition2' == default_publisher_qos.partition()[1])

    # . group_data
    count = 1
    for group_value in default_publisher_qos.group_data():
        if 1 == count:
            assert(0 == group_value)
        elif 2 == count:
            assert(1 == group_value)
        elif 3 == count:
            assert(2 == group_value)
        else:
            assert(3 == group_value)
        count += 1

    # .entity_factory
    assert(False == default_publisher_qos.entity_factory().autoenable_created_entities)

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
    participant_qos.flow_controllers().push_back(flow)
    flow = fastdds.FlowControllerDescriptor()
    flow.name = 'Flow2'
    flow.max_bytes_per_period = 5000
    flow.period_ms = 3000
    flow.scheduler = fastdds.FlowControllerSchedulerPolicy_HIGH_PRIORITY
    participant_qos.flow_controllers().push_back(flow)
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
    participant_qos.properties().properties().push_back(property)
    property = fastdds.Property()
    property.name('Property2')
    property.value('Value2')
    participant_qos.properties().properties().push_back(property)
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

    participant_qos.user_data().push_back(0)
    participant_qos.user_data().push_back(1)
    participant_qos.user_data().push_back(2)
    participant_qos.user_data().push_back(3)
    count = 1
    for user_value in participant_qos.user_data():
        if 1 == count:
            assert(0 == user_value)
        elif 2 == count:
            assert(1 == user_value)
        elif 3 == count:
            assert(2 == user_value)
        else:
            assert(3 == user_value)
        count += 1

    # .wire_protocol
    participant_qos.wire_protocol().prefix.value = (1,2,3,4,5,6,7,8,9,10,11,12)
    participant_qos.wire_protocol().participant_id = 32
    assert((1,2,3,4,5,6,7,8,9,10,11,12) == participant_qos.wire_protocol().prefix.value)
    assert(32 == participant_qos.wire_protocol().participant_id)

    ## .builtin
    participant_qos.wire_protocol().builtin.use_WriterLivelinessProtocol = False
    participant_qos.wire_protocol().builtin.readerHistoryMemoryPolicy = fastdds.PREALLOCATED_MEMORY_MODE;
    participant_qos.wire_protocol().builtin.readerPayloadSize = 3
    participant_qos.wire_protocol().builtin.writerHistoryMemoryPolicy = fastdds.PREALLOCATED_MEMORY_MODE;
    participant_qos.wire_protocol().builtin.writerPayloadSize = 5
    participant_qos.wire_protocol().builtin.mutation_tries = 50;
    participant_qos.wire_protocol().builtin.avoid_builtin_multicast = False
    assert(False == participant_qos.wire_protocol().builtin.use_WriterLivelinessProtocol)
    assert(fastdds.PREALLOCATED_MEMORY_MODE == participant_qos.wire_protocol().builtin.readerHistoryMemoryPolicy)
    assert(3 == participant_qos.wire_protocol().builtin.readerPayloadSize)
    assert(fastdds.PREALLOCATED_MEMORY_MODE == participant_qos.wire_protocol().builtin.writerHistoryMemoryPolicy)
    assert(5 == participant_qos.wire_protocol().builtin.writerPayloadSize)
    assert(50 == participant_qos.wire_protocol().builtin.mutation_tries)
    assert(False == participant_qos.wire_protocol().builtin.avoid_builtin_multicast)
    ### .discovery_config
    participant_qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol = False
    participant_qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol = True
    participant_qos.wire_protocol().builtin.discovery_config.leaseDuration.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config.leaseDuration.nanosec = 10
    participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod.nanosec =  10
    participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.count = 10
    participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.period.seconds =  30
    participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.period.nanosec =  10
    participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP. use_PublicationWriterANDSubscriptionReader = False
    participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationReaderANDSubscriptionWriter = False
    found_secure_member = False
    members = inspect.getmembers(participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP)
    for m in members:
        if 'enable_builtin_secure_publications_writer_and_subscriptions_reader' == m[0]:
            found_secure_member = True
            break
    if found_secure_member:
        participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.enable_builtin_secure_publications_writer_and_subscriptions_reader = False
        participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.enable_builtin_secure_subscriptions_writer_and_publications_reader = False
    participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.nanosec = 10
    participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.nanosec = 10
    server_info = fastdds.RemoteServerAttributes()
    server_info.guidPrefix.value = (1,2,3,4,5,6,7,8,9,10,11,12)
    locator = fastdds.Locator_t()
    locator.address = (0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,1)
    locator.port = 7400
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    server_info.metatrafficMulticastLocatorList.push_back(locator)
    server_info.metatrafficUnicastLocatorList.push_back(locator)
    participant_qos.wire_protocol().builtin.discovery_config.m_DiscoveryServers.push_back(server_info)
    participant_qos.wire_protocol().builtin.discovery_config.ignoreParticipantFlags = fastdds.FILTER_DIFFERENT_HOST
    assert(False == participant_qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol)
    assert(True == participant_qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol)
    assert(30 == participant_qos.wire_protocol().builtin.discovery_config.leaseDuration.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.leaseDuration.nanosec)
    assert(30 == participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod.nanosec)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.count)
    assert(30 == participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.period.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.period.nanosec)
    assert(False == participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP. use_PublicationWriterANDSubscriptionReader)
    assert(False == participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationReaderANDSubscriptionWriter)
    if found_secure_member:
        assert(False == participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.enable_builtin_secure_publications_writer_and_subscriptions_reader)
        assert(False == participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.enable_builtin_secure_subscriptions_writer_and_publications_reader)
    assert(30 == participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.nanosec)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.nanosec)
    server_info = participant_qos.wire_protocol().builtin.discovery_config.m_DiscoveryServers[0]
    assert((1,2,3,4,5,6,7,8,9,10,11,12) == server_info.guidPrefix.value)
    locator = server_info.metatrafficMulticastLocatorList[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,1) == locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    locator = server_info.metatrafficUnicastLocatorList[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,1) == locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    assert(fastdds.FILTER_DIFFERENT_HOST == participant_qos.wire_protocol().builtin.discovery_config.ignoreParticipantFlags)
    ### .typelookup_config;
    participant_qos.wire_protocol().builtin.typelookup_config.use_client = True
    participant_qos.wire_protocol().builtin.typelookup_config.use_server = True
    assert(True == participant_qos.wire_protocol().builtin.typelookup_config.use_client)
    assert(True == participant_qos.wire_protocol().builtin.typelookup_config.use_server)
    ### .metatrafficUnicastLocatorList;
    locator = fastdds.Locator_t()
    locator.address = (0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,2)
    locator.port = 7401
    locator.kind = fastdds.LOCATOR_KIND_TCPv4
    participant_qos.wire_protocol().builtin.metatrafficUnicastLocatorList.push_back(locator)
    locator = participant_qos.wire_protocol().builtin.metatrafficUnicastLocatorList[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,2) == locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    ### .metatrafficMulticastLocatorList;
    locator = fastdds.Locator_t()
    locator.address = (1,0,0,0,0,0,0,0,0,0,0,0,255,233,0,9)
    locator.port = 7411
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    participant_qos.wire_protocol().builtin.metatrafficMulticastLocatorList.push_back(locator)
    locator = participant_qos.wire_protocol().builtin.metatrafficMulticastLocatorList[0]
    assert((1,0,0,0,0,0,0,0,0,0,0,0,255,233,0,9) == locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    ### .initialPeersList;
    locator = fastdds.Locator_t()
    locator.address = (1,0,255,0,0,0,0,0,0,0,0,0,127,0,0,1)
    locator.port = 1024
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    participant_qos.wire_protocol().builtin.initialPeersList.push_back(locator)
    locator = participant_qos.wire_protocol().builtin.initialPeersList[0]
    assert((1,0,255,0,0,0,0,0,0,0,0,0,127,0,0,1) == locator.address)
    assert(1024 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    ## .default_multicast_locator_list
    locator = fastdds.Locator_t()
    locator.address = (1,0,0,0,0,0,0,0,0,0,0,0,255,233,0,9)
    locator.port = 7411
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    participant_qos.wire_protocol().default_multicast_locator_list.push_back(locator)
    locator = participant_qos.wire_protocol().default_multicast_locator_list[0]
    assert((1,0,0,0,0,0,0,0,0,0,0,0,255,233,0,9) == locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    ## .default_unicast_locator_list
    locator = fastdds.Locator_t()
    locator.address = (0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,2)
    locator.port = 7401
    locator.kind = fastdds.LOCATOR_KIND_TCPv4
    participant_qos.wire_protocol().default_unicast_locator_list.push_back(locator)
    locator = participant_qos.wire_protocol().default_unicast_locator_list[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,2) == locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    ## .port
    participant_qos.wire_protocol().port.portBase = 7410
    participant_qos.wire_protocol().port.domainIDGain = 200
    participant_qos.wire_protocol().port.participantIDGain = 3
    participant_qos.wire_protocol().port.offsetd0 = 1
    participant_qos.wire_protocol().port.offsetd1 = 11
    participant_qos.wire_protocol().port.offsetd2 = 21
    participant_qos.wire_protocol().port.offsetd3 = 22
    assert(7410 == participant_qos.wire_protocol().port.portBase)
    assert(200 == participant_qos.wire_protocol().port.domainIDGain)
    assert(3 == participant_qos.wire_protocol().port.participantIDGain)
    assert(1 == participant_qos.wire_protocol().port.offsetd0)
    assert(11 == participant_qos.wire_protocol().port.offsetd1)
    assert(21 == participant_qos.wire_protocol().port.offsetd2)
    assert(22 == participant_qos.wire_protocol().port.offsetd3)

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

    # .user_data
    count = 1
    for user_value in default_participant_qos.user_data():
        if 1 == count:
            assert(0 == user_value)
        elif 2 == count:
            assert(1 == user_value)
        elif 3 == count:
            assert(2 == user_value)
        else:
            assert(3 == user_value)
        count += 1


    # .wire_protocol
    assert((1,2,3,4,5,6,7,8,9,10,11,12) == default_participant_qos.wire_protocol().prefix.value)
    assert(32 == default_participant_qos.wire_protocol().participant_id)
    ## .builtin
    assert(False == default_participant_qos.wire_protocol().builtin.use_WriterLivelinessProtocol)
    assert(fastdds.PREALLOCATED_MEMORY_MODE == default_participant_qos.wire_protocol().builtin.readerHistoryMemoryPolicy)
    assert(3 == default_participant_qos.wire_protocol().builtin.readerPayloadSize)
    assert(fastdds.PREALLOCATED_MEMORY_MODE == default_participant_qos.wire_protocol().builtin.writerHistoryMemoryPolicy)
    assert(5 == default_participant_qos.wire_protocol().builtin.writerPayloadSize)
    assert(50 == default_participant_qos.wire_protocol().builtin.mutation_tries)
    assert(False == default_participant_qos.wire_protocol().builtin.avoid_builtin_multicast)
    ### .discovery_config
    assert(False == default_participant_qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol)
    assert(True == default_participant_qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol)
    assert(30 == default_participant_qos.wire_protocol().builtin.discovery_config.leaseDuration.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.discovery_config.leaseDuration.nanosec)
    assert(30 == default_participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod.nanosec)
    assert(10 == default_participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.count)
    assert(30 == default_participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.period.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.discovery_config.initial_announcements.period.nanosec)
    assert(False == default_participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP. use_PublicationWriterANDSubscriptionReader)
    assert(False == default_participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationReaderANDSubscriptionWriter)
    if found_secure_member:
        assert(False == default_participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.enable_builtin_secure_publications_writer_and_subscriptions_reader)
        assert(False == default_participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP.enable_builtin_secure_subscriptions_writer_and_publications_reader)
    assert(30 == default_participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.nanosec)
    assert(10 == default_participant_qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod.nanosec)
    server_info = default_participant_qos.wire_protocol().builtin.discovery_config.m_DiscoveryServers[0]
    assert((1,2,3,4,5,6,7,8,9,10,11,12) == server_info.guidPrefix.value)
    locator = server_info.metatrafficMulticastLocatorList[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,1) == locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    locator = server_info.metatrafficUnicastLocatorList[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,1) == locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    assert(fastdds.FILTER_DIFFERENT_HOST == default_participant_qos.wire_protocol().builtin.discovery_config.ignoreParticipantFlags)
    ### .typelookup_config;
    assert(True == default_participant_qos.wire_protocol().builtin.typelookup_config.use_client)
    assert(True == default_participant_qos.wire_protocol().builtin.typelookup_config.use_server)
    ### .metatrafficUnicastLocatorList;
    locator = default_participant_qos.wire_protocol().builtin.metatrafficUnicastLocatorList[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,2) == locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    ### .metatrafficMulticastLocatorList;
    locator = default_participant_qos.wire_protocol().builtin.metatrafficMulticastLocatorList[0]
    assert((1,0,0,0,0,0,0,0,0,0,0,0,255,233,0,9) == locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    ### .initialPeersList;
    locator = default_participant_qos.wire_protocol().builtin.initialPeersList[0]
    assert((1,0,255,0,0,0,0,0,0,0,0,0,127,0,0,1) == locator.address)
    assert(1024 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    ## .default_multicast_locator_list
    locator = default_participant_qos.wire_protocol().default_multicast_locator_list[0]
    assert((1,0,0,0,0,0,0,0,0,0,0,0,255,233,0,9) == locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    ## .default_unicast_locator_list
    locator = default_participant_qos.wire_protocol().default_unicast_locator_list[0]
    assert((0,0,0,0,0,0,0,0,0,0,0,0,192,168,1,2) == locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    ## .port
    assert(7410 == default_participant_qos.wire_protocol().port.portBase)
    assert(200 == default_participant_qos.wire_protocol().port.domainIDGain)
    assert(3 == default_participant_qos.wire_protocol().port.participantIDGain)
    assert(1 == default_participant_qos.wire_protocol().port.offsetd0)
    assert(11 == default_participant_qos.wire_protocol().port.offsetd1)
    assert(21 == default_participant_qos.wire_protocol().port.offsetd2)
    assert(22 == default_participant_qos.wire_protocol().port.offsetd3)
