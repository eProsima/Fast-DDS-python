# Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import fastdds
from blackbox_common import *

from threading import Thread, Lock, Condition
from os import getpid
from socket import gethostname
from time import sleep
import copy

class PubSubWriter :

    class ParticipantListener(fastdds.DomainParticipantListener) :

        def __init__(self, writer) :
            self._writer = writer
            super().__init__()

        def on_participant_discovery(self, domain_participant, info) :
            if (self._writer._onDiscovery != None):
                self._writer._cvDiscovery.acquire()
                self._writer._discovery_result = self._writer._onDiscovery(info)
                self._writer._cvDiscovery.notify()
                self._writer._cvDiscovery.release()

            if (info.status == fastdds.ParticipantDiscoveryInfo.DISCOVERED_PARTICIPANT) :
                self._writer._participant_matched()

            elif (info.status == fastdds.ParticipantDiscoveryInfo.REMOVED_PARTICIPANT or
                  info.status == fastdds.ParticipantDiscoveryInfo.DROPPED_PARTICIPANT) :
                self._writer._participant_unmatched()

        def on_subscriber_discovery(self, domain_participant, info) :
            if (info.status == fastdds.ReaderDiscoveryInfo.DISCOVERED_READER) :
                self._writer._add_reader_info(info.info)
            elif (info.status == fastdds.ReaderDiscoveryInfo.CHANGED_QOS_READER) :
                self._writer._change_reader_info(info.info)
            elif (info.status == fastdds.ReaderDiscoveryInfo.REMOVED_READER) :
                self._writer._remove_reader_info(info.info)

        def on_publisher_discovery(self, domain_participant, info) :
            if (info.status == fastdds.WriterDiscoveryInfo.DISCOVERED_WRITER) :
                self._writer._add_writer_info(info.info)
            elif (info.status == fastdds.WriterDiscoveryInfo.CHANGED_QOS_WRITER) :
                self._writer._change_writer_info(info.info)
            elif (info.status == fastdds.WriterDiscoveryInfo.REMOVED_WRITER) :
                self._writer._remove_writer_info(info.info)

# if HAVE_SECURITY
        def onParticipantAuthentication(self, domain_participant, info) :
            if (info.status == fastdds.ParticipantAuthenticationInfo.AUTHORIZED_PARTICIPANT) :
                self._writer._authorized()
            elif (info.status == fastdds.ParticipantAuthenticationInfo.UNAUTHORIZED_PARTICIPANT) :
                self._writer._unauthorized()
# endif HAVE_SECURITY


    class Listener (fastdds.DataWriterListener) :
        def __init__(self, writer) :
            self._writer = writer
            self._times_deadline_missed = 0
            self._times_liveliness_lost = 0
            super().__init__()

        def on_publication_matched(self, datawriter, info) :
            if (0 < info.current_count_change) :
                print ("Publisher matched subscriber {}".format(info.last_subscription_handle))
                self._writer._matched()
            else :
                print ("Publisher unmatched subscriber {}".format(info.last_subscription_handle))
                self._writer._unmatched()

        def on_offered_deadline_missed(self, datawriter, status) :
            self._times_deadline_missed = status.total_count

        def on_offered_incompatible_qos(self, datawriter, status) :
            self._writer.incompatible_qos(status)

        def on_liveliness_lost(self, datawriter, status) :
            self._times_liveliness_lost = status.total_count
            self._writer.liveliness_lost()

        def  missed_deadlines(self) :
            return self._times_deadline_missed

        def  times_liveliness_lost(self) :
            return self._times_liveliness_lost

    def __init__(self, data_type, topic_data_type, topic_name) :
        self._participant_listener = PubSubWriter.ParticipantListener(self)
        self._listener = PubSubWriter.Listener(self)
        self._participant = None
        self._participant_qos = fastdds.DomainParticipantQos()
        self._topic = None
        self._publisher = None
        self._publisher_qos = fastdds.PublisherQos()
        self._datawriter = None
        self._datawriter_qos = fastdds.DataWriterQos()
        self._status_mask = fastdds.StatusMask.all()
        self._topic_name = topic_name
        self._participant_guid = fastdds.GUID_t_unknown()
        self._datawriter_guid = fastdds.GUID_t_unknown()
        self._initialized = False
        self._total_msgs = []
        self._cv = Condition()
        self._cvDiscovery = Condition()
        self._matched_reader = 0
        self._matched_participants = 0
        self._data_type = data_type
        self._topic_data_type = topic_data_type
        self._cvEntitiesInfoList = Condition()
        self._mapWriterInfoList = {}
        self._mapReaderInfoList = {}
        self._mapTopicCountList = {}
        self._mapPartitionCountList = {}
        self._discovery_result = False
        self._xml_file = ""
        self._participant_profile = ""
        self._datawriter_profile = ""
        self._onDiscovery = None
