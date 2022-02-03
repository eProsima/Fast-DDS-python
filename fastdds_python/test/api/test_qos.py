import fastdds

import inspect

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
