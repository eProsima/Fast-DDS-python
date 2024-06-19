import os

import fastdds

import inspect


def test_datareader_qos():
    # DataReaderQos
    datareader_qos = fastdds.DataReaderQos()

    # .durability
    datareader_qos.durability().kind = fastdds.TRANSIENT_DURABILITY_QOS
    assert(fastdds.TRANSIENT_DURABILITY_QOS ==
           datareader_qos.durability().kind)

    # .deadline
    datareader_qos.deadline().period.seconds = 10
    datareader_qos.deadline().period.nanosec = 20
    assert(10 == datareader_qos.deadline().period.seconds)
    assert(20 == datareader_qos.deadline().period.nanosec)

    # .latency_budget
    datareader_qos.latency_budget().duration.seconds = 20
    datareader_qos.latency_budget().duration.nanosec = 30
    assert(20 == datareader_qos.latency_budget().duration.seconds)
    assert(30 == datareader_qos.latency_budget().duration.nanosec)

    # .liveliness
    datareader_qos.liveliness().kind = \
        fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
    datareader_qos.liveliness().lease_duration.seconds = 40
    datareader_qos.liveliness().lease_duration.nanosec = 61
    datareader_qos.liveliness().announcement_period.seconds = 30
    datareader_qos.liveliness().announcement_period.nanosec = 50
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS ==
           datareader_qos.liveliness().kind)
    assert(40 == datareader_qos.liveliness().lease_duration.seconds)
    assert(61 == datareader_qos.liveliness().lease_duration.nanosec)
    assert(30 == datareader_qos.liveliness().announcement_period.seconds)
    assert(50 == datareader_qos.liveliness().announcement_period.nanosec)

    # .reliability
    datareader_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    datareader_qos.reliability().max_blocking_time.seconds = 100
    datareader_qos.reliability().max_blocking_time.nanosec = \
        fastdds.Time_t.INFINITE_NANOSECONDS
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           datareader_qos.reliability().kind)
    assert(100 == datareader_qos.reliability().max_blocking_time.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           datareader_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    datareader_qos.destination_order().kind = \
        fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS ==
           datareader_qos.destination_order().kind)

    # . history
    datareader_qos.history().kind = fastdds.KEEP_ALL_HISTORY_QOS
    datareader_qos.history().depth = 1000
    assert(fastdds.KEEP_ALL_HISTORY_QOS == datareader_qos.history().kind)
    assert(1000 == datareader_qos.history().depth)

    # .resource_limits
    datareader_qos.resource_limits().max_samples = 3000
    datareader_qos.resource_limits().max_instances = 100
    datareader_qos.resource_limits().max_samples_per_instance = 500
    datareader_qos.resource_limits().allocated_samples = 50
    datareader_qos.resource_limits().extra_samples = 2
    assert(3000 == datareader_qos.resource_limits().max_samples)
    assert(100 == datareader_qos.resource_limits().max_instances)
    assert(500 == datareader_qos.resource_limits().max_samples_per_instance)
    assert(50 == datareader_qos.resource_limits().allocated_samples)
    assert(2 == datareader_qos.resource_limits().extra_samples)

    # .user_data
    datareader_qos.user_data().push_back(0)
    datareader_qos.user_data().push_back(1)
    datareader_qos.user_data().push_back(2)
    datareader_qos.user_data().push_back(3)
    count = 1
    for user_value in datareader_qos.user_data():
        if 1 == count:
            assert(0 == user_value)
        elif 2 == count:
            assert(1 == user_value)
        elif 3 == count:
            assert(2 == user_value)
        else:
            assert(3 == user_value)
        count += 1

    # .ownership
    datareader_qos.ownership().kind = fastdds.EXCLUSIVE_OWNERSHIP_QOS
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS == datareader_qos.ownership().kind)

    # .time_based_filter
    datareader_qos.time_based_filter().minimum_separation.seconds = \
        fastdds.Time_t.INFINITE_SECONDS
    datareader_qos.time_based_filter().minimum_separation.nanosec = \
        fastdds.Time_t.INFINITE_NANOSECONDS
    assert(fastdds.Time_t.INFINITE_SECONDS ==
           datareader_qos.time_based_filter().minimum_separation.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           datareader_qos.time_based_filter().minimum_separation.nanosec)

    # .reader_data_lifecycle
    datareader_qos.reader_data_lifecycle(). \
        autopurge_disposed_samples_delay.seconds = 100
    datareader_qos.reader_data_lifecycle(). \
        autopurge_disposed_samples_delay.nanosec = 30000
    datareader_qos.reader_data_lifecycle(). \
        autopurge_no_writer_samples_delay.seconds = 30000
    datareader_qos.reader_data_lifecycle(). \
        autopurge_no_writer_samples_delay.nanosec = 100
    assert(100 == datareader_qos.reader_data_lifecycle().
           autopurge_disposed_samples_delay.seconds)
    assert(30000 == datareader_qos.reader_data_lifecycle().
           autopurge_disposed_samples_delay.nanosec)
    assert(30000 == datareader_qos.reader_data_lifecycle().
           autopurge_no_writer_samples_delay.seconds)
    assert(100 == datareader_qos.reader_data_lifecycle().
           autopurge_no_writer_samples_delay.nanosec)

    # .lifespan
    datareader_qos.lifespan().duration.seconds = 10
    datareader_qos.lifespan().duration.nanosec = 33
    assert(10 == datareader_qos.lifespan().duration.seconds)
    assert(33 == datareader_qos.lifespan().duration.nanosec)

    # .durability_service
    datareader_qos.durability_service().history_kind = \
        fastdds.KEEP_ALL_HISTORY_QOS
    datareader_qos.durability_service().history_depth = 10
    datareader_qos.durability_service().max_samples = 5
    datareader_qos.durability_service().max_instances = 20
    datareader_qos.durability_service().max_samples_per_instance = 30
    datareader_qos.durability_service().service_cleanup_delay.seconds = \
        fastdds.Time_t.INFINITE_SECONDS
    datareader_qos.durability_service().service_cleanup_delay.nanosec = \
        fastdds.Time_t.INFINITE_NANOSECONDS
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           datareader_qos.durability_service().history_kind)
    assert(10 == datareader_qos.durability_service().history_depth)
    assert(5 == datareader_qos.durability_service().max_samples)
    assert(20 == datareader_qos.durability_service().max_instances)
    assert(30 == datareader_qos.durability_service().max_samples_per_instance)
    assert(fastdds.Time_t.INFINITE_SECONDS ==
           datareader_qos.durability_service().service_cleanup_delay.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           datareader_qos.durability_service().service_cleanup_delay.nanosec)

    # .reliable_reader_qos
    datareader_qos.reliable_reader_qos().times.initial_acknack_delay.seconds = 34
    datareader_qos.reliable_reader_qos().times.initial_acknack_delay.nanosec = 32
    datareader_qos.reliable_reader_qos().times.heartbeat_response_delay. \
        seconds = 432
    datareader_qos.reliable_reader_qos().times.heartbeat_response_delay. \
        nanosec = 43
    datareader_qos.reliable_reader_qos().disable_positive_acks.enabled = True
    datareader_qos.reliable_reader_qos().disable_positive_acks.duration. \
        seconds = 13
    datareader_qos.reliable_reader_qos().disable_positive_acks.duration. \
        nanosec = 320
    assert(34 == datareader_qos.reliable_reader_qos().times.
           initial_acknack_delay.seconds)
    assert(32 == datareader_qos.reliable_reader_qos().times.
           initial_acknack_delay.nanosec)
    assert(432 == datareader_qos.reliable_reader_qos().times.
           heartbeat_response_delay.seconds)
    assert(43 == datareader_qos.reliable_reader_qos().times.
           heartbeat_response_delay.nanosec)
    assert(datareader_qos.reliable_reader_qos().
           disable_positive_acks.enabled)
    assert(13 == datareader_qos.reliable_reader_qos().
           disable_positive_acks.duration.seconds)
    assert(320 == datareader_qos.reliable_reader_qos().
           disable_positive_acks.duration.nanosec)

    # TODO .type_consistency

    # .expects_inline_qos
    datareader_qos.expects_inline_qos(True)
    assert(datareader_qos.expects_inline_qos())

    # .properties
    properties = {}
    property = fastdds.Property()
    property.name('Property1')
    property.value('Value1')
    datareader_qos.properties().properties().push_back(property)
    properties[property.name()] = [property.value(), False]
    property = fastdds.Property()
    property.name('Property2')
    property.value('Value2')
    datareader_qos.properties().properties().push_back(property)
    properties[property.name()] = [property.value(), False]
    for prop in datareader_qos.properties().properties():
        for proper in properties:
            if prop.name() == proper and prop.value() == properties[proper][0]:
                properties[proper][1] = True

    for prop in properties:
        assert(properties[proper][1])

    # .endpoint
    datareader_qos.endpoint().user_defined_id = 1
    datareader_qos.endpoint().entity_id = 2
    datareader_qos.endpoint().history_memory_policy = \
        fastdds.PREALLOCATED_WITH_REALLOC_MEMORY_MODE
    assert(1 == datareader_qos.endpoint().user_defined_id)
    assert(2 == datareader_qos.endpoint().entity_id)
    assert(fastdds.PREALLOCATED_WITH_REALLOC_MEMORY_MODE ==
           datareader_qos.endpoint().history_memory_policy)

    # .reader_resource_limits
    datareader_qos.reader_resource_limits(). \
        matched_publisher_allocation.initial = 30
    datareader_qos.reader_resource_limits(). \
        matched_publisher_allocation.maximum = 300
    datareader_qos.reader_resource_limits(). \
        matched_publisher_allocation.increment = 4
    datareader_qos.reader_resource_limits(). \
        sample_infos_allocation.initial = 40
    datareader_qos.reader_resource_limits(). \
        sample_infos_allocation.maximum = 400
    datareader_qos.reader_resource_limits(). \
        sample_infos_allocation.increment = 5
    datareader_qos.reader_resource_limits(). \
        outstanding_reads_allocation.initial = 50
    datareader_qos.reader_resource_limits(). \
        outstanding_reads_allocation.maximum = 500
    datareader_qos.reader_resource_limits(). \
        outstanding_reads_allocation.increment = 6
    datareader_qos.reader_resource_limits().max_samples_per_read = 33
    assert(30 == datareader_qos.reader_resource_limits().
           matched_publisher_allocation.initial)
    assert(300 == datareader_qos.reader_resource_limits().
           matched_publisher_allocation.maximum)
    assert(4 == datareader_qos.reader_resource_limits().
           matched_publisher_allocation.increment)
    assert(40 == datareader_qos.reader_resource_limits().
           sample_infos_allocation.initial)
    assert(400 == datareader_qos.reader_resource_limits().
           sample_infos_allocation.maximum)
    assert(5 == datareader_qos.reader_resource_limits().
           sample_infos_allocation.increment)
    assert(50 == datareader_qos.reader_resource_limits().
           outstanding_reads_allocation.initial)
    assert(500 == datareader_qos.reader_resource_limits().
           outstanding_reads_allocation.maximum)
    assert(6 == datareader_qos.reader_resource_limits().
           outstanding_reads_allocation.increment)
    assert(33 == datareader_qos.reader_resource_limits().max_samples_per_read)

    # .data_sharing
    datareader_qos.data_sharing().on("/")
    datareader_qos.data_sharing().set_max_domains(3)
    assert(fastdds.ON == datareader_qos.data_sharing().kind())
    assert("/" == datareader_qos.data_sharing().shm_directory())
    assert(3 == datareader_qos.data_sharing().max_domains())
    datareader_qos.data_sharing().clear()
    assert(fastdds.AUTO == datareader_qos.data_sharing().kind())
    assert("" == datareader_qos.data_sharing().shm_directory())
    assert(0 == datareader_qos.data_sharing().max_domains())
    datareader_qos.data_sharing().on("/")
    datareader_qos.data_sharing().set_max_domains(3)
    assert(fastdds.ON == datareader_qos.data_sharing().kind())
    assert("/" == datareader_qos.data_sharing().shm_directory())
    assert(3 == datareader_qos.data_sharing().max_domains())

    # Check against default_datareader_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    subscriber = participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)
    assert(subscriber is not None)
    subscriber.set_default_datareader_qos(datareader_qos)

    default_datareader_qos = fastdds.DataReaderQos()
    subscriber.get_default_datareader_qos(default_datareader_qos)

    # Revert changes in default
    datareader_qos = fastdds.DataReaderQos()
    subscriber.set_default_datareader_qos(datareader_qos)

    participant.delete_subscriber(subscriber)
    factory.delete_participant(participant)

    # .durability
    assert(fastdds.TRANSIENT_DURABILITY_QOS ==
           default_datareader_qos.durability().kind)

    # .deadline
    assert(10 == default_datareader_qos.deadline().period.seconds)
    assert(20 == default_datareader_qos.deadline().period.nanosec)

    # .latency_budget
    assert(20 == default_datareader_qos.latency_budget().duration.seconds)
    assert(30 == default_datareader_qos.latency_budget().duration.nanosec)

    # .liveliness
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS ==
           default_datareader_qos.liveliness().kind)
    assert(40 == default_datareader_qos.liveliness().lease_duration.seconds)
    assert(61 == default_datareader_qos.liveliness().lease_duration.nanosec)
    assert(30 == default_datareader_qos.liveliness().
           announcement_period.seconds)
    assert(50 == default_datareader_qos.liveliness().
           announcement_period.nanosec)

    # .reliability
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           default_datareader_qos.reliability().kind)
    assert(100 == default_datareader_qos.reliability().
           max_blocking_time.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           default_datareader_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS ==
           default_datareader_qos.destination_order().kind)

    # . history
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           default_datareader_qos.history().kind)
    assert(1000 == default_datareader_qos.history().depth)

    # .resource_limits
    assert(3000 == default_datareader_qos.resource_limits().max_samples)
    assert(100 == default_datareader_qos.resource_limits().max_instances)
    assert(500 == default_datareader_qos.resource_limits().
           max_samples_per_instance)
    assert(50 == default_datareader_qos.resource_limits().allocated_samples)
    assert(2 == default_datareader_qos.resource_limits().extra_samples)

    # .user_data
    count = 1
    for user_value in default_datareader_qos.user_data():
        if 1 == count:
            assert(0 == user_value)
        elif 2 == count:
            assert(1 == user_value)
        elif 3 == count:
            assert(2 == user_value)
        else:
            assert(3 == user_value)
        count += 1

    # .ownership
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS ==
           default_datareader_qos.ownership().kind)

    # .time_based_filter
    assert(fastdds.Time_t.INFINITE_SECONDS == default_datareader_qos.
           time_based_filter().minimum_separation.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS == default_datareader_qos.
           time_based_filter().minimum_separation.nanosec)

    # .reader_data_lifecycle
    assert(100 == default_datareader_qos.reader_data_lifecycle().
           autopurge_disposed_samples_delay.seconds)
    assert(30000 == default_datareader_qos.reader_data_lifecycle().
           autopurge_disposed_samples_delay.nanosec)
    assert(30000 == default_datareader_qos.reader_data_lifecycle().
           autopurge_no_writer_samples_delay.seconds)
    assert(100 == default_datareader_qos.reader_data_lifecycle().
           autopurge_no_writer_samples_delay.nanosec)

    # .lifespan
    assert(10 == default_datareader_qos.lifespan().duration.seconds)
    assert(33 == default_datareader_qos.lifespan().duration.nanosec)

    # .durability_service
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           default_datareader_qos.durability_service().history_kind)
    assert(10 == default_datareader_qos.durability_service().history_depth)
    assert(5 == default_datareader_qos.durability_service().max_samples)
    assert(20 == default_datareader_qos.durability_service().max_instances)
    assert(30 == default_datareader_qos.durability_service().
           max_samples_per_instance)
    assert(fastdds.Time_t.INFINITE_SECONDS == default_datareader_qos.
           durability_service().service_cleanup_delay.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS == default_datareader_qos.
           durability_service().service_cleanup_delay.nanosec)

    # .reliable_reader_qos
    assert(34 == default_datareader_qos.reliable_reader_qos().times.
           initial_acknack_delay.seconds)
    assert(32 == default_datareader_qos.reliable_reader_qos().times.
           initial_acknack_delay.nanosec)
    assert(432 == default_datareader_qos.reliable_reader_qos().times.
           heartbeat_response_delay.seconds)
    assert(43 == default_datareader_qos.reliable_reader_qos().times.
           heartbeat_response_delay.nanosec)
    assert(default_datareader_qos.reliable_reader_qos().
           disable_positive_acks.enabled)
    assert(13 == default_datareader_qos.reliable_reader_qos().
           disable_positive_acks.duration.seconds)
    assert(320 == default_datareader_qos.reliable_reader_qos().
           disable_positive_acks.duration.nanosec)

    # .expects_inline_qos
    assert(default_datareader_qos.expects_inline_qos())

    # .properties
    count = 1
    for prop in default_datareader_qos.properties().properties():
        if 1 == count:
            assert('Property1' == prop.name())
            assert('Value1' == prop.value())
        else:
            assert('Property2' == prop.name())
            assert('Value2' == prop.value())
        count += 1

    # .endpoint
    assert(1 == default_datareader_qos.endpoint().user_defined_id)
    assert(2 == default_datareader_qos.endpoint().entity_id)
    assert(fastdds.PREALLOCATED_WITH_REALLOC_MEMORY_MODE ==
           default_datareader_qos.endpoint().history_memory_policy)

    # .reader_resource_limits
    assert(30 == default_datareader_qos.reader_resource_limits().
           matched_publisher_allocation.initial)
    assert(300 == default_datareader_qos.reader_resource_limits().
           matched_publisher_allocation.maximum)
    assert(4 == default_datareader_qos.reader_resource_limits().
           matched_publisher_allocation.increment)
    assert(40 == default_datareader_qos.reader_resource_limits().
           sample_infos_allocation.initial)
    assert(400 == default_datareader_qos.reader_resource_limits().
           sample_infos_allocation.maximum)
    assert(5 == default_datareader_qos.reader_resource_limits().
           sample_infos_allocation.increment)
    assert(50 == default_datareader_qos.reader_resource_limits().
           outstanding_reads_allocation.initial)
    assert(500 == default_datareader_qos.reader_resource_limits().
           outstanding_reads_allocation.maximum)
    assert(6 == default_datareader_qos.reader_resource_limits().
           outstanding_reads_allocation.increment)
    assert(33 == default_datareader_qos.reader_resource_limits().
           max_samples_per_read)

    # .data_sharing
    assert(fastdds.ON == default_datareader_qos.data_sharing().kind())
    assert("/" == default_datareader_qos.data_sharing().shm_directory())
    assert(3 == default_datareader_qos.data_sharing().max_domains())


