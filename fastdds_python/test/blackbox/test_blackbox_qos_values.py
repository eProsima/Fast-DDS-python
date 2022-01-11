# Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase

import fastdds

class TestQosValues(TestCase):

    def test_participant_factory_qos_values(self):
        qos = fastdds.DomainParticipantFactoryQos()

        # Entity Factory Qos, implemented in the library
        qos.entity_factory().autoenable_created_entities = False
        self.assertEqual(qos.entity_factory().autoenable_created_entities, False)

    def test_participant_qos_values(self):
        qos = fastdds.DomainParticipantQos()

        '''
        # User Data Qos, implemented in the library.
        qos.user_data().set_max_size(10)
        data = fastdds.OctetResourceLimitedVector()
        data.push_back(1)
        data.push_back(2)
        qos.user_data().setValue(data)
        self.assertEqual(qos.user_data().dataVec(), data)
        
        #set_max_size
        #resize
        #dataVec
        #dataVec(val)
        #getValue
        #setValue(val)
        '''

        # Entity Factory Qos, implemented in the library
        qos.entity_factory().autoenable_created_entities = False
        self.assertEqual(qos.entity_factory().autoenable_created_entities, False)

        # Participant allocation limits
        qos.allocation().locators.max_unicast_locators = 10
        qos.allocation().locators.max_multicast_locators = 15

        qos.allocation().participants.initial = 10
        qos.allocation().participants.maximum = 20
        qos.allocation().participants.increment = 5

        qos.allocation().readers.initial = 10
        qos.allocation().readers.maximum = 20
        qos.allocation().readers.increment = 5

        qos.allocation().writers.initial = 10
        qos.allocation().writers.maximum = 20
        qos.allocation().writers.increment = 5

        qos.allocation().send_buffers.preallocated_number = 10
        qos.allocation().send_buffers.dynamic = True

        qos.allocation().data_limits.max_properties = 10
        qos.allocation().data_limits.max_user_data = 20
        qos.allocation().data_limits.max_partitions = 30
        qos.allocation().data_limits.max_datasharing_domains = 40

        self.assertEqual(qos.allocation().locators.max_unicast_locators, 10)
        self.assertEqual(qos.allocation().locators.max_multicast_locators, 15)

        self.assertEqual(qos.allocation().participants.initial, 10)
        self.assertEqual(qos.allocation().participants.maximum, 20)
        self.assertEqual(qos.allocation().participants.increment, 5)

        self.assertEqual(qos.allocation().readers.initial, 10)
        self.assertEqual(qos.allocation().readers.maximum, 20)
        self.assertEqual(qos.allocation().readers.increment, 5)

        self.assertEqual(qos.allocation().writers.initial, 10)
        self.assertEqual(qos.allocation().writers.maximum, 20)
        self.assertEqual(qos.allocation().writers.increment, 5)

        self.assertEqual(qos.allocation().send_buffers.preallocated_number, 10)
        self.assertEqual(qos.allocation().send_buffers.dynamic, True)

        self.assertEqual(qos.allocation().data_limits.max_properties, 10)
        self.assertEqual(qos.allocation().data_limits.max_user_data, 20)
        self.assertEqual(qos.allocation().data_limits.max_partitions, 30)
        self.assertEqual(qos.allocation().data_limits.max_datasharing_domains, 40)

        rlaa = fastdds.RemoteLocatorsAllocationAttributes()
        rlaa.max_unicast_locators = 10
        rlaa.max_multicast_locators = 15
        self.assertEqual(qos.allocation().locators, rlaa)

        rlcc = fastdds.ResourceLimitedContainerConfig()
        rlcc.initial = 10
        rlcc.maximum = 20
        rlcc.increment = 5
        self.assertEqual(qos.allocation().participants, rlcc)
        self.assertEqual(qos.allocation().readers, rlcc)
        self.assertEqual(qos.allocation().writers, rlcc)
        
        sbaa = fastdds.SendBuffersAllocationAttributes()
        sbaa.preallocated_number = 10
        sbaa.dynamic = True
        self.assertEqual(qos.allocation().send_buffers, sbaa)
        
        vldl = fastdds.VariableLengthDataLimits()
        vldl.max_properties = 10
        vldl.max_user_data = 20
        vldl.max_partitions = 30
        vldl.max_datasharing_domains = 40
        self.assertEqual(qos.allocation().data_limits, vldl)


        # Property policies
        pp = fastdds.Property()
        pp.name("Key")
        pp.value("value")
        qos.properties().properties().push_back(pp)
        self.assertEqual(qos.properties().properties().size(), 1)
        self.assertEqual(qos.properties().properties()[0].name(), "Key")
        self.assertEqual(qos.properties().properties()[0].value(), "value")

        '''
        bp = fastdds.BinaryProperty()
        bp.name("Key")
        bp.value().push_back(0)
        bp.value().push_back(1)
        qos.properties().binary_properties().push_back(bp)
        self.assertEqual(qos.properties().binary_properties().size(), 1)
        self.assertEqual(qos.properties().binary_properties()[0].name(), "Key")
        self.assertEqual(qos.properties().binary_properties()[0].value().size(), 2)
        self.assertEqual(qos.properties().binary_properties()[0].value()[0], 0)
        self.assertEqual(qos.properties().binary_properties()[0].value()[1], 1)
        '''

        # Wire Protocol options

        loc = fastdds.Locator_t()
        loc.kind = fastdds.LOCATOR_KIND_TCPv4
        loc.port = 1004
        #loc.address = octet[16]

        '''
        # Array members are treated as opaque pointers, and cannot acess the elements
        # Suposedly you should be able with typemaps, but it didn't work
        qos.wire_protocol().prefix.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertEqual(qos.wire_protocol().prefix.value, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        '''
        qos.wire_protocol().participant_id = 10
        self.assertEqual(qos.wire_protocol().participant_id, 10)

        qos.wire_protocol().builtin.discovery_config.discoveryProtocol = fastdds.CLIENT
        qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol = False
        qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol = True
        qos.wire_protocol().builtin.discovery_config.leaseDuration = fastdds.Time_t(5, 100)
        qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod = fastdds.Time_t(10, 500)
        qos.wire_protocol().builtin.discovery_config.initial_announcements.count = 100
        qos.wire_protocol().builtin.discovery_config.initial_announcements.period = fastdds.Time_t(10, 500)
        qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationWriterANDSubscriptionReader = False
        qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationReaderANDSubscriptionWriter = False
        qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod = fastdds.Time_t(15, 700)
        qos.wire_protocol().builtin.discovery_config.ignoreParticipantFlags = fastdds.FILTER_DIFFERENT_HOST
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.discoveryProtocol, fastdds.CLIENT)
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol, False)
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol, True)
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.leaseDuration, fastdds.Time_t(5, 100))
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod, fastdds.Time_t(10, 500))
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.initial_announcements.count, 100)
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.initial_announcements.period, fastdds.Time_t(10, 500))
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationWriterANDSubscriptionReader, False)
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.m_simpleEDP.use_PublicationReaderANDSubscriptionWriter, False)
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.discoveryServer_client_syncperiod, fastdds.Time_t(15, 700))
        self.assertEqual(qos.wire_protocol().builtin.discovery_config.ignoreParticipantFlags, fastdds.FILTER_DIFFERENT_HOST)

        qos.wire_protocol().builtin.use_WriterLivelinessProtocol = False
        self.assertEqual(qos.wire_protocol().builtin.use_WriterLivelinessProtocol, False)

        qos.wire_protocol().builtin.typelookup_config.use_client = True
        qos.wire_protocol().builtin.typelookup_config.use_server = True
        self.assertEqual(qos.wire_protocol().builtin.typelookup_config.use_client, True)
        self.assertEqual(qos.wire_protocol().builtin.typelookup_config.use_server, True)

        qos.wire_protocol().builtin.metatrafficUnicastLocatorList.push_back(loc)
        qos.wire_protocol().builtin.metatrafficMulticastLocatorList.push_back(loc)
        qos.wire_protocol().builtin.initialPeersList.push_back(loc)

        self.assertEqual(qos.wire_protocol().builtin.metatrafficUnicastLocatorList.size(), 1)
        self.assertEqual(qos.wire_protocol().builtin.metatrafficMulticastLocatorList.size(), 1)
        self.assertEqual(qos.wire_protocol().builtin.initialPeersList.size(), 1)
        # SWIG does not wrap the iterator idiom, so we cannot check the values

        qos.wire_protocol().builtin.metatrafficUnicastLocatorList.erase(loc)
        qos.wire_protocol().builtin.metatrafficMulticastLocatorList.erase(loc)
        qos.wire_protocol().builtin.initialPeersList.erase(loc)
        self.assertEqual(qos.wire_protocol().builtin.metatrafficUnicastLocatorList.size(), 0)
        self.assertEqual(qos.wire_protocol().builtin.metatrafficMulticastLocatorList.size(), 0)
        self.assertEqual(qos.wire_protocol().builtin.initialPeersList.size(), 0)

        qos.wire_protocol().builtin.readerHistoryMemoryPolicy = fastdds.DYNAMIC_REUSABLE_MEMORY_MODE
        qos.wire_protocol().builtin.readerPayloadSize = 1
        qos.wire_protocol().builtin.writerHistoryMemoryPolicy = fastdds.DYNAMIC_RESERVE_MEMORY_MODE
        qos.wire_protocol().builtin.writerPayloadSize = 10
        qos.wire_protocol().builtin.mutation_tries = 20
        qos.wire_protocol().builtin.avoid_builtin_multicast = False
        self.assertEqual(qos.wire_protocol().builtin.readerHistoryMemoryPolicy, fastdds.DYNAMIC_REUSABLE_MEMORY_MODE)
        self.assertEqual(qos.wire_protocol().builtin.readerPayloadSize, 1)
        self.assertEqual(qos.wire_protocol().builtin.writerHistoryMemoryPolicy, fastdds.DYNAMIC_RESERVE_MEMORY_MODE)
        self.assertEqual(qos.wire_protocol().builtin.writerPayloadSize, 10)
        self.assertEqual(qos.wire_protocol().builtin.mutation_tries, 20)
        self.assertEqual(qos.wire_protocol().builtin.avoid_builtin_multicast, False)

        qos.wire_protocol().port.portBase = 10
        qos.wire_protocol().port.domainIDGain = 20
        qos.wire_protocol().port.participantIDGain = 30
        qos.wire_protocol().port.offsetd0 = 40
        qos.wire_protocol().port.offsetd1 = 50
        qos.wire_protocol().port.offsetd2 = 60
        qos.wire_protocol().port.offsetd3 = 70
        self.assertEqual(qos.wire_protocol().port.portBase, 10)
        self.assertEqual(qos.wire_protocol().port.domainIDGain, 20)
        self.assertEqual(qos.wire_protocol().port.participantIDGain, 30)
        self.assertEqual(qos.wire_protocol().port.offsetd0, 40)
        self.assertEqual(qos.wire_protocol().port.offsetd1, 50)
        self.assertEqual(qos.wire_protocol().port.offsetd2, 60)
        self.assertEqual(qos.wire_protocol().port.offsetd3, 70)

        qos.wire_protocol().throughput_controller.bytesPerPeriod = 10
        qos.wire_protocol().throughput_controller.periodMillisecs = 20
        self.assertEqual(qos.wire_protocol().throughput_controller.bytesPerPeriod, 10)
        self.assertEqual(qos.wire_protocol().throughput_controller.periodMillisecs, 20)

        qos.wire_protocol().default_unicast_locator_list.push_back(loc)
        qos.wire_protocol().default_multicast_locator_list.push_back(loc)
        self.assertEqual(qos.wire_protocol().default_unicast_locator_list.size(), 1)
        self.assertEqual(qos.wire_protocol().default_multicast_locator_list.size(), 1)
        # SWIG does not wrap the iterator idiom, so we cannot check the values

        qos.wire_protocol().default_unicast_locator_list.erase(loc)
        qos.wire_protocol().default_multicast_locator_list.erase(loc)
        self.assertEqual(qos.wire_protocol().default_unicast_locator_list.size(), 0)
        self.assertEqual(qos.wire_protocol().default_multicast_locator_list.size(), 0)

        # Transport options
        qos.transport().use_builtin_transports = False
        qos.transport().send_socket_buffer_size = 10
        qos.transport().listen_socket_buffer_size = 15

        self.assertEqual(qos.transport().use_builtin_transports, False)
        self.assertEqual(qos.transport().send_socket_buffer_size, 10)
        self.assertEqual(qos.transport().listen_socket_buffer_size, 15)

        '''
        t = fastdds.UDPv4TransportDescriptor()
        t.non_blocking_send = True
        t.sendBufferSize = 2048
        t.receiveBufferSize = 2048
        qos.transport().user_transports.push_back(t)

        self.assertEqual(qos.transport().user_transports.size(), 1)
        self.assertEqual(qos.transport().user_transports[0], t)
        '''


    def test_topic_qos_values(self):
        qos = fastdds.TopicQos()

       

        '''
        # Topic Data Qos, implemented in the library.
        qos.topic_data_().set_max_size(10)
        data = fastdds.OctetResourceLimitedVector()
        data.push_back(1)
        data.push_back(2)
        qos.topic_data_().setValue(data)
        self.assertEqual(qos.topic_data_().dataVec(), data)
        
        #set_max_size
        #resize
        #dataVec
        #dataVec(val)
        #getValue
        #setValue(val)
        '''

        # Durability Qos, implemented in the library.
        qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
        self.assertEqual(qos.durability().kind, fastdds.TRANSIENT_LOCAL_DURABILITY_QOS)

        qos.durability().durabilityKind(fastdds.TRANSIENT)
        self.assertEqual(qos.durability().durabilityKind(), fastdds.TRANSIENT)
        # Durability Service Qos (Extension).
        qos.durability_service().service_cleanup_delay = fastdds.Time_t(5, 100)
        qos.durability_service().history_kind = fastdds.KEEP_ALL_HISTORY_QOS
        qos.durability_service().history_depth = 10
        qos.durability_service().max_samples = 20
        qos.durability_service().max_instances = 30
        qos.durability_service().max_samples_per_instance = 40
        self.assertEqual(qos.durability_service().service_cleanup_delay, fastdds.Time_t(5, 100))
        self.assertEqual(qos.durability_service().history_kind, fastdds.KEEP_ALL_HISTORY_QOS)
        self.assertEqual(qos.durability_service().history_depth, 10)
        self.assertEqual(qos.durability_service().max_samples, 20)
        self.assertEqual(qos.durability_service().max_instances, 30)
        self.assertEqual(qos.durability_service().max_samples_per_instance, 40)

        # Deadline Qos, implemented in the library.
        qos.deadline().period = fastdds.Time_t(5, 100)
        self.assertEqual(qos.deadline().period, fastdds.Time_t(5, 100))

        # Latency Budget Qos, implemented in the library.
        qos.latency_budget().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.latency_budget().duration, fastdds.Time_t(5, 100))

        # Liveliness Qos, implemented in the library.
        qos.liveliness().kind = fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
        qos.liveliness().lease_duration = fastdds.Time_t(5, 100)
        qos.liveliness().announcement_period = fastdds.Time_t(5, 100)
        self.assertEqual(qos.liveliness().kind, fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS)
        self.assertEqual(qos.liveliness().lease_duration, fastdds.Time_t(5, 100))
        self.assertEqual(qos.liveliness().announcement_period, fastdds.Time_t(5, 100))

        # Reliability Qos, implemented in the library.
        qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
        qos.reliability().max_blocking_time = fastdds.Time_t(5, 100)
        self.assertEqual(qos.reliability().kind, fastdds.RELIABLE_RELIABILITY_QOS)
        self.assertEqual(qos.reliability().max_blocking_time, fastdds.Time_t(5, 100))

        # Destination Order Qos, NOT implemented in the library.
        qos.destination_order().kind = fastdds.BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS
        self.assertEqual(qos.destination_order().kind, fastdds.BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS)

        # History Qos, implemented in the library.
        qos.history().kind = fastdds.KEEP_ALL_HISTORY_QOS
        qos.history().depth = 55
        self.assertEqual(qos.history().kind, fastdds.KEEP_ALL_HISTORY_QOS)
        self.assertEqual(qos.history().depth, 55)

        # Resource Limits Qos, implemented in the library.
        qos.resource_limits().max_samples = 5
        qos.resource_limits().max_instances = 10
        qos.resource_limits().max_samples_per_instance = 15
        qos.resource_limits().allocated_samples = 20
        qos.resource_limits().extra_samples = 25
        self.assertEqual(qos.resource_limits().max_samples, 5)
        self.assertEqual(qos.resource_limits().max_instances, 10)
        self.assertEqual(qos.resource_limits().max_samples_per_instance, 15)
        self.assertEqual(qos.resource_limits().allocated_samples, 20)
        self.assertEqual(qos.resource_limits().extra_samples, 25)

        # Transport Priority Qos, NOT implemented in the library.
        qos.transport_priority().value = 10
        self.assertEqual(qos.transport_priority().value, 10)

        # Lifespan Qos (Extension).
        qos.lifespan().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.lifespan().duration, fastdds.Time_t(5, 100))

        # Ownership Qos, implemented in the library.
        qos.ownership().kind = fastdds.EXCLUSIVE_OWNERSHIP_QOS
        self.assertEqual(qos.ownership().kind, fastdds.EXCLUSIVE_OWNERSHIP_QOS)

        # Data Representation Qos, implemented in the library.
        qos.representation().m_value.push_back(fastdds.XML_DATA_REPRESENTATION)
        self.assertEqual(qos.representation().m_value[0], fastdds.XML_DATA_REPRESENTATION)

    def test_publisher_qos_values(self):
        qos = fastdds.PublisherQos()

        # Presentation Qos, NOT implemented in the library.
        qos.presentation().access_scope = fastdds.GROUP_PRESENTATION_QOS
        qos.presentation().coherent_access = True
        qos.presentation().ordered_access = True

        self.assertEqual(qos.presentation().access_scope, fastdds.GROUP_PRESENTATION_QOS)
        self.assertEqual(qos.presentation().coherent_access, True)
        self.assertEqual(qos.presentation().ordered_access, True)

        # Partition Qos, implemented in the library.
        qos.partition().push_back("partition1")
        qos.partition().push_back("partition2")
        self.assertEqual(qos.partition().size(), 2)
        partitions = qos.partition().names()
        self.assertEqual(partitions[0], "partition1")
        self.assertEqual(partitions[1], "partition2")

        '''
        # Group Data Qos, implemented in the library.
        qos.group_data().set_max_size(10)
        data = fastdds.OctetResourceLimitedVector()
        data.push_back(1)
        data.push_back(2)
        qos.group_data().setValue(data)
        self.assertEqual(qos.group_data().dataVec(), data)
        
        #set_max_size
        #resize
        #dataVec
        #dataVec(val)
        #getValue
        #setValue(val)
        '''

        # Entity Factory Qos, implemented in the library
        qos.entity_factory().autoenable_created_entities = False
        self.assertEqual(qos.entity_factory().autoenable_created_entities, False)

    def test_subscriber_qos_values(self):
        qos = fastdds.SubscriberQos()

        # Presentation Qos, NOT implemented in the library.
        qos.presentation().access_scope = fastdds.GROUP_PRESENTATION_QOS
        qos.presentation().coherent_access = True
        qos.presentation().ordered_access = True

        self.assertEqual(qos.presentation().access_scope, fastdds.GROUP_PRESENTATION_QOS)
        self.assertEqual(qos.presentation().coherent_access, True)
        self.assertEqual(qos.presentation().ordered_access, True)

        # Partition Qos, implemented in the library.
        qos.partition().push_back("partition1")
        qos.partition().push_back("partition2")
        self.assertEqual(qos.partition().size(), 2)
        partitions = qos.partition().names()
        self.assertEqual(partitions[0], "partition1")
        self.assertEqual(partitions[1], "partition2")

        '''
        # Group Data Qos, implemented in the library.
        qos.group_data().set_max_size(10)
        data = fastdds.OctetResourceLimitedVector()
        data.push_back(1)
        data.push_back(2)
        qos.group_data().setValue(data)
        self.assertEqual(qos.group_data().dataVec(), data)
        
        #set_max_size
        #resize
        #dataVec
        #dataVec(val)
        #getValue
        #setValue(val)
        '''

        # Entity Factory Qos, implemented in the library
        qos.entity_factory().autoenable_created_entities = False
        self.assertEqual(qos.entity_factory().autoenable_created_entities, False)

    def test_datareader_qos_values(self):
        qos = fastdds.DataReaderQos()

        # Expects Inline QOS (Extension).
        qos.expects_inline_qos(True)
        self.assertTrue(qos.expects_inline_qos())

        qos.expects_inline_qos(False)
        self.assertFalse(qos.expects_inline_qos())

        # Durability Qos, implemented in the library.
        qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
        self.assertEqual(qos.durability().kind, fastdds.TRANSIENT_LOCAL_DURABILITY_QOS)

        qos.durability().durabilityKind(fastdds.TRANSIENT)
        self.assertEqual(qos.durability().durabilityKind(), fastdds.TRANSIENT)

        # Deadline Qos, implemented in the library.
        qos.deadline().period = fastdds.Time_t(5, 100)
        self.assertEqual(qos.deadline().period, fastdds.Time_t(5, 100))

        # Latency Budget Qos, implemented in the library.
        qos.latency_budget().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.latency_budget().duration, fastdds.Time_t(5, 100))

        # Liveliness Qos, implemented in the library.
        qos.liveliness().kind = fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
        qos.liveliness().lease_duration = fastdds.Time_t(5, 100)
        qos.liveliness().announcement_period = fastdds.Time_t(5, 100)
        self.assertEqual(qos.liveliness().kind, fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS)
        self.assertEqual(qos.liveliness().lease_duration, fastdds.Time_t(5, 100))
        self.assertEqual(qos.liveliness().announcement_period, fastdds.Time_t(5, 100))

        # Reliability Qos, implemented in the library.
        qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
        qos.reliability().max_blocking_time = fastdds.Time_t(5, 100)
        self.assertEqual(qos.reliability().kind, fastdds.RELIABLE_RELIABILITY_QOS)
        self.assertEqual(qos.reliability().max_blocking_time, fastdds.Time_t(5, 100))

        # Destination Order Qos, NOT implemented in the library.
        qos.destination_order().kind = fastdds.BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS
        self.assertEqual(qos.destination_order().kind, fastdds.BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS)

        # History Qos, implemented in the library.
        qos.history().kind = fastdds.KEEP_ALL_HISTORY_QOS
        qos.history().depth = 55
        self.assertEqual(qos.history().kind, fastdds.KEEP_ALL_HISTORY_QOS)
        self.assertEqual(qos.history().depth, 55)

        # Resource Limits Qos, implemented in the library.
        qos.resource_limits().max_samples = 5
        qos.resource_limits().max_instances = 10
        qos.resource_limits().max_samples_per_instance = 15
        qos.resource_limits().allocated_samples = 20
        qos.resource_limits().extra_samples = 25
        self.assertEqual(qos.resource_limits().max_samples, 5)
        self.assertEqual(qos.resource_limits().max_instances, 10)
        self.assertEqual(qos.resource_limits().max_samples_per_instance, 15)
        self.assertEqual(qos.resource_limits().allocated_samples, 20)
        self.assertEqual(qos.resource_limits().extra_samples, 25)

        '''
        # User Data Qos, implemented in the library.
        qos.user_data().set_max_size(10)
        data = fastdds.OctetResourceLimitedVector()
        data.push_back(1)
        data.push_back(2)
        qos.user_data().setValue(data)
        self.assertEqual(qos.user_data().dataVec(), data)
        
        #set_max_size
        #resize
        #dataVec
        #dataVec(val)
        #getValue
        #setValue(val)
        '''

        # Ownership Qos, implemented in the library.
        qos.ownership().kind = fastdds.EXCLUSIVE_OWNERSHIP_QOS
        self.assertEqual(qos.ownership().kind, fastdds.EXCLUSIVE_OWNERSHIP_QOS)

        # Time Based Filter Qos, NOT implemented in the library.
        qos.time_based_filter().minimum_separation = fastdds.Time_t(5, 100)
        self.assertEqual(qos.time_based_filter().minimum_separation, fastdds.Time_t(5, 100))

        # Reader Data Lifecycle Qos, NOT implemented in the library.
        qos.reader_data_lifecycle().autopurge_no_writer_samples_delay = fastdds.Time_t(5, 100)
        qos.reader_data_lifecycle().autopurge_disposed_samples_delay = fastdds.Time_t(10, 500)
        self.assertEqual(qos.reader_data_lifecycle().autopurge_no_writer_samples_delay, fastdds.Time_t(5, 100))
        self.assertEqual(qos.reader_data_lifecycle().autopurge_disposed_samples_delay, fastdds.Time_t(10, 500))

        # Lifespan Qos (Extension).
        qos.lifespan().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.lifespan().duration, fastdds.Time_t(5, 100))

        # Durability Service Qos (Extension).
        qos.durability_service().service_cleanup_delay = fastdds.Time_t(5, 100)
        qos.durability_service().history_kind = fastdds.KEEP_ALL_HISTORY_QOS
        qos.durability_service().history_depth = 10
        qos.durability_service().max_samples = 20
        qos.durability_service().max_instances = 30
        qos.durability_service().max_samples_per_instance = 40
        self.assertEqual(qos.durability_service().service_cleanup_delay, fastdds.Time_t(5, 100))
        self.assertEqual(qos.durability_service().history_kind, fastdds.KEEP_ALL_HISTORY_QOS)
        self.assertEqual(qos.durability_service().history_depth, 10)
        self.assertEqual(qos.durability_service().max_samples, 20)
        self.assertEqual(qos.durability_service().max_instances, 30)
        self.assertEqual(qos.durability_service().max_samples_per_instance, 40)

        # Reliable reader configuration (Extension)
        qos.reliable_reader_qos().times.initialAcknackDelay = fastdds.Time_t(5, 100)
        qos.reliable_reader_qos().times.heartbeatResponseDelay = fastdds.Time_t(10, 500)
        qos.reliable_reader_qos().disable_positive_ACKs.enabled = True
        qos.reliable_reader_qos().disable_positive_ACKs.duration = fastdds.Time_t(15, 700)
        self.assertEqual(qos.reliable_reader_qos().times.initialAcknackDelay, fastdds.Time_t(5, 100))
        self.assertEqual(qos.reliable_reader_qos().times.heartbeatResponseDelay, fastdds.Time_t(10, 500))
        self.assertEqual(qos.reliable_reader_qos().disable_positive_ACKs.enabled, True)
        self.assertEqual(qos.reliable_reader_qos().disable_positive_ACKs.duration, fastdds.Time_t(15, 700))

        rt = fastdds.ReaderTimes()
        rt.initialAcknackDelay = fastdds.Time_t(5, 100)
        rt.heartbeatResponseDelay = fastdds.Time_t(10, 500)
        self.assertEqual(qos.reliable_reader_qos().times, rt)

        dpa = fastdds.DisablePositiveACKsQosPolicy()
        dpa.enabled = True
        dpa.duration = fastdds.Time_t(15, 700)
        self.assertEqual(qos.reliable_reader_qos().disable_positive_ACKs, dpa)

        # Tipe consistency (Extension)
        qos.type_consistency().type_consistency.m_kind = fastdds.DISALLOW_TYPE_COERCION
        qos.type_consistency().type_consistency.m_ignore_sequence_bounds = False
        qos.type_consistency().type_consistency.m_ignore_string_bounds = False
        qos.type_consistency().type_consistency.m_ignore_member_names = True
        qos.type_consistency().type_consistency.m_prevent_type_widening = True
        qos.type_consistency().type_consistency.m_force_type_validation = True

        qos.type_consistency().representation.m_value.push_back(fastdds.XML_DATA_REPRESENTATION)

        self.assertEqual(qos.type_consistency().type_consistency.m_kind, fastdds.DISALLOW_TYPE_COERCION)
        self.assertEqual(qos.type_consistency().type_consistency.m_ignore_sequence_bounds, False)
        self.assertEqual(qos.type_consistency().type_consistency.m_ignore_string_bounds, False)
        self.assertEqual(qos.type_consistency().type_consistency.m_ignore_member_names, True)
        self.assertEqual(qos.type_consistency().type_consistency.m_prevent_type_widening, True)
        self.assertEqual(qos.type_consistency().type_consistency.m_force_type_validation, True)

        self.assertEqual(qos.type_consistency().representation.m_value.size(), 1)
        self.assertEqual(qos.type_consistency().representation.m_value[0], fastdds.XML_DATA_REPRESENTATION)

        tc = fastdds.TypeConsistencyEnforcementQosPolicy()
        tc.m_kind = fastdds.DISALLOW_TYPE_COERCION
        tc.m_ignore_sequence_bounds = False
        tc.m_ignore_string_bounds = False
        tc.m_ignore_member_names = True
        tc.m_prevent_type_widening = True
        tc.m_force_type_validation = True
        self.assertEqual(qos.type_consistency().type_consistency, tc)

        r = fastdds.DataRepresentationQosPolicy()
        r.m_value.push_back(fastdds.XML_DATA_REPRESENTATION)
        self.assertEqual(qos.type_consistency().representation, r)

        # Properties (Extension).
        pp = fastdds.Property()
        pp.name("Key")
        pp.value("value")
        qos.properties().properties().push_back(pp)
        self.assertEqual(qos.properties().properties().size(), 1)
        self.assertEqual(qos.properties().properties()[0].name(), "Key")
        self.assertEqual(qos.properties().properties()[0].value(), "value")

        '''
        bp = fastdds.BinaryProperty()
        bp.name("Key")
        bp.value().push_back(0)
        bp.value().push_back(1)
        qos.properties().binary_properties().push_back(bp)
        self.assertEqual(qos.properties().binary_properties().size(), 1)
        self.assertEqual(qos.properties().binary_properties()[0].name(), "Key")
        self.assertEqual(qos.properties().binary_properties()[0].value().size(), 2)
        self.assertEqual(qos.properties().binary_properties()[0].value()[0], 0)
        self.assertEqual(qos.properties().binary_properties()[0].value()[1], 1)
        '''

        # Endpoint configuration (Extension)
        loc = fastdds.Locator_t()
        loc.kind = fastdds.LOCATOR_KIND_TCPv4
        loc.port = 1004
        #loc.address = octet[16]

        qos.endpoint().unicast_locator_list.push_back(loc)
        qos.endpoint().multicast_locator_list.push_back(loc)
        qos.endpoint().remote_locator_list.push_back(loc)
        qos.endpoint().user_defined_id = 10
        qos.endpoint().entity_id = 15
        qos.endpoint().history_memory_policy = fastdds.DYNAMIC_REUSABLE_MEMORY_MODE

        self.assertEqual(qos.endpoint().unicast_locator_list.size(), 1)
        self.assertEqual(qos.endpoint().multicast_locator_list.size(), 1)
        self.assertEqual(qos.endpoint().remote_locator_list.size(), 1)
        # SWIG does not wrap the iterator idiom, so we cannot check the values
        self.assertEqual(qos.endpoint().user_defined_id, 10)
        self.assertEqual(qos.endpoint().entity_id, 15)
        self.assertEqual(qos.endpoint().history_memory_policy, fastdds.DYNAMIC_REUSABLE_MEMORY_MODE)

        qos.endpoint().unicast_locator_list.erase(loc)
        qos.endpoint().multicast_locator_list.erase(loc)
        qos.endpoint().remote_locator_list.erase(loc)
        self.assertEqual(qos.endpoint().unicast_locator_list.size(), 0)
        self.assertEqual(qos.endpoint().multicast_locator_list.size(), 0)
        self.assertEqual(qos.endpoint().remote_locator_list.size(), 0)

        # ReaderResourceLimitsQos
        qos.reader_resource_limits().matched_publisher_allocation.initial = 10
        qos.reader_resource_limits().matched_publisher_allocation.maximum = 100
        qos.reader_resource_limits().matched_publisher_allocation.increment = 10

        qos.reader_resource_limits().sample_infos_allocation.initial = 10
        qos.reader_resource_limits().sample_infos_allocation.maximum = 100
        qos.reader_resource_limits().sample_infos_allocation.increment = 10

        qos.reader_resource_limits().outstanding_reads_allocation.initial = 10
        qos.reader_resource_limits().outstanding_reads_allocation.maximum = 100
        qos.reader_resource_limits().outstanding_reads_allocation.increment = 10

        qos.reader_resource_limits().max_samples_per_read = 100

        self.assertEqual(qos.reader_resource_limits().matched_publisher_allocation.initial, 10)
        self.assertEqual(qos.reader_resource_limits().matched_publisher_allocation.maximum, 100)
        self.assertEqual(qos.reader_resource_limits().matched_publisher_allocation.increment, 10)

        self.assertEqual(qos.reader_resource_limits().sample_infos_allocation.initial, 10)
        self.assertEqual(qos.reader_resource_limits().sample_infos_allocation.maximum, 100)
        self.assertEqual(qos.reader_resource_limits().sample_infos_allocation.increment, 10)

        self.assertEqual(qos.reader_resource_limits().outstanding_reads_allocation.initial, 10)
        self.assertEqual(qos.reader_resource_limits().outstanding_reads_allocation.maximum, 100)
        self.assertEqual(qos.reader_resource_limits().outstanding_reads_allocation.increment, 10)

        self.assertEqual(qos.reader_resource_limits().max_samples_per_read, 100)

        # DataSharing configuration (Extension)
        ids = fastdds.uint16_t_vector()
        ids.push_back(1004)
        qos.data_sharing().automatic()
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        qos.data_sharing().automatic("CustomDirectory")
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        qos.data_sharing().automatic(ids)
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 1)
        self.assertEqual(qos.data_sharing().domain_ids()[0], 1004)

        qos.data_sharing().automatic("CustomDirectory", ids)
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 1)
        self.assertEqual(qos.data_sharing().domain_ids()[0], 1004)

        qos.data_sharing().on("CustomDirectory")
        self.assertEqual(qos.data_sharing().kind(), fastdds.ON)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        qos.data_sharing().on("CustomDirectory", ids)
        self.assertEqual(qos.data_sharing().kind(), fastdds.ON)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 1)
        self.assertEqual(qos.data_sharing().domain_ids()[0], 1004)

        qos.data_sharing().off()
        self.assertEqual(qos.data_sharing().kind(), fastdds.OFF)
        self.assertEqual(qos.data_sharing().shm_directory(), "")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

    def test_datawriter_qos_values(self):
        qos = fastdds.DataWriterQos()

        # Durability Qos, implemented in the library.
        qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
        self.assertEqual(qos.durability().kind, fastdds.TRANSIENT_LOCAL_DURABILITY_QOS)

        qos.durability().durabilityKind(fastdds.TRANSIENT)
        self.assertEqual(qos.durability().durabilityKind(), fastdds.TRANSIENT)

        # Deadline Qos, implemented in the library.
        qos.deadline().period = fastdds.Time_t(5, 100)
        self.assertEqual(qos.deadline().period, fastdds.Time_t(5, 100))

        # Latency Budget Qos, implemented in the library.
        qos.latency_budget().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.latency_budget().duration, fastdds.Time_t(5, 100))

        # Liveliness Qos, implemented in the library.
        qos.liveliness().kind = fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS
        qos.liveliness().lease_duration = fastdds.Time_t(5, 100)
        qos.liveliness().announcement_period = fastdds.Time_t(5, 100)
        self.assertEqual(qos.liveliness().kind, fastdds.MANUAL_BY_PARTICIPANT_LIVELINESS_QOS)
        self.assertEqual(qos.liveliness().lease_duration, fastdds.Time_t(5, 100))
        self.assertEqual(qos.liveliness().announcement_period, fastdds.Time_t(5, 100))

        # Reliability Qos, implemented in the library.
        qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
        qos.reliability().max_blocking_time = fastdds.Time_t(5, 100)
        self.assertEqual(qos.reliability().kind, fastdds.RELIABLE_RELIABILITY_QOS)
        self.assertEqual(qos.reliability().max_blocking_time, fastdds.Time_t(5, 100))

        # Destination Order Qos, NOT implemented in the library.
        qos.destination_order().kind = fastdds.BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS
        self.assertEqual(qos.destination_order().kind, fastdds.BY_SOURCE_TIMESTAMP_DESTINATIONORDER_QOS)

        # History Qos, implemented in the library.
        qos.history().kind = fastdds.KEEP_ALL_HISTORY_QOS
        qos.history().depth = 55
        self.assertEqual(qos.history().kind, fastdds.KEEP_ALL_HISTORY_QOS)
        self.assertEqual(qos.history().depth, 55)

        # Resource Limits Qos, implemented in the library.
        qos.resource_limits().max_samples = 5
        qos.resource_limits().max_instances = 10
        qos.resource_limits().max_samples_per_instance = 15
        qos.resource_limits().allocated_samples = 20
        qos.resource_limits().extra_samples = 25
        self.assertEqual(qos.resource_limits().max_samples, 5)
        self.assertEqual(qos.resource_limits().max_instances, 10)
        self.assertEqual(qos.resource_limits().max_samples_per_instance, 15)
        self.assertEqual(qos.resource_limits().allocated_samples, 20)
        self.assertEqual(qos.resource_limits().extra_samples, 25)

        '''
        # User Data Qos, implemented in the library.
        qos.user_data().set_max_size(10)
        data = fastdds.OctetResourceLimitedVector()
        data.push_back(1)
        data.push_back(2)
        qos.user_data().setValue(data)
        self.assertEqual(qos.user_data().dataVec(), data)
        
        #set_max_size
        #resize
        #dataVec
        #dataVec(val)
        #getValue
        #setValue(val)
        '''

        # Ownership Qos, implemented in the library.
        qos.ownership().kind = fastdds.EXCLUSIVE_OWNERSHIP_QOS
        self.assertEqual(qos.ownership().kind, fastdds.EXCLUSIVE_OWNERSHIP_QOS)

        # Lifespan Qos (Extension).
        qos.lifespan().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.lifespan().duration, fastdds.Time_t(5, 100))

        # Durability Service Qos (Extension).
        qos.durability_service().service_cleanup_delay = fastdds.Time_t(5, 100)
        qos.durability_service().history_kind = fastdds.KEEP_ALL_HISTORY_QOS
        qos.durability_service().history_depth = 10
        qos.durability_service().max_samples = 20
        qos.durability_service().max_instances = 30
        qos.durability_service().max_samples_per_instance = 40
        self.assertEqual(qos.durability_service().service_cleanup_delay, fastdds.Time_t(5, 100))
        self.assertEqual(qos.durability_service().history_kind, fastdds.KEEP_ALL_HISTORY_QOS)
        self.assertEqual(qos.durability_service().history_depth, 10)
        self.assertEqual(qos.durability_service().max_samples, 20)
        self.assertEqual(qos.durability_service().max_instances, 30)
        self.assertEqual(qos.durability_service().max_samples_per_instance, 40)

        # Properties (Extension).
        pp = fastdds.Property()
        pp.name("Key")
        pp.value("value")
        qos.properties().properties().push_back(pp)
        self.assertEqual(qos.properties().properties().size(), 1)
        self.assertEqual(qos.properties().properties()[0].name(), "Key")
        self.assertEqual(qos.properties().properties()[0].value(), "value")

        '''
        bp = fastdds.BinaryProperty()
        bp.name("Key")
        bp.value().push_back(0)
        bp.value().push_back(1)
        qos.properties().binary_properties().push_back(bp)
        self.assertEqual(qos.properties().binary_properties().size(), 1)
        self.assertEqual(qos.properties().binary_properties()[0].name(), "Key")
        self.assertEqual(qos.properties().binary_properties()[0].value().size(), 2)
        self.assertEqual(qos.properties().binary_properties()[0].value()[0], 0)
        self.assertEqual(qos.properties().binary_properties()[0].value()[1], 1)
        '''

        # Endpoint configuration (Extension)
        loc = fastdds.Locator_t()
        loc.kind = fastdds.LOCATOR_KIND_TCPv4
        loc.port = 1004
        #loc.address = octet[16]

        qos.endpoint().unicast_locator_list.push_back(loc)
        qos.endpoint().multicast_locator_list.push_back(loc)
        qos.endpoint().remote_locator_list.push_back(loc)
        qos.endpoint().user_defined_id = 10
        qos.endpoint().entity_id = 15
        qos.endpoint().history_memory_policy = fastdds.DYNAMIC_REUSABLE_MEMORY_MODE

        self.assertEqual(qos.endpoint().unicast_locator_list.size(), 1)
        self.assertEqual(qos.endpoint().multicast_locator_list.size(), 1)
        self.assertEqual(qos.endpoint().remote_locator_list.size(), 1)
        # SWIG does not wrap the iterator idiom, so we cannot check the values
        self.assertEqual(qos.endpoint().user_defined_id, 10)
        self.assertEqual(qos.endpoint().entity_id, 15)
        self.assertEqual(qos.endpoint().history_memory_policy, fastdds.DYNAMIC_REUSABLE_MEMORY_MODE)

        qos.endpoint().unicast_locator_list.erase(loc)
        qos.endpoint().multicast_locator_list.erase(loc)
        qos.endpoint().remote_locator_list.erase(loc)
        self.assertEqual(qos.endpoint().unicast_locator_list.size(), 0)
        self.assertEqual(qos.endpoint().multicast_locator_list.size(), 0)
        self.assertEqual(qos.endpoint().remote_locator_list.size(), 0)

        # WriterResourceLimitsQos
        qos.writer_resource_limits().matched_subscriber_allocation.initial = 10
        qos.writer_resource_limits().matched_subscriber_allocation.maximum = 100
        qos.writer_resource_limits().matched_subscriber_allocation.increment = 10

        self.assertEqual(qos.writer_resource_limits().matched_subscriber_allocation.initial, 10)
        self.assertEqual(qos.writer_resource_limits().matched_subscriber_allocation.maximum, 100)
        self.assertEqual(qos.writer_resource_limits().matched_subscriber_allocation.increment, 10)

        # DataSharing configuration (Extension)
        ids = fastdds.uint16_t_vector()
        ids.push_back(1004)
        qos.data_sharing().automatic()
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        qos.data_sharing().automatic("CustomDirectory")
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        qos.data_sharing().automatic(ids)
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 1)
        self.assertEqual(qos.data_sharing().domain_ids()[0], 1004)

        qos.data_sharing().automatic("CustomDirectory", ids)
        self.assertEqual(qos.data_sharing().kind(), fastdds.AUTO)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 1)
        self.assertEqual(qos.data_sharing().domain_ids()[0], 1004)

        qos.data_sharing().on("CustomDirectory")
        self.assertEqual(qos.data_sharing().kind(), fastdds.ON)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        qos.data_sharing().on("CustomDirectory", ids)
        self.assertEqual(qos.data_sharing().kind(), fastdds.ON)
        self.assertEqual(qos.data_sharing().shm_directory(), "CustomDirectory")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 1)
        self.assertEqual(qos.data_sharing().domain_ids()[0], 1004)

        qos.data_sharing().off()
        self.assertEqual(qos.data_sharing().kind(), fastdds.OFF)
        self.assertEqual(qos.data_sharing().shm_directory(), "")
        self.assertEqual(len(qos.data_sharing().domain_ids()), 0)

        # Transport Priority Qos, NOT implemented in the library.
        qos.transport_priority().value = 10
        self.assertEqual(qos.transport_priority().value, 10)

        # Lifespan Qos, implemented in the library.
        qos.lifespan().duration = fastdds.Time_t(5, 100)
        self.assertEqual(qos.lifespan().duration, fastdds.Time_t(5, 100))

        # Ownership Strength Qos, implemented in the library.
        qos.ownership_strength().value = 10
        self.assertEqual(qos.ownership_strength().value, 10)

        # Writer Data Lifecycle Qos, NOT implemented in the library.
        qos.writer_data_lifecycle().autodispose_unregistered_instances = False
        self.assertEqual(qos.writer_data_lifecycle().autodispose_unregistered_instances, False)

        # Publication Mode Qos, implemented in the library.
        qos.publish_mode().kind = fastdds.ASYNCHRONOUS_PUBLISH_MODE
        self.assertEqual(qos.publish_mode().kind, fastdds.ASYNCHRONOUS_PUBLISH_MODE)

        # Data Representation Qos, implemented in the library.
        qos.representation().m_value.push_back(fastdds.XML_DATA_REPRESENTATION)
        self.assertEqual(qos.representation().m_value[0], fastdds.XML_DATA_REPRESENTATION)

        # RTPS Reliable Writer Qos
        qos.reliable_writer_qos().times.initialHeartbeatDelay = fastdds.Time_t(5, 100)
        qos.reliable_writer_qos().times.heartbeatPeriod = fastdds.Time_t(10, 500)
        qos.reliable_writer_qos().times.nackResponseDelay = fastdds.Time_t(15, 700)
        qos.reliable_writer_qos().times.nackSupressionDuration = fastdds.Time_t(20, 000)
        qos.reliable_writer_qos().disable_positive_acks.enabled = True
        qos.reliable_writer_qos().disable_positive_acks.duration = fastdds.Time_t(15, 700)
        self.assertEqual(qos.reliable_writer_qos().times.initialHeartbeatDelay, fastdds.Time_t(5, 100))
        self.assertEqual(qos.reliable_writer_qos().times.heartbeatPeriod, fastdds.Time_t(10, 500))
        self.assertEqual(qos.reliable_writer_qos().times.nackResponseDelay, fastdds.Time_t(15, 700))
        self.assertEqual(qos.reliable_writer_qos().times.nackSupressionDuration, fastdds.Time_t(20, 000))
        self.assertEqual(qos.reliable_writer_qos().disable_positive_acks.enabled, True)
        self.assertEqual(qos.reliable_writer_qos().disable_positive_acks.duration, fastdds.Time_t(15, 700))

        wt = fastdds.WriterTimes()
        wt.initialHeartbeatDelay = fastdds.Time_t(5, 100)
        wt.heartbeatPeriod = fastdds.Time_t(10, 500)
        wt.nackResponseDelay = fastdds.Time_t(15, 700)
        wt.nackSupressionDuration = fastdds.Time_t(20, 000)
        self.assertEqual(qos.reliable_writer_qos().times, wt)

        dpa = fastdds.DisablePositiveACKsQosPolicy()
        dpa.enabled = True
        dpa.duration = fastdds.Time_t(15, 700)
        self.assertEqual(qos.reliable_writer_qos().disable_positive_acks, dpa)

        # Throughput controller
        qos.throughput_controller().bytesPerPeriod = 10
        qos.throughput_controller().periodMillisecs = 15
        self.assertEqual(qos.throughput_controller().bytesPerPeriod, 10)
        self.assertEqual(qos.throughput_controller().periodMillisecs, 15)