# if HAVE_SECURITY
        self._cvAuthentication = Condition()
        self._authorized_participant = 0
        self._unauthorized = 0
# endif HAVE_SECURITY
        self._liveliness_cv = Condition()
        self._times_liveliness_lost = 0
        self._incompatible_qos_cv = Condition()
        self._times_incompatible_qos = 0
        self._last_incompatible_qos = fastdds.INVALID_QOS_POLICY_ID


        # Generate topic name
        self._topic_name = "{topic}_{host}_{pid}".format(topic=self._topic_name, host=gethostname(), pid=getpid())

        if (enable_datasharing) :
            self._datawriter_qos.data_sharing().automatic()
            self._datawriter_qos.resource_limits().extra_samples = 5
        else :
            self._datawriter_qos.data_sharing().off()

        if (use_pull_mode) :
            self._datawriter_qos.properties().properties().emplace_back("fastdds.push_mode", "false")

        # By default, memory mode is preallocated (the most restrictive)
        self._datawriter_qos.endpoint().history_memory_policy = fastdds.PREALLOCATED_MEMORY_MODE

        # By default, heartbeat period and nack response delay are 100 milliseconds.
        self._datawriter_qos.reliable_writer_qos().times.heartbeatPeriod.seconds = 0
        self._datawriter_qos.reliable_writer_qos().times.heartbeatPeriod.nanosec = 100000000
        self._datawriter_qos.reliable_writer_qos().times.nackResponseDelay.seconds = 0
        self._datawriter_qos.reliable_writer_qos().times.nackResponseDelay.nanosec = 100000000

        # Increase default max_blocking_time to 1 second
        self._datawriter_qos.reliability().max_blocking_time.seconds = 1
        self._datawriter_qos.reliability().max_blocking_time.nanosec = 0

    def __del__(self) :
        self.destroy()

    def get_native_writer(self) :
        return self._datawriter

    def init(self) :
        assert(not self._initialized)
        self._matched_reader = 0

        if (self._xml_file) :
            fastdds.DomainParticipantFactory.get_instance().load_XML_profiles_file(self._xml_file)
            if (not self._participant_profile.empty()) :
                self._participant = fastdds.DomainParticipantFactory.get_instance().create_participant_with_profile(
                    getpid() % 230,
                    self._participant_profile,
                    self._participant_listener,
                    fastdds.StatusMask.none())
                assert(self._participant != None)
                assert(self._participant.is_enabled())
        if (self._participant == None) :
            self._participant = fastdds.DomainParticipantFactory.get_instance().create_participant(
                getpid() % 230,
                self._participant_qos,
                self._participant_listener,
                fastdds.StatusMask.none())

        if (self._participant != None) :
            self._participant_guid = self._participant.guid()

            # Register type
            self._type = fastdds.TypeSupport(self._topic_data_type())

            self._participant.register_type(self._type)

            # Create topic
            self._topic = self._participant.create_topic(self._topic_name, self._type.get_type_name(),
                    fastdds.TOPIC_QOS_DEFAULT)
            assert(self._topic != None)
            assert(self._topic.is_enabled())

            # Create publisher
            self.createPublisher()

    def createPublisher(self) :
        if (self._participant != None) :
            self._publisher = self._participant.create_publisher(self._publisher_qos)
            assert(self._publisher != None)
            assert(self._publisher.is_enabled())

            if (self._xml_file) :
                if (self._datawriter_profile) :
                    self._datawriter = self._publisher.create_datawriter_with_profile(self._topic, self._datawriter_profile, self._listener,
                                    self._status_mask)
                    assert(self._datawriter != None)
                    assert(self._datawriter.is_enabled())
            if (self._datawriter == None) :
                self._datawriter = self._publisher.create_datawriter(self._topic, self._datawriter_qos, self._listener, self._status_mask)

            if (self._datawriter != None) :
                print ("Created datawriter {guid} for topic {topic}".format (guid=self._datawriter.guid(), topic=self._topic_name))
                self._initialized = True;
                self._datawriter_guid = self._datawriter.guid()

    def removePublisher(self) :
        self._initialized = False
        if (self._datawriter != None) :
            self._publisher.delete_datawriter(self._datawriter)
        self._datawriter = None
        if (self._publisher != None) :
            self._participant.delete_publisher(self._publisher)
        self._publisher = None
        self._matched_reader = 0

    def isInitialized(self) :
        return self._initialized

    def getParticipant(self) :
        return self._participant

    def destroy(self) :
        if (self._participant != None) :
            if (self._datawriter) :
                self._publisher.delete_datawriter(self._datawriter)
                self._datawriter = None
            if (self._publisher) :
                self._participant.delete_publisher(self._publisher)
                self._publisher = None
            if (self._topic) :
                self._participant.delete_topic(self._topic)
                self._topic = None
            fastdds.DomainParticipantFactory.get_instance().delete_participant(self._participant)
            self._participant = None

        self.initialized_ = False


    def send(self, msgs, milliseconds = 0) :
        while msgs :
            msg = msgs[0]
            if (self._datawriter.write(msg)) :
                default_send_print(msg)
                msgs.pop(0)
                if (milliseconds > 0) :
                    sleep(milliseconds / 1000)
            else :
                break

    def register_instance(self, msg) :
        return self._datawriter.register_instance(msg)

    def unregister_instance(self, msg, instance_handle) :
        return fastdds.ReturnCode_t.RETCODE_OK == self._datawriter.unregister_instance(msg, instance_handle)

    def dispose(self, msg, instance_handle) :
        return fastdds.ReturnCode_t.RETCODE_OK == self._datawriter.dispose(msg, instance_handle)

    def send_sample(self, msg) :
        return self._datawriter.write(msg)

    def assert_liveliness(self) :
        self._datawriter.assert_liveliness()

    def wait_discovery(self, timeout=None, expected_match = 0) :
        self._cvDiscovery.acquire()
        print ("Writer is waiting discovery...")
        if (expected_match == 0) :
            ret = self._cvDiscovery.wait_for(lambda : self._matched_reader != 0, timeout)
        else :
            ret = self._cvDiscovery.wait_for(lambda : self._matched_reader == expected_match, timeout)
        self._cvDiscovery.release()
        print("Writer discovery finished...")
        return ret

    def wait_participant_undiscovery(self, timeout=None) :
        ret_value = True;
        self._cvDiscovery.acquire()
        print("Writer is waiting participant undiscovery...")
        ret_value = self._cvDiscovery.wait_for(lambda : self._matched_participants == 0, timeout)
        self._cvDiscovery.release()

        if (ret_value) :
            print("Writer participant undiscovery finished successfully...")
        else :
            print("Writer participant undiscovery finished unsuccessfully...")

        return ret_value


    def wait_reader_undiscovery(self) :
        self._cvDiscovery.acquire()
        print ("Writer is waiting removal...")
        self._cvDiscovery.wait_for(lambda : self._matched_reader == 0)
        self._cvDiscovery.release()
        print("Writer removal finished...")

    def wait_liveliness_lost(self, times = 1) :
        self._liveliness_cv.acquire()
        self._liveliness_cv.wait_for(lambda : self._times_liveliness_lost >= times)
        self._liveliness_cv.release()

    def liveliness_lost(self) :
        self._liveliness_cv.acquire()
        self._times_liveliness_lost += 1
        self._liveliness_cv.notify()
        self._liveliness_cv.release()

    def wait_incompatible_qos(self, times = 1) :
        self._incompatible_qos_cv.acquire()
        self._incompatible_qos_cv.wait_for(lambda : self._times_incompatible_qos >= times)
        self._incompatible_qos_cv.release()

    def incompatible_qos(self, status) :
        self._incompatible_qos_cv.acquire()
        self._times_incompatible_qos += 1
        self._last_incompatible_qos = status.last_policy_id
        self._incompatible_qos_cv.notify()
        self._incompatible_qos_cv.release()