def test_datawriter_qos():
    # DataWriterQos
    datawriter_qos = fastdds.DataWriterQos()

    # .durability
    datawriter_qos.durability().kind = fastdds.TRANSIENT_DURABILITY_QOS
    assert(fastdds.TRANSIENT_DURABILITY_QOS ==
           datawriter_qos.durability().kind)

    # .durability_service
    datawriter_qos.durability_service().history_kind = \
        fastdds.KEEP_ALL_HISTORY_QOS
    datawriter_qos.durability_service().history_depth = 10
    datawriter_qos.durability_service().max_samples = 5
    datawriter_qos.durability_service().max_instances = 20
    datawriter_qos.durability_service().max_samples_per_instance = 30
    datawriter_qos.durability_service().service_cleanup_delay.seconds = \
        fastdds.Time_t.INFINITE_SECONDS
    datawriter_qos.durability_service().service_cleanup_delay.nanosec = \
        fastdds.Time_t.INFINITE_NANOSECONDS
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           datawriter_qos.durability_service().history_kind)
    assert(10 == datawriter_qos.durability_service().history_depth)
    assert(5 == datawriter_qos.durability_service().max_samples)
    assert(20 == datawriter_qos.durability_service().max_instances)
    assert(30 == datawriter_qos.durability_service().max_samples_per_instance)
    assert(fastdds.Time_t.INFINITE_SECONDS ==
           datawriter_qos.durability_service().service_cleanup_delay.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           datawriter_qos.durability_service().service_cleanup_delay.nanosec)

    # .deadline
    datawriter_qos.deadline().period.seconds = 10
    datawriter_qos.deadline().period.nanosec = 20
    assert(10 == datawriter_qos.deadline().period.seconds)
    assert(20 == datawriter_qos.deadline().period.nanosec)

    # .latency_budget
    datawriter_qos.latency_budget().duration.seconds = 20
    datawriter_qos.latency_budget().duration.nanosec = 30
    assert(20 == datawriter_qos.latency_budget().duration.seconds)
    assert(30 == datawriter_qos.latency_budget().duration.nanosec)

    # .liveliness
    datawriter_qos.liveliness().kind = \
        fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
    datawriter_qos.liveliness().lease_duration.seconds = 40
    datawriter_qos.liveliness().lease_duration.nanosec = 61
    datawriter_qos.liveliness().announcement_period.seconds = 30
    datawriter_qos.liveliness().announcement_period.nanosec = 50
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS ==
           datawriter_qos.liveliness().kind)
    assert(40 == datawriter_qos.liveliness().lease_duration.seconds)
    assert(61 == datawriter_qos.liveliness().lease_duration.nanosec)
    assert(30 == datawriter_qos.liveliness().announcement_period.seconds)
    assert(50 == datawriter_qos.liveliness().announcement_period.nanosec)

    # .reliability
    datawriter_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    datawriter_qos.reliability().max_blocking_time.seconds = 100
    datawriter_qos.reliability().max_blocking_time.nanosec = \
        fastdds.Time_t.INFINITE_NANOSECONDS
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           datawriter_qos.reliability().kind)
    assert(100 == datawriter_qos.reliability().max_blocking_time.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           datawriter_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    datawriter_qos.destination_order().kind = \
        fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS ==
           datawriter_qos.destination_order().kind)

    # .history
    datawriter_qos.history().kind = fastdds.KEEP_ALL_HISTORY_QOS
    datawriter_qos.history().depth = 1000
    assert(fastdds.KEEP_ALL_HISTORY_QOS == datawriter_qos.history().kind)
    assert(1000 == datawriter_qos.history().depth)

    # .resource_limits
    datawriter_qos.resource_limits().max_samples = 3000
    datawriter_qos.resource_limits().max_instances = 100
    datawriter_qos.resource_limits().max_samples_per_instance = 500
    datawriter_qos.resource_limits().allocated_samples = 50
    datawriter_qos.resource_limits().extra_samples = 2
    assert(3000 == datawriter_qos.resource_limits().max_samples)
    assert(100 == datawriter_qos.resource_limits().max_instances)
    assert(500 == datawriter_qos.resource_limits().max_samples_per_instance)
    assert(50 == datawriter_qos.resource_limits().allocated_samples)
    assert(2 == datawriter_qos.resource_limits().extra_samples)

    # .transport_priority
    datawriter_qos.transport_priority().value = 10
    assert(10 == datawriter_qos.transport_priority().value)

    # .lifespan
    datawriter_qos.lifespan().duration.seconds = 10
    datawriter_qos.lifespan().duration.nanosec = 33
    assert(10 == datawriter_qos.lifespan().duration.seconds)
    assert(33 == datawriter_qos.lifespan().duration.nanosec)

    # .user_data
    datawriter_qos.user_data().push_back(0)
    datawriter_qos.user_data().push_back(1)
    datawriter_qos.user_data().push_back(2)
    datawriter_qos.user_data().push_back(3)
    count = 1
    for user_value in datawriter_qos.user_data():
        if 1 == count:
            assert(0 == user_value)
        elif 2 == count:
            assert(1 == user_value)
        elif 3 == count:
            assert(2 == user_value)
        else:
            assert(3 == user_value)
        count += 1

    # .ownership
    datawriter_qos.ownership().kind = fastdds.EXCLUSIVE_OWNERSHIP_QOS
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS == datawriter_qos.ownership().kind)

    # .ownership_strength
    datawriter_qos.ownership_strength().value = 30
    assert(30 == datawriter_qos.ownership_strength().value)

    # .writer_data_lifecycle
    datawriter_qos.writer_data_lifecycle(). \
        autodispose_unregistered_instances = False
    assert(not datawriter_qos.writer_data_lifecycle().
           autodispose_unregistered_instances)

    # .publish_mode
    datawriter_qos.publish_mode().kind = fastdds.ASYNCHRONOUS_PUBLISH_MODE
    datawriter_qos.publish_mode().flow_controller_name = 'Prueba'
    assert(fastdds.ASYNCHRONOUS_PUBLISH_MODE ==
           datawriter_qos.publish_mode().kind)
    assert('Prueba' == datawriter_qos.publish_mode().flow_controller_name)

    # .properties
    property = fastdds.Property()
    property.name('Property1')
    property.value('Value1')
    datawriter_qos.properties().properties().push_back(property)
    property = fastdds.Property()
    property.name('Property2')
    property.value('Value2')
    datawriter_qos.properties().properties().push_back(property)
    count = 1
    for prop in datawriter_qos.properties().properties():
        if 1 == count:
            assert('Property1' == prop.name())
            assert('Value1' == prop.value())
        else:
            assert('Property2' == prop.name())
            assert('Value2' == prop.value())
        count += 1

    # .reliable_writer_qos
    datawriter_qos.reliable_writer_qos().times. \
        initialHeartbeatDelay.seconds = 2
    datawriter_qos.reliable_writer_qos().times. \
        initialHeartbeatDelay.nanosec = 15
    datawriter_qos.reliable_writer_qos().times.heartbeatPeriod.seconds = 3
    datawriter_qos.reliable_writer_qos().times.heartbeatPeriod.nanosec = 16
    datawriter_qos.reliable_writer_qos().times.nackResponseDelay.seconds = 4
    datawriter_qos.reliable_writer_qos().times.nackResponseDelay.nanosec = 17
    datawriter_qos.reliable_writer_qos().times. \
        nackSupressionDuration.seconds = 5
    datawriter_qos.reliable_writer_qos().times. \
        nackSupressionDuration.nanosec = 18
    datawriter_qos.reliable_writer_qos().disable_positive_acks.enabled = True
    datawriter_qos.reliable_writer_qos(). \
        disable_positive_acks.duration.seconds = 13
    datawriter_qos.reliable_writer_qos(). \
        disable_positive_acks.duration.nanosec = 320
    datawriter_qos.reliable_writer_qos().disable_heartbeat_piggyback = True
    assert(2 == datawriter_qos.reliable_writer_qos().times.
           initialHeartbeatDelay.seconds)
    assert(15 == datawriter_qos.reliable_writer_qos().times.
           initialHeartbeatDelay.nanosec)
    assert(3 == datawriter_qos.reliable_writer_qos().times.
           heartbeatPeriod.seconds)
    assert(16 == datawriter_qos.reliable_writer_qos().times.
           heartbeatPeriod.nanosec)
    assert(4 == datawriter_qos.reliable_writer_qos().times.
           nackResponseDelay.seconds)
    assert(17 == datawriter_qos.reliable_writer_qos().times.
           nackResponseDelay.nanosec)
    assert(5 == datawriter_qos.reliable_writer_qos().times.
           nackSupressionDuration.seconds)
    assert(18 == datawriter_qos.reliable_writer_qos().times.
           nackSupressionDuration.nanosec)
    assert(13 == datawriter_qos.reliable_writer_qos().
           disable_positive_acks.duration.seconds)
    assert(320 == datawriter_qos.reliable_writer_qos().
           disable_positive_acks.duration.nanosec)
    assert(datawriter_qos.reliable_writer_qos().
           disable_heartbeat_piggyback)

    # .endpoint
    datawriter_qos.endpoint().user_defined_id = 1
    datawriter_qos.endpoint().entity_id = 2
    datawriter_qos.endpoint().history_memory_policy = \
        fastdds.PREALLOCATED_WITH_REALLOC_MEMORY_MODE
    assert(1 == datawriter_qos.endpoint().user_defined_id)
    assert(2 == datawriter_qos.endpoint().entity_id)
    assert(fastdds.PREALLOCATED_WITH_REALLOC_MEMORY_MODE ==
           datawriter_qos.endpoint().history_memory_policy)

    # .writer_resource_limits
    datawriter_qos.writer_resource_limits(). \
        matched_subscriber_allocation.initial = 30
    datawriter_qos.writer_resource_limits(). \
        matched_subscriber_allocation.maximum = 300
    datawriter_qos.writer_resource_limits(). \
        matched_subscriber_allocation.increment = 400
    assert(30 == datawriter_qos.writer_resource_limits().
           matched_subscriber_allocation.initial)
    assert(300 == datawriter_qos.writer_resource_limits().
           matched_subscriber_allocation.maximum)
    assert(400 == datawriter_qos.writer_resource_limits().
           matched_subscriber_allocation.increment)

    # .data_sharing
    datawriter_qos.data_sharing().on("/")
    datawriter_qos.data_sharing().set_max_domains(3)
    assert(fastdds.ON == datawriter_qos.data_sharing().kind())
    assert("/" == datawriter_qos.data_sharing().shm_directory())
    assert(3 == datawriter_qos.data_sharing().max_domains())
    datawriter_qos.data_sharing().clear()
    assert(fastdds.AUTO == datawriter_qos.data_sharing().kind())
    assert("" == datawriter_qos.data_sharing().shm_directory())
    assert(0 == datawriter_qos.data_sharing().max_domains())
    datawriter_qos.data_sharing().on("/")
    datawriter_qos.data_sharing().set_max_domains(3)
    assert(fastdds.ON == datawriter_qos.data_sharing().kind())
    assert("/" == datawriter_qos.data_sharing().shm_directory())
    assert(3 == datawriter_qos.data_sharing().max_domains())

    # Check agains default_datawriter_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    publisher = participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)
    assert(publisher is not None)
    publisher.set_default_datawriter_qos(datawriter_qos)

    default_datawriter_qos = fastdds.DataWriterQos()
    publisher.get_default_datawriter_qos(default_datawriter_qos)

    # Revert changes in default
    datawriter_qos = fastdds.DataWriterQos()
    publisher.set_default_datawriter_qos(datawriter_qos)

    participant.delete_publisher(publisher)
    factory.delete_participant(participant)

    # .durability
    assert(fastdds.TRANSIENT_DURABILITY_QOS ==
           default_datawriter_qos.durability().kind)

    # .durability_service
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           default_datawriter_qos.durability_service().history_kind)
    assert(10 == default_datawriter_qos.durability_service().history_depth)
    assert(5 == default_datawriter_qos.durability_service().max_samples)
    assert(20 == default_datawriter_qos.durability_service().max_instances)
    assert(30 == default_datawriter_qos.durability_service().
           max_samples_per_instance)
    assert(fastdds.Time_t.INFINITE_SECONDS == default_datawriter_qos.
           durability_service().service_cleanup_delay.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS == default_datawriter_qos.
           durability_service().service_cleanup_delay.nanosec)

    # .deadline
    assert(10 == default_datawriter_qos.deadline().period.seconds)
    assert(20 == default_datawriter_qos.deadline().period.nanosec)

    # .latency_budget
    assert(20 == default_datawriter_qos.latency_budget().duration.seconds)
    assert(30 == default_datawriter_qos.latency_budget().duration.nanosec)

    # .liveliness
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS ==
           default_datawriter_qos.liveliness().kind)
    assert(40 == default_datawriter_qos.liveliness().lease_duration.seconds)
    assert(61 == default_datawriter_qos.liveliness().lease_duration.nanosec)
    assert(30 == default_datawriter_qos.liveliness().
           announcement_period.seconds)
    assert(50 == default_datawriter_qos.liveliness().
           announcement_period.nanosec)

    # .reliability
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           default_datawriter_qos.reliability().kind)
    assert(100 == default_datawriter_qos.reliability().
           max_blocking_time.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           default_datawriter_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS ==
           default_datawriter_qos.destination_order().kind)

    # .history
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           default_datawriter_qos.history().kind)
    assert(1000 == default_datawriter_qos.history().depth)

    # .resource_limits
    assert(3000 == default_datawriter_qos.resource_limits().max_samples)
    assert(100 == default_datawriter_qos.resource_limits().max_instances)
    assert(500 == default_datawriter_qos.resource_limits().
           max_samples_per_instance)
    assert(50 == default_datawriter_qos.resource_limits().allocated_samples)
    assert(2 == default_datawriter_qos.resource_limits().extra_samples)

    # .transport_priority
    default_datawriter_qos.transport_priority().value = 10
    assert(10 == default_datawriter_qos.transport_priority().value)

    # .lifespan
    assert(10 == default_datawriter_qos.lifespan().duration.seconds)
    assert(33 == default_datawriter_qos.lifespan().duration.nanosec)

    # .user_data
    count = 1
    for user_value in default_datawriter_qos.user_data():
        if 1 == count:
            assert(0 == user_value)
        elif 2 == count:
            assert(1 == user_value)
        elif 3 == count:
            assert(2 == user_value)
        else:
            assert(3 == user_value)
        count += 1

    # .ownership
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS ==
           default_datawriter_qos.ownership().kind)

    # .ownership_strength
    assert(30 == default_datawriter_qos.ownership_strength().value)

    # .publish_mode
    assert(fastdds.ASYNCHRONOUS_PUBLISH_MODE ==
           default_datawriter_qos.publish_mode().kind)
    assert('Prueba' == default_datawriter_qos.publish_mode().
            flow_controller_name)

    # .properties
    count = 1
    for prop in default_datawriter_qos.properties().properties():
        if 1 == count:
            assert('Property1' == prop.name())
            assert('Value1' == prop.value())
        else:
            assert('Property2' == prop.name())
            assert('Value2' == prop.value())
        count += 1

    # .reliable_writer_qos
    assert(2 == default_datawriter_qos.reliable_writer_qos().times.
           initialHeartbeatDelay.seconds)
    assert(15 == default_datawriter_qos.reliable_writer_qos().times.
           initialHeartbeatDelay.nanosec)
    assert(3 == default_datawriter_qos.reliable_writer_qos().times.
           heartbeatPeriod.seconds)
    assert(16 == default_datawriter_qos.reliable_writer_qos().times.
           heartbeatPeriod.nanosec)
    assert(4 == default_datawriter_qos.reliable_writer_qos().times.
           nackResponseDelay.seconds)
    assert(17 == default_datawriter_qos.reliable_writer_qos().times.
           nackResponseDelay.nanosec)
    assert(5 == default_datawriter_qos.reliable_writer_qos().times.
           nackSupressionDuration.seconds)
    assert(18 == default_datawriter_qos.reliable_writer_qos().times.
           nackSupressionDuration.nanosec)
    assert(default_datawriter_qos.reliable_writer_qos().
           disable_positive_acks.enabled)
    assert(13 == default_datawriter_qos.reliable_writer_qos().
           disable_positive_acks.duration.seconds)
    assert(320 == default_datawriter_qos.reliable_writer_qos().
           disable_positive_acks.duration.nanosec)
    assert(default_datawriter_qos.reliable_writer_qos().
           disable_heartbeat_piggyback)

    # .endpoint
    assert(1 == default_datawriter_qos.endpoint().user_defined_id)
    assert(2 == default_datawriter_qos.endpoint().entity_id)
    assert(fastdds.PREALLOCATED_WITH_REALLOC_MEMORY_MODE ==
           default_datawriter_qos.endpoint().history_memory_policy)

    # .writer_resource_limits
    assert(30 == default_datawriter_qos.writer_resource_limits().
           matched_subscriber_allocation.initial)
    assert(300 == default_datawriter_qos.writer_resource_limits().
           matched_subscriber_allocation.maximum)
    assert(400 == default_datawriter_qos.writer_resource_limits().
           matched_subscriber_allocation.increment)

    # .data_sharing
    assert(fastdds.ON == default_datawriter_qos.data_sharing().kind())
    assert("/" == default_datawriter_qos.data_sharing().shm_directory())
    assert(3 == default_datawriter_qos.data_sharing().max_domains())


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
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           topic_qos.durability_service().history_kind)
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
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS ==
           topic_qos.liveliness().kind)
    assert(40 == topic_qos.liveliness().lease_duration.seconds)
    assert(61 == topic_qos.liveliness().lease_duration.nanosec)
    assert(30 == topic_qos.liveliness().announcement_period.seconds)
    assert(50 == topic_qos.liveliness().announcement_period.nanosec)

    # .reliability
    topic_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    topic_qos.reliability().max_blocking_time.seconds = 100
    topic_qos.reliability().max_blocking_time.nanosec = \
        fastdds.Time_t.INFINITE_NANOSECONDS
    assert(fastdds.RELIABLE_RELIABILITY_QOS == topic_qos.reliability().kind)
    assert(100 == topic_qos.reliability().max_blocking_time.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           topic_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    topic_qos.destination_order().kind = \
        fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS ==
           topic_qos.destination_order().kind)

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
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    participant.set_default_topic_qos(topic_qos)

    default_topic_qos = fastdds.TopicQos()
    participant.get_default_topic_qos(default_topic_qos)

    # Revert changes in default
    topic_qos = fastdds.TopicQos()
    participant.set_default_topic_qos(topic_qos)

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
    assert(fastdds.TRANSIENT_DURABILITY_QOS ==
           default_topic_qos.durability().kind)

    # .durability_service
    assert(fastdds.KEEP_ALL_HISTORY_QOS ==
           default_topic_qos.durability_service().history_kind)
    assert(10 == default_topic_qos.durability_service().history_depth)
    assert(5 == default_topic_qos.durability_service().max_samples)
    assert(20 == default_topic_qos.durability_service().max_instances)
    assert(30 == default_topic_qos.durability_service().
           max_samples_per_instance)

    # .deadline
    assert(10 == default_topic_qos.deadline().period.seconds)
    assert(20 == default_topic_qos.deadline().period.nanosec)

    # .latency_budget
    assert(20 == default_topic_qos.latency_budget().duration.seconds)
    assert(30 == default_topic_qos.latency_budget().duration.nanosec)

    # .liveliness
    assert(fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS ==
           default_topic_qos.liveliness().kind)
    assert(40 == default_topic_qos.liveliness().lease_duration.seconds)
    assert(61 == default_topic_qos.liveliness().lease_duration.nanosec)
    assert(30 == default_topic_qos.liveliness().announcement_period.seconds)
    assert(50 == default_topic_qos.liveliness().announcement_period.nanosec)

    # .reliability
    assert(fastdds.RELIABLE_RELIABILITY_QOS ==
           default_topic_qos.reliability().kind)
    assert(100 == default_topic_qos.reliability().max_blocking_time.seconds)
    assert(fastdds.Time_t.INFINITE_NANOSECONDS ==
           default_topic_qos.reliability().max_blocking_time.nanosec)

    # .destination_order
    assert(fastdds.BY_RECEPTION_TIMESTAMP_DESTINATIONORDER_QOS ==
           default_topic_qos.destination_order().kind)

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
    assert(fastdds.EXCLUSIVE_OWNERSHIP_QOS ==
           default_topic_qos.ownership().kind)