#if HAVE_SECURITY
    def waitAuthorized(self) :
        self._cvAuthentication.acquire()
        print ("Reader is waiting authorization...")
        self._cvAuthentication.wait_for(lambda : self._authorized_participant > 0)
        self._cvAuthentication.release()
        print("Reader authorization finished...")

    def waitUnauthorized(self) :
        self._cvAuthentication.acquire()
        print ("Reader is waiting unauthorization...")
        self._cvAuthentication.wait_for(lambda : self._unauthorized > 0)
        self._cvAuthentication.release()
        print("Reader unauthorization finished...")
#endif // if HAVE_SECURITY

    def block_until_discover_topic(self, topicName, repeatedTimes) :
        self._cvEntitiesInfoList.acquire()
        self._cvEntitiesInfoList.wait_for(lambda : self._mapTopicCountList.get(topicName.to_string()) == repeatedTimes)
        self._cvEntitiesInfoList.release()

    def block_until_discover_partition(self, partition, repeatedTimes) :
        self._cvEntitiesInfoList.acquire()
        self._cvEntitiesInfoList.wait_for(lambda : self._mapPartitionCountList.get(partition) == repeatedTimes)
        self._cvEntitiesInfoList.release()

    def waitForAllAcked(self, max_wait) :
        return (fastdds.ReturnCode_t.RETCODE_OK ==
               self._datawriter.wait_for_acknowledgments(fastdds.Time_t(max_wait, 0)))

    def deactivate_status_listener(self, mask) :
        self._status_mask >> mask
        return self

    def activate_status_listener(self, mask) :
        self._status_mask << mask
        return self

    def reset_status_listener(self) :
        self._status_mask = fastdds.StatusMask.all()
        return self

    def reliability(self, kind) :
        self._datawriter_qos.reliability().kind = kind
        return self

    def mem_policy(self, mem_policy) :
        self._datawriter_qos.endpoint().history_memory_policy = mem_policy
        return self

    def deadline_period(self, deadline_period) :
        self._datawriter_qos.deadline().period = deadline_period
        return self

    def liveliness_kind(self, kind) :
        self._datawriter_qos.liveliness().kind = kind
        return self

    def liveliness_lease_duration(self, lease_duration) :
        self._datawriter_qos.liveliness().lease_duration = lease_duration
        return self

    def latency_budget_duration(self, latency_duration) :
        self._datawriter_qos.latency_budget().duration = latency_duration
        return self

    def get_latency_budget_duration(self) :
        return self._datawriter_qos.latency_budget().duration

    def liveliness_announcement_period( self, announcement_period) :
        self._datawriter_qos.liveliness().announcement_period = announcement_period
        return self

    def lifespan_period(self, lifespan_period) :
        self._datawriter_qos.lifespan().duration = lifespan_period
        return self

    def keep_duration(self, duration) :
        self._datawriter_qos.reliable_writer_qos().disable_positive_ACKs.enabled = True
        self._datawriter_qos.reliable_writer_qos().disable_positive_ACKs.duration = duration
        return self

    def max_blocking_time(self, time) :
        self._datawriter_qos.reliability().max_blocking_time = time
        return self

    def add_throughput_controller_descriptor_to_pparams(self, scheduler_policy, bytesPerPeriod, periodInMs) :
        new_flow_controller = fastdds.FlowControllerDescriptor()
        new_flow_controller.name = "MyFlowController"
        new_flow_controller.scheduler = scheduler_policy
        new_flow_controller.max_bytes_per_period = bytesPerPeriod
        new_flow_controller.period_ms = periodInMs
        self._participant_qos.flow_controllers().push_back(new_flow_controller)
        self._datawriter_qos.publish_mode().flow_controller_name = "MyFlowController"
        return self

    def asynchronously(self, kind) :
        self._datawriter_qos.publish_mode().kind = kind
        return self

    def history_kind(self, kind) :
        self._datawriter_qos.history().kind = kind
        return self

    def history_depth(self, depth) :
        self._datawriter_qos.history().depth = depth
        return self

    def disable_builtin_transport(self,) :
        self._participant_qos.transport().use_builtin_transports = False
        return self

    def add_user_transport_to_pparams(self, userTransportDescriptor) :
        self._participant_qos.transport().user_transports.push_back(userTransportDescriptor)
        return self

    def durability_kind(self, kind) :
        self._datawriter_qos.durability().kind = kind
        return self

    def resource_limits_allocated_samples(self, initial) :
        self._datawriter_qos.resource_limits().allocated_samples = initial
        return self

    def resource_limits_max_samples(self, max) :
        self._datawriter_qos.resource_limits().max_samples = max
        return self

    def resource_limits_max_instances(self, max) :
        self._datawriter_qos.resource_limits().max_instances = max
        return self

    def resource_limits_max_samples_per_instance(self, max) :
        self._datawriter_qos.resource_limits().max_samples_per_instance = max
        return self

    def resource_limits_extra_samples(self, extra) :
        self._datawriter_qos.resource_limits().extra_samples = extra
        return self

    def matched_readers_allocation(self, initial, maximum) :
        self._datawriter_qos.writer_resource_limits().matched_subscriber_allocation.initial = initial
        self._datawriter_qos.writer_resource_limits().matched_subscriber_allocation.maximum = maximum
        return self

    def expect_no_allocs(self) :
        # TODO(Mcc): Add no allocations check code when feature is completely ready
        return self

    def heartbeat_period_seconds(self, secs) :
        self._datawriter_qos.reliable_writer_qos().times.heartbeatPeriod.seconds = secs
        return self

    def heartbeat_period_nanosec(self, nanosec) :
        self._datawriter_qos.reliable_writer_qos().times.heartbeatPeriod.nanosec = nanosec
        return self

    def unicastLocatorList(self, unicast_locators) :
        self._datawriter_qos.endpoint().unicast_locator_list = unicast_locators
        return self

    def add_to_unicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._datawriter_qos.endpoint().unicast_locator_list.push_back(loc)

        return self

    def multicastLocatorList(self, multicast_locators) :
        self._datawriter_qos.endpoint().multicast_locators = multicast_locators
        return self

    def add_to_multicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._datawriter_qos.endpoint().multicast_locator_list.push_back(loc)

        return self

    def metatraffic_unicast_locator_list(self, unicast_locators) :
        self._participant_qos.wire_protocol().builtin.metatrafficUnicastLocatorList = unicast_locators
        return self

    def add_to_metatraffic_unicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._participant_qos.wire_protocol().builtin.metatrafficUnicastLocatorList.push_back(loc)

        return self

    def metatraffic_multicast_locator_list(self, multicast_locators) :
        self._participant_qos.wire_protocol().builtin.metatrafficMulticastLocatorList = multicast_locators
        return self

    def add_to_metatraffic_multicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._participant_qos.wire_protocol().builtin.metatrafficMulticastLocatorList.push_back(loc)

        return self

    def set_default_unicast_locators(self, locators) :
        self._participant_qos.wire_protocol().default_unicast_locator_list = locators
        return self

    def add_to_default_unicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._participant_qos.wire_protocol().default_unicast_locator_list.push_back(loc)

        return self

    def set_default_multicast_locators(self, locators) :
        self._participant_qos.wire_protocol().default_multicast_locator_list = locators
        return self

    def add_to_default_multicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._participant_qos.wire_protocol().default_multicast_locator_list.push_back(loc)

        return self

    def initial_peers(self, initial_peers) :
        self._participant_qos.wire_protocol().builtin.initialPeersList = initial_peers
        return self

    def static_discovery(self, filename) :
        self._participant_qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol = False
        self._participant_qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol = True
        self._participant_qos.wire_protocol().builtin.discovery_config.static_edp_xml_config(filename)
        return self

    def property_policy(self, property_policy) :
        self._participant_qos.properties(property_policy)
        return self

    def entity_property_policy(self, property_policy) :
        self._datawriter_qos.properties(property_policy)
        return self


    def setPublisherIDs(self, UserID, EntityID) :
        self._datawriter_qos.endpoint().user_defined_id = UserID
        self._datawriter_qos.endpoint().entity_id = EntityID
        return self

    def setManualTopicName(self, topic_name) :
        self.topic_name_ = topic_name
        return self

    def disable_multicast(self, participantId) :
        self._participant_qos.wire_protocol().participant_id = participantId

        default_unicast_locators = fastdds.LocatorList()
        default_unicast_locator = fastdds.Locator_t()
        loopback_locator = fastdds.Locator_t()
        if (not use_udpv4) :
            default_unicast_locator.kind = fastdds.LOCATOR_KIND_UDPv6
            loopback_locator.kind = fastdds.LOCATOR_KIND_UDPv6

        default_unicast_locators.push_back(default_unicast_locator)
        self._participant_qos.wire_protocol().builtin.metatrafficUnicastLocatorList = default_unicast_locators

        if (not fastdds.IPLocator.setIPv4(loopback_locator, 127, 0, 0, 1)) :
            fastdds.IPLocator.setIPv6(loopback_locator, "::1")
        self._participant_qos.wire_protocol().builtin.initialPeersList.push_back(loopback_locator)
        return self

    def partition(self, partition) :
        self._publisher_qos.partition().push_back(partition)
        return self

    def userData(self, user_data) :
        self._participant_qos.user_data(user_data)
        return self

    def endpoint_userData(self, user_data) :
        self._datawriter_qos.user_data(user_data)
        return self

    def user_data_max_size(self, max_user_data) :
        self._participant_qos.allocation().data_limits.max_user_data = max_user_data
        return self

    def properties_max_size(self, max_properties) :
        self._participant_qos.allocation().data_limits.max_properties = max_properties
        return self

    def partitions_max_size(self, max_partitions) :
        self._participant_qos.allocation().data_limits.max_partitions = max_partitions
        return self

    def lease_duration(self, lease_duration, announce_period) :
        self._participant_qos.wire_protocol().builtin.discovery_config.leaseDuration = lease_duration
        self._participant_qos.wire_protocol().builtin.discovery_config.leaseDuration_announcementperiod = announce_period
        return self

    def load_participant_attr(self, xml) :
        # TODO
        return self

    def load_publisher_attr(self, xml) :
        # TODO
        return self

    def max_initial_peers_range(self, maxInitialPeerRange) :
        self._participant_qos.transport().use_builtin_transports = False
        if (use_udpv4) :
            descriptor = fastdds.UDPv4TransportDescriptor
        else :
            descriptor = fastdds.UDPv6TransportDescriptor
        
        descriptor.maxInitialPeersRange = maxInitialPeerRange
        self._participant_qos.transport().user_transports.push_back(descriptor)
        return self

    def socket_buffer_size(self, sockerBufferSize) :
        self._participant_qos.transport().listen_socket_buffer_size = sockerBufferSize
        return self

    def participant_id(self, participantId) :
        self._participant_qos.wire_protocol().participant_id = participantId
        return self

    def datasharing_off(self) :
        self._datawriter_qos.data_sharing().off()
        return self

    def datasharing_auto(self, domain_id) :
        self._datawriter_qos.data_sharing().automatic(domain_id)
        return self

    def datasharing_auto(self, directory, domain_id) :
        self._datawriter_qos.data_sharing().automatic(directory, domain_id)
        return self

    def datasharing_on(self, directory, domain_id) :
        self._datawriter_qos.data_sharing().on(directory, domain_id)
        return self

    def topic_name(self) :
        return self._topic_name

    def participant_guid(self) :
        return self._participant_guid

    def datawriter_guid(self) :
        return self._datawriter_guid