def test_subscriber_qos():
    # SubscriberQos
    subscriber_qos = fastdds.SubscriberQos()

    # .presentation
    subscriber_qos.presentation().access_scope = fastdds.TOPIC_PRESENTATION_QOS
    subscriber_qos.presentation().coherent_access = True
    subscriber_qos.presentation().ordered_access = True
    assert(fastdds.TOPIC_PRESENTATION_QOS ==
           subscriber_qos.presentation().access_scope)
    assert(subscriber_qos.presentation().coherent_access)
    assert(subscriber_qos.presentation().ordered_access)

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
    assert(not subscriber_qos.entity_factory().autoenable_created_entities)

    # Check agains default_subscriber_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    participant.set_default_subscriber_qos(subscriber_qos)

    default_subscriber_qos = fastdds.SubscriberQos()
    participant.get_default_subscriber_qos(default_subscriber_qos)

    # Revert changes in default
    subscriber_qos = fastdds.SubscriberQos()
    participant.set_default_subscriber_qos(subscriber_qos)

    factory.delete_participant(participant)

    # .presentation
    assert(fastdds.TOPIC_PRESENTATION_QOS ==
           default_subscriber_qos.presentation().access_scope)
    assert(default_subscriber_qos.presentation().coherent_access)
    assert(default_subscriber_qos.presentation().ordered_access)

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
    assert(not default_subscriber_qos.entity_factory().
           autoenable_created_entities)