#if HAVE_SQLITE3
    def make_persistent(self, filename, persistence_guid) :
        self._participant_qos.properties().properties().emplace_back("dds.persistence.plugin", "builtin.SQLITE3")
        self._participant_qos.properties().properties().emplace_back("dds.persistence.sqlite3.filename", filename)
        self._datawriter_qos.durability().kind = fastdds.TRANSIENT_DURABILITY_QOS
        self._datawriter_qos.properties().properties().emplace_back("dds.persistence.guid", persistence_guid)

        return self
#endif // if HAVE_SQLITE3

    def update_partition(self, partition) :
        self._publisher_qos.partition().clear()
        self._publisher_qos.partition().push_back(partition)
        return (fastdds.ReturnCode_t.RETCODE_OK == self._publisher.set_qos(self._publisher_qos))

    def clear_partitions(self) :
        self._publisher_qos.partition().clear()
        return (fastdds.ReturnCode_t.RETCODE_OK == self._publisher.set_qos(self._publisher_qos))

    def remove_all_changes(self, number_of_changes_removed) :
        return fastdds.ReturnCode_t.RETCODE_OK == self._datawriter.clear_history(number_of_changes_removed)

    def is_matched(self) :
        return self._matched_reader > 0

    def missed_deadlines(self) :
        return self._listener.missed_deadlines()

    def times_liveliness_lost(self) :
        self._liveliness_cv.acquire()
        ret = self._times_liveliness_lost
        self._liveliness_cv.release()
        return ret

    def times_incompatible_qos(self) :
        self._incompatible_qos_cv.acquire()
        ret = self._times_incompatible_qos
        self._incompatible_qos_cv.release()
        return ret

    def last_incompatible_qos(self) :
        self._incompatible_qos_cv.acquire()
        ret = self._lasat_incompatible_qos
        self._incompatible_qos_cv.release()
        return ret

    def get_incompatible_qos_status(self) :
        ret = fastdds.OfferedIncompatibleQosStatus()
        self._datawriter.get_offered_incompatible_qos_status(ret)
        return ret

    def set_xml_filename(self, name) :
        self._xml_file = name

    def set_participant_profile(self, profile) :
        self._participant_profile = profile

    def set_datawriter_profile(self, profile) :
        self._datawriter_profile = profile


    def _participant_matched(self) :
        self._cvDiscovery.acquire()
        self._matched_participants += 1
        self._cvDiscovery.notify()
        self._cvDiscovery.release()

    def _participant_unmatched(self) :
        self._cvDiscovery.acquire()
        self._matched_participants -= 1
        self._cvDiscovery.notify()
        self._cvDiscovery.release()

    def _matched(self) :
        self._cvDiscovery.acquire()
        self._matched_reader += 1
        self._cvDiscovery.notify()
        self._cvDiscovery.release()

    def _unmatched(self) :
        self._cvDiscovery.acquire()
        self._matched_reader -= 1
        self._cvDiscovery.notify()
        self._cvDiscovery.release()

#if HAVE_SECURITY
    def _authorized(self) :
        self._cvAuthentication.acquire()
        self._authorized_participant += 1
        self._cvAuthentication.notify_all()
        self._cvAuthentication.release()

    def _unauthorized(self) :
        self._cvAuthentication.acquire()
        self._unauthorized += 1
        self._cvAuthentication.notify_all()
        self._cvAuthentication.release()
#endif // if HAVE_SECURITY

    def _add_writer_info(self, writer_data) :
        self._cvEntitiesInfoList.acquire()
        self._mapWriterInfoList[writer_data.guid()] = writer_data

        topic_name_str = writer_data.topicName().to_string()
        if (topic_name_str in self._mapTopicCountList) :
            self._mapTopicCountList[topic_name_str] += 1
        else :
            self._mapTopicCountList[topic_name_str] = 1

        for partition in writer_data.m_qos.m_partition.names() :
            if (partition in self._mapPartitionCountList) :
                self._mapPartitionCountList[partition] += 1
            else :
                self._mapPartitionCountList[partition] = 1

        self._cvEntitiesInfoList.notify()
        self._cvEntitiesInfoList.release()


    def _change_writer_info(self, writer_data) :
        self._cvEntitiesInfoList.acquire()

        assert(writer_data.guid() in self._mapWriterInfoList)
        old_writer_data = self._mapWriterInfoList[writer_data.guid()]
        self._mapWriterInfoList[writer_data.guid()] = writer_data

        assert(self._mapTopicCountList[writer_data.topicName().to_string()] > 0)

        for partition in old_writer_data.m_qos.m_partition.names() :
            assert(partition in self._mapPartitionCountList)
            self._mapPartitionCountList[partition] -= 1
            if (self._mapPartitionCountList[partition] == 0) :
                self._mapPartitionCountList.pop(partition)

        for partition in writer_data.m_qos.m_partition.names() :
            if (partition in self._mapPartitionCountList) :
                self._mapPartitionCountList[partition] += 1
            else :
                self._mapPartitionCountList[partition] = 1

        self._cvEntitiesInfoList.notify()
        self._cvEntitiesInfoList.release()

    def _add_reader_info(self, reader_data) :
        self._cvEntitiesInfoList.acquire()
        self._mapReaderInfoList[reader_data.guid()] = reader_data

        topic_name_str = reader_data.topicName().to_string()
        if (topic_name_str in self._mapTopicCountList) :
            self._mapTopicCountList[topic_name_str] += 1
        else :
            self._mapTopicCountList[topic_name_str] = 1

        for partition in reader_data.m_qos.m_partition.names() :
            if (partition in self._mapPartitionCountList) :
                self._mapPartitionCountList[partition] += 1
            else :
                self._mapPartitionCountList[partition] = 1

        self._cvEntitiesInfoList.notify()
        self._cvEntitiesInfoList.release()


    def _change_reader_info(self, reader_data) :
        self._cvEntitiesInfoList.acquire()

        assert(reader_data.guid() in self._mapReaderInfoList)
        old_reader_data = self._mapReaderInfoList[reader_data.guid()]
        self._mapReaderInfoList[reader_data.guid()] = reader_data

        assert(self._mapTopicCountList[reader_data.topicName().to_string()] > 0)

        for partition in old_reader_data.m_qos.m_partition.names() :
            assert(partition in self._mapPartitionCountList)
            self._mapPartitionCountList[partition] -= 1
            if (self._mapPartitionCountList[partition] == 0) :
                self._mapPartitionCountList.pop(partition)

        for partition in reader_data.m_qos.m_partition.names() :
            if (partition in self._mapPartitionCountList) :
                self._mapPartitionCountList[partition] += 1
            else :
                self._mapPartitionCountList[partition] = 1

        self._cvEntitiesInfoList.notify()
        self._cvEntitiesInfoList.release()

    def _remove_writer_info(self, writer_data) :
        self._cvEntitiesInfoList.acquire()

        assert(writer_data.guid() in self._mapWriterInfoList)
        self._mapWriterInfoList.pop(writer_data.guid())
        
        topic_name_str = writer_data.topicName().to_string()
        assert(self._mapTopicCountList[topic_name_str] > 0)
        self._mapTopicCountList[topic_name_str] -= 1
        if (self._mapTopicCountList[topic_name_str] == 0) :
            self._mapTopicCountList.pop(topic_name_str)

        for partition in writer_data.m_qos.m_partition.names() :
            assert(partition in self._mapPartitionCountList)
            self._mapPartitionCountList[partition] -= 1
            if (self._mapPartitionCountList[partition] == 0) :
                self._mapPartitionCountList.pop(partition)

        self._cvEntitiesInfoList.notify()
        self._cvEntitiesInfoList.release()

    def _remove_reader_info(self, reader_data) :
        self._cvEntitiesInfoList.acquire()
        assert(reader_data.guid() in self._mapReaderInfoList)
        self._mapReaderInfoList.pop(reader_data.guid())
        
        topic_name_str = reader_data.topicName().to_string()
        assert(self._mapTopicCountList[topic_name_str] > 0)
        self._mapTopicCountList[topic_name_str] -= 1
        if (self._mapTopicCountList[topic_name_str] == 0) :
            self._mapTopicCountList.pop(topic_name_str)

        for partition in reader_data.m_qos.m_partition.names() :
            assert(partition in self._mapPartitionCountList)
            self._mapPartitionCountList[partition] -= 1
            if (self._mapPartitionCountList[partition] == 0) :
                self._mapPartitionCountList.pop(partition)

        self._cvEntitiesInfoList.notify()
        self._cvEntitiesInfoList.release()