def test_publisher_qos():
    # PublisherQos
    publisher_qos = fastdds.PublisherQos()

    # .presentation
    publisher_qos.presentation().access_scope = fastdds.TOPIC_PRESENTATION_QOS
    publisher_qos.presentation().coherent_access = True
    publisher_qos.presentation().ordered_access = True
    assert(fastdds.TOPIC_PRESENTATION_QOS ==
           publisher_qos.presentation().access_scope)
    assert(publisher_qos.presentation().coherent_access)
    assert(publisher_qos.presentation().ordered_access)

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
    assert(not publisher_qos.entity_factory().
           autoenable_created_entities)

    # Check agains default_publisher_qos
    factory = fastdds.DomainParticipantFactory.get_instance()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant is not None)
    participant.set_default_publisher_qos(publisher_qos)

    default_publisher_qos = fastdds.PublisherQos()
    participant.get_default_publisher_qos(default_publisher_qos)

    # Revert changes in default
    publisher_qos = fastdds.PublisherQos()
    participant.set_default_publisher_qos(publisher_qos)

    factory.delete_participant(participant)

    # .presentation
    assert(fastdds.TOPIC_PRESENTATION_QOS ==
           default_publisher_qos.presentation().access_scope)
    assert(default_publisher_qos.presentation().coherent_access)
    assert(default_publisher_qos.presentation().ordered_access)

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
    assert(not default_publisher_qos.entity_factory().
           autoenable_created_entities)


def test_domain_participant_qos():
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
    assert(40 == participant_qos.allocation().data_limits.
           max_datasharing_domains)
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
    assert(participant_qos.allocation().send_buffers.dynamic)
    assert(100 == participant_qos.allocation().total_readers().initial)
    assert(400 == participant_qos.allocation().total_readers().maximum)
    assert(3 == participant_qos.allocation().total_readers().increment)
    assert(100 == participant_qos.allocation().total_writers().initial)
    assert(400 == participant_qos.allocation().total_writers().maximum)
    assert(3 == participant_qos.allocation().total_writers().increment)

    # .entity_factory
    participant_qos.entity_factory().autoenable_created_entities = False
    assert(not participant_qos.entity_factory().autoenable_created_entities)

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
            assert(fastdds.FlowControllerSchedulerPolicy_ROUND_ROBIN ==
                   flow_controller.scheduler)
        else:
            assert('Flow2' == flow_controller.name)
            assert(5000 == flow_controller.max_bytes_per_period)
            assert(3000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_HIGH_PRIORITY ==
                   flow_controller.scheduler)
        count += 1

    # .name
    participant_qos.name("test name")
    assert("test name" == participant_qos.name())

    # .properties
    properties = {}
    property = fastdds.Property()
    property.name('Property1')
    property.value('Value1')
    participant_qos.properties().properties().push_back(property)
    properties[property.name()] = [property.value(), False]
    property = fastdds.Property()
    property.name('Property2')
    property.value('Value2')
    participant_qos.properties().properties().push_back(property)
    properties[property.name()] = [property.value(), False]
    for prop in participant_qos.properties().properties():
        for proper in properties:
            if prop.name() == proper and prop.value() == properties[proper][0]:
                properties[proper][1] = True

    for prop in properties:
        assert(properties[proper][1])

    # .transports
    participant_qos.transport().listen_socket_buffer_size = 10000
    participant_qos.transport().send_socket_buffer_size = 20000
    participant_qos.transport().use_builtin_transports = False
    assert(10000 == participant_qos.transport().listen_socket_buffer_size)
    assert(20000 == participant_qos.transport().send_socket_buffer_size)
    assert(not participant_qos.transport().use_builtin_transports)

    # .user_data
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
    participant_qos.wire_protocol().prefix.value = \
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    participant_qos.wire_protocol().participant_id = 32
    assert((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) ==
           participant_qos.wire_protocol().prefix.value)
    assert(32 == participant_qos.wire_protocol().participant_id)

    # # .builtin
    participant_qos.wire_protocol().builtin.use_WriterLivelinessProtocol = \
        False
    participant_qos.wire_protocol().builtin.readerHistoryMemoryPolicy = \
        fastdds.PREALLOCATED_MEMORY_MODE
    participant_qos.wire_protocol().builtin.readerPayloadSize = 3
    participant_qos.wire_protocol().builtin.writerHistoryMemoryPolicy = \
        fastdds.PREALLOCATED_MEMORY_MODE
    participant_qos.wire_protocol().builtin.writerPayloadSize = 5
    participant_qos.wire_protocol().builtin.mutation_tries = 50
    participant_qos.wire_protocol().builtin.avoid_builtin_multicast = False
    assert(not participant_qos.wire_protocol().builtin.
           use_WriterLivelinessProtocol)
    assert(fastdds.PREALLOCATED_MEMORY_MODE ==
           participant_qos.wire_protocol().builtin.readerHistoryMemoryPolicy)
    assert(3 == participant_qos.wire_protocol().builtin.readerPayloadSize)
    assert(fastdds.PREALLOCATED_MEMORY_MODE ==
           participant_qos.wire_protocol().builtin.writerHistoryMemoryPolicy)
    assert(5 == participant_qos.wire_protocol().builtin.writerPayloadSize)
    assert(50 == participant_qos.wire_protocol().builtin.mutation_tries)
    assert(not participant_qos.wire_protocol().builtin.avoid_builtin_multicast)
    # ## .discovery_config
    participant_qos.wire_protocol().builtin.discovery_config. \
        use_SIMPLE_EndpointDiscoveryProtocol = False
    participant_qos.wire_protocol().builtin.discovery_config. \
        use_STATIC_EndpointDiscoveryProtocol = True
    participant_qos.wire_protocol().builtin.discovery_config. \
        leaseDuration.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config. \
        leaseDuration.nanosec = 10
    participant_qos.wire_protocol().builtin.discovery_config. \
        leaseDuration_announcementperiod.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config. \
        leaseDuration_announcementperiod.nanosec = 10
    participant_qos.wire_protocol().builtin.discovery_config. \
        initial_announcements.count = 10
    participant_qos.wire_protocol().builtin.discovery_config. \
        initial_announcements.period.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config. \
        initial_announcements.period.nanosec = 10
    participant_qos.wire_protocol().builtin.discovery_config. \
        m_simpleEDP. use_PublicationWriterANDSubscriptionReader = False
    participant_qos.wire_protocol().builtin.discovery_config. \
        m_simpleEDP.use_PublicationReaderANDSubscriptionWriter = False
    found_secure_member = False
    members = inspect.getmembers(participant_qos.wire_protocol().
                                 builtin.discovery_config.m_simpleEDP)
    cstr = 'enable_builtin_secure_publications_writer_and_subscriptions_reader'
    for m in members:
        if cstr == m[0]:
            found_secure_member = True
            break
    if found_secure_member:
        participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP. \
            enable_builtin_secure_publications_writer_and_subscriptions_reader\
            = False
        participant_qos.wire_protocol().builtin.discovery_config.m_simpleEDP. \
            enable_builtin_secure_subscriptions_writer_and_publications_reader\
            = False
    participant_qos.wire_protocol().builtin.discovery_config. \
        discoveryServer_client_syncperiod.seconds = 30
    participant_qos.wire_protocol().builtin.discovery_config. \
        discoveryServer_client_syncperiod.nanosec = 10
    participant_qos.wire_protocol().builtin.discovery_config. \
        discoveryServer_client_syncperiod.nanosec = 10
    server_info = fastdds.RemoteServerAttributes()
    server_info.guidPrefix.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,  12)
    locator = fastdds.Locator_t()
    locator.address = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 1)
    locator.port = 7400
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    server_info.metatrafficMulticastLocatorList.push_back(locator)
    server_info.metatrafficUnicastLocatorList.push_back(locator)
    participant_qos.wire_protocol().builtin.discovery_config. \
        m_DiscoveryServers.push_back(server_info)
    participant_qos.wire_protocol().builtin.discovery_config. \
        ignoreParticipantFlags = fastdds.FILTER_DIFFERENT_HOST
    assert(not participant_qos.wire_protocol().builtin.discovery_config.
           use_SIMPLE_EndpointDiscoveryProtocol)
    assert(participant_qos.wire_protocol().builtin.discovery_config.
           use_STATIC_EndpointDiscoveryProtocol)
    assert(30 == participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration.nanosec)
    assert(30 == participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration_announcementperiod.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration_announcementperiod.nanosec)
    assert(10 == participant_qos.wire_protocol().builtin.
           discovery_config.initial_announcements.count)
    assert(30 == participant_qos.wire_protocol().builtin.
           discovery_config.initial_announcements.period.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.
           discovery_config.initial_announcements.period.nanosec)
    assert(not participant_qos.wire_protocol().builtin.discovery_config.
           m_simpleEDP. use_PublicationWriterANDSubscriptionReader)
    assert(not participant_qos.wire_protocol().builtin.discovery_config.
           m_simpleEDP.use_PublicationReaderANDSubscriptionWriter)
    if found_secure_member:
        assert(not participant_qos.wire_protocol().builtin.discovery_config.
               m_simpleEDP.
               enable_builtin_secure_publications_writer_and_subscriptions_reader)
        assert(not participant_qos.wire_protocol().builtin.discovery_config.
               m_simpleEDP.
               enable_builtin_secure_subscriptions_writer_and_publications_reader)
    assert(30 == participant_qos.wire_protocol().builtin.discovery_config.
           discoveryServer_client_syncperiod.seconds)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.
           discoveryServer_client_syncperiod.nanosec)
    assert(10 == participant_qos.wire_protocol().builtin.discovery_config.
           discoveryServer_client_syncperiod.nanosec)
    server_info = participant_qos.wire_protocol().builtin.discovery_config. \
        m_DiscoveryServers[0]
    assert((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) ==
           server_info.guidPrefix.value)
    locator = server_info.metatrafficMulticastLocatorList[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 1) ==
           locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    locator = server_info.metatrafficUnicastLocatorList[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 1) ==
           locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    assert(fastdds.FILTER_DIFFERENT_HOST == participant_qos.
           wire_protocol().builtin.discovery_config.ignoreParticipantFlags)
    # ## .metatrafficUnicastLocatorList;
    locator = fastdds.Locator_t()
    locator.address = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 2)
    locator.port = 7401
    locator.kind = fastdds.LOCATOR_KIND_TCPv4
    participant_qos.wire_protocol().builtin. \
        metatrafficUnicastLocatorList.push_back(locator)
    locator = participant_qos.wire_protocol().builtin. \
        metatrafficUnicastLocatorList[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 2) ==
           locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    # ## .metatrafficMulticastLocatorList;
    locator = fastdds.Locator_t()
    locator.address = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 233, 0, 9)
    locator.port = 7411
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    participant_qos.wire_protocol().builtin. \
        metatrafficMulticastLocatorList.push_back(locator)
    locator = participant_qos.wire_protocol().builtin. \
        metatrafficMulticastLocatorList[0]
    assert((1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 233, 0, 9) ==
           locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    # ## .initialPeersList;
    locator = fastdds.Locator_t()
    locator.address = (1, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 0, 0, 1)
    locator.port = 1024
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    participant_qos.wire_protocol().builtin.initialPeersList.push_back(locator)
    locator = participant_qos.wire_protocol().builtin.initialPeersList[0]
    assert((1, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 0, 0, 1) ==
           locator.address)
    assert(1024 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    # # .default_multicast_locator_list
    locator = fastdds.Locator_t()
    locator.address = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 233, 0, 9)
    locator.port = 7411
    locator.kind = fastdds.LOCATOR_KIND_UDPv4
    participant_qos.wire_protocol().default_multicast_locator_list. \
        push_back(locator)
    locator = participant_qos.wire_protocol().default_multicast_locator_list[0]
    assert((1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 233, 0, 9) ==
           locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    # # .default_unicast_locator_list
    locator = fastdds.Locator_t()
    locator.address = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 2)
    locator.port = 7401
    locator.kind = fastdds.LOCATOR_KIND_TCPv4
    participant_qos.wire_protocol().default_unicast_locator_list. \
        push_back(locator)
    locator = participant_qos.wire_protocol().default_unicast_locator_list[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 2) ==
           locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    # # .port
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

    # Revert changes in default
    participant_qos = fastdds.DomainParticipantQos()
    factory.set_default_participant_qos(participant_qos)

    # .allocation
    assert(10 == default_participant_qos.allocation().
           data_limits.max_properties)
    assert(20 == default_participant_qos.allocation().
           data_limits.max_user_data)
    assert(30 == default_participant_qos.allocation().
           data_limits.max_partitions)
    assert(40 == default_participant_qos.allocation().
           data_limits.max_datasharing_domains)
    assert(10 == default_participant_qos.allocation().locators.
           max_unicast_locators)
    assert(20 == default_participant_qos.allocation().locators.
           max_multicast_locators)
    assert(10 == default_participant_qos.allocation().participants.initial)
    assert(20 == default_participant_qos.allocation().participants.maximum)
    assert(3 == default_participant_qos.allocation().participants.increment)
    assert(10 == default_participant_qos.allocation().writers.initial)
    assert(20 == default_participant_qos.allocation().writers.maximum)
    assert(3 == default_participant_qos.allocation().writers.increment)
    assert(10 == default_participant_qos.allocation().readers.initial)
    assert(20 == default_participant_qos.allocation().readers.maximum)
    assert(3 == default_participant_qos.allocation().readers.increment)
    assert(10 == default_participant_qos.allocation().send_buffers.
           preallocated_number)
    assert(default_participant_qos.allocation().send_buffers.dynamic)
    assert(100 == default_participant_qos.allocation().total_readers().initial)
    assert(400 == default_participant_qos.allocation().total_readers().maximum)
    assert(3 == default_participant_qos.allocation().total_readers().increment)
    assert(100 == default_participant_qos.allocation().total_writers().initial)
    assert(400 == default_participant_qos.allocation().total_writers().maximum)
    assert(3 == default_participant_qos.allocation().total_writers().increment)

    # .entity_factory
    assert(not default_participant_qos.entity_factory().
           autoenable_created_entities)

    # .flow_controllers
    count = 1
    for flow_controller in default_participant_qos.flow_controllers():
        if 1 == count:
            assert('Flow1' == flow_controller.name)
            assert(3000 == flow_controller.max_bytes_per_period)
            assert(5000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_ROUND_ROBIN ==
                   flow_controller.scheduler)
        else:
            assert('Flow2' == flow_controller.name)
            assert(5000 == flow_controller.max_bytes_per_period)
            assert(3000 == flow_controller.period_ms)
            assert(fastdds.FlowControllerSchedulerPolicy_HIGH_PRIORITY ==
                   flow_controller.scheduler)
        count += 1

    # .name
    assert("test name" == default_participant_qos.name())

    # .properties
    for prop in properties:
        properties[proper][1] = False

    for prop in default_participant_qos.properties().properties():
        for proper in properties:
            if prop.name() == proper and prop.value() == properties[proper][0]:
                properties[proper][1] = True

    for prop in properties:
        assert(properties[proper][1])

    # .transports
    assert(10000 == default_participant_qos.transport().
           listen_socket_buffer_size)
    assert(20000 == default_participant_qos.transport().
           send_socket_buffer_size)
    assert(not default_participant_qos.transport().use_builtin_transports)

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
    assert((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) ==
           default_participant_qos.wire_protocol().prefix.value)
    assert(32 == default_participant_qos.wire_protocol().participant_id)
    # # .builtin
    assert(not default_participant_qos.wire_protocol().builtin.
           use_WriterLivelinessProtocol)
    assert(fastdds.PREALLOCATED_MEMORY_MODE == default_participant_qos.
           wire_protocol().builtin.readerHistoryMemoryPolicy)
    assert(3 == default_participant_qos.wire_protocol().builtin.
           readerPayloadSize)
    assert(fastdds.PREALLOCATED_MEMORY_MODE == default_participant_qos.
           wire_protocol().builtin.writerHistoryMemoryPolicy)
    assert(5 == default_participant_qos.wire_protocol().builtin.
           writerPayloadSize)
    assert(50 == default_participant_qos.wire_protocol().builtin.
           mutation_tries)
    assert(not default_participant_qos.wire_protocol().builtin.
           avoid_builtin_multicast)
    # ## .discovery_config
    assert(not default_participant_qos.wire_protocol().builtin.
           discovery_config.use_SIMPLE_EndpointDiscoveryProtocol)
    assert(default_participant_qos.wire_protocol().builtin.
           discovery_config.use_STATIC_EndpointDiscoveryProtocol)
    assert(30 == default_participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration.nanosec)
    assert(30 == default_participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration_announcementperiod.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.
           discovery_config.leaseDuration_announcementperiod.nanosec)
    assert(10 == default_participant_qos.wire_protocol().builtin.
           discovery_config.initial_announcements.count)
    assert(30 == default_participant_qos.wire_protocol().builtin.
           discovery_config.initial_announcements.period.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.
           discovery_config.initial_announcements.period.nanosec)
    assert(not default_participant_qos.wire_protocol().builtin.
           discovery_config.m_simpleEDP.
           use_PublicationWriterANDSubscriptionReader)
    assert(not default_participant_qos.wire_protocol().builtin.
           discovery_config.m_simpleEDP.
           use_PublicationReaderANDSubscriptionWriter)
    if found_secure_member:
        assert(not default_participant_qos.wire_protocol().builtin.
               discovery_config.m_simpleEDP.
               enable_builtin_secure_publications_writer_and_subscriptions_reader)
        assert(not default_participant_qos.wire_protocol().builtin.
               discovery_config.m_simpleEDP.
               enable_builtin_secure_subscriptions_writer_and_publications_reader)
    assert(30 == default_participant_qos.wire_protocol().builtin.
           discovery_config.discoveryServer_client_syncperiod.seconds)
    assert(10 == default_participant_qos.wire_protocol().builtin.
           discovery_config.discoveryServer_client_syncperiod.nanosec)
    assert(10 == default_participant_qos.wire_protocol().builtin.
           discovery_config.discoveryServer_client_syncperiod.nanosec)
    server_info = default_participant_qos.wire_protocol().builtin. \
        discovery_config.m_DiscoveryServers[0]
    assert((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) ==
           server_info.guidPrefix.value)
    locator = server_info.metatrafficMulticastLocatorList[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 1) ==
           locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    locator = server_info.metatrafficUnicastLocatorList[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 1) ==
           locator.address)
    assert(7400 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    assert(fastdds.FILTER_DIFFERENT_HOST == default_participant_qos.
           wire_protocol().builtin.discovery_config.ignoreParticipantFlags)
    # ## .metatrafficUnicastLocatorList;
    locator = default_participant_qos.wire_protocol().builtin. \
        metatrafficUnicastLocatorList[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 2) ==
           locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    # ## .metatrafficMulticastLocatorList;
    locator = default_participant_qos.wire_protocol().builtin. \
        metatrafficMulticastLocatorList[0]
    assert((1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 233, 0, 9) ==
           locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    # ## .initialPeersList;
    locator = default_participant_qos.wire_protocol(). \
        builtin.initialPeersList[0]
    assert((1, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 0, 0, 1) ==
           locator.address)
    assert(1024 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    # # .default_multicast_locator_list
    locator = default_participant_qos.wire_protocol(). \
        default_multicast_locator_list[0]
    assert((1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 233, 0, 9) ==
           locator.address)
    assert(7411 == locator.port)
    assert(fastdds.LOCATOR_KIND_UDPv4 == locator.kind)
    # # .default_unicast_locator_list
    locator = default_participant_qos.wire_protocol(). \
        default_unicast_locator_list[0]
    assert((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 168, 1, 2) ==
           locator.address)
    assert(7401 == locator.port)
    assert(fastdds.LOCATOR_KIND_TCPv4 == locator.kind)
    # # .port
    assert(7410 == default_participant_qos.wire_protocol().port.portBase)
    assert(200 == default_participant_qos.wire_protocol().port.domainIDGain)
    assert(3 == default_participant_qos.wire_protocol().port.participantIDGain)
    assert(1 == default_participant_qos.wire_protocol().port.offsetd0)
    assert(11 == default_participant_qos.wire_protocol().port.offsetd1)
    assert(21 == default_participant_qos.wire_protocol().port.offsetd2)
    assert(22 == default_participant_qos.wire_protocol().port.offsetd3)


def test_domain_participant_factory_qos():
    factory = fastdds.DomainParticipantFactory.get_instance()
    factory_qos = fastdds.DomainParticipantFactoryQos()

    factory_qos.entity_factory().autoenable_created_entities = False
    assert(not factory_qos.entity_factory().autoenable_created_entities)

    factory.set_qos(factory_qos)
    default_factory_qos = fastdds.DomainParticipantFactoryQos()
    factory.get_qos(default_factory_qos)
    # Revert changes in default
    factory_qos = fastdds.DomainParticipantFactoryQos()
    factory.set_qos(factory_qos)


    assert(not default_factory_qos.entity_factory().
           autoenable_created_entities)
    default_factory_qos = fastdds.DomainParticipantFactoryQos()


def test_replier_qos():
    replier_qos = fastdds.ReplierQos()

    replier_qos.service_name = "service_name"
    assert("service_name" == replier_qos.service_name)

    replier_qos.request_type = "request_type"
    assert("request_type" == replier_qos.request_type)

    replier_qos.reply_type = "reply_type"
    assert("reply_type" == replier_qos.reply_type)

    replier_qos.request_topic_name = "request_topic_name"
    assert("request_topic_name" == replier_qos.request_topic_name)

    replier_qos.reply_topic_name = "reply_topic_name"
    assert("reply_topic_name" == replier_qos.reply_topic_name)

    replier_qos.writer_qos = fastdds.DATAWRITER_QOS_DEFAULT
    assert(fastdds.DATAWRITER_QOS_DEFAULT == replier_qos.writer_qos)

    replier_qos.reader_qos = fastdds.DATAREADER_QOS_DEFAULT
    assert(fastdds.DATAREADER_QOS_DEFAULT == replier_qos.reader_qos)


def test_requester_qos():
    requester_qos = fastdds.RequesterQos()

    requester_qos.service_name = "service_name"
    assert("service_name" == requester_qos.service_name)

    requester_qos.request_type = "request_type"
    assert("request_type" == requester_qos.request_type)

    requester_qos.reply_type = "reply_type"
    assert("reply_type" == requester_qos.reply_type)

    requester_qos.request_topic_name = "request_topic_name"
    assert("request_topic_name" == requester_qos.request_topic_name)

    requester_qos.reply_topic_name = "reply_topic_name"
    assert("reply_topic_name" == requester_qos.reply_topic_name)

    requester_qos.writer_qos = fastdds.DATAWRITER_QOS_DEFAULT
    assert(fastdds.DATAWRITER_QOS_DEFAULT == requester_qos.writer_qos)

    requester_qos.reader_qos = fastdds.DATAREADER_QOS_DEFAULT
    assert(fastdds.DATAREADER_QOS_DEFAULT == requester_qos.reader_qos)
