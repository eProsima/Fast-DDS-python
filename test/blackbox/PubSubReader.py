# Copyright 2021 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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

import fastdds_wrapper as fastdds
from blackbox_common import *

from threading import Thread, Lock, Condition
from os import getpid
from socket import gethostname
import copy

class PubSubReader :

    class ParticipantListener(fastdds.DomainParticipantListener) :

        def __init__(self, reader) :
            self._reader = reader
            super().__init__()

        def on_participant_discovery(self, domain_participant, info) :
            if (self._reader._onDiscovery != None):
                self._reader._cvDiscovery.acquire()
                self._reader._discovery_result |= self._reader._onDiscovery(info)
                self._reader._cvDiscovery.notify()
                self._reader._cvDiscovery.release()

            if (info.status == fastdds.ParticipantDiscoveryInfo.DISCOVERED_PARTICIPANT) :
                self._reader._participant_matched()
            elif (info.status == fastdds.ParticipantDiscoveryInfo.REMOVED_PARTICIPANT or
                    info.status == fastdds.ParticipantDiscoveryInfo.DROPPED_PARTICIPANT) :
                    self._reader._participant_unmatched()

        def on_publisher_discovery(self, domain_participant, info) :
            if (self._reader._onEndpointDiscovery != None) :
                self._reader._cvDiscovery.acquire()
                self._reader._discovery_result |= self._reader._onEndpointDiscovery(info)
                self._reader._cvDiscovery.notify()
                self._reader._cvDiscovery.release()

# if HAVE_SECURITY
        def onParticipantAuthentication(self, domain_participant, info) :
            if (info.status == fastdds.ParticipantAuthenticationInfo.AUTHORIZED_PARTICIPANT) :
                self._reader._authorized()
            elif (info.status == fastdds.ParticipantAuthenticationInfo.UNAUTHORIZED_PARTICIPANT) :
                self._reader._unauthorized()
# endif HAVE_SECURITY


    class Listener (fastdds.DataReaderListener) :
        def __init__(self, reader) :
            self._reader = reader
            self._times_deadline_missed = 0
            super().__init__()

        def on_data_available(self, datareader) :
            assert(datareader)
            self._reader._message_receive_cv.acquire()
            self._reader._message_receive_count += 1
            self._reader._message_receive_cv.notify()
            self._reader._message_receive_cv.release()

            if (self._reader._receiving) :
                while self._reader.receive_one(datareader) :
                    pass

        def on_subscription_matched(self, datareader, info) :
            if (0 < info.current_count_change) :
                print ("Subscriber matched publisher {}".format(info.last_publication_handle))
                self._reader._matched()
            else :
                print ("Subscriber unmatched publisher {}".format(info.last_publication_handle))
                self._reader._unmatched()

        def on_requested_deadline_missed(self, datareader, status) :
            self._times_deadline_missed = status.total_count

        def on_requested_incompatible_qos(self, datareader, status) :
            self._reader.incompatible_qos(status)

        def on_liveliness_changed(self, datareader, status) :
            self._reader.set_liveliness_changed_status(status)

            if (status.alive_count_change == 1) :
                self._reader.liveliness_recovered()

            elif (status.not_alive_count_change == 1) :
                self._reader.liveliness_lost()


        def  missed_deadlines(self) :
            return self._times_deadline_missed

    def __init__(self, data_type, topic_data_type, topic_name, take=True, statistics=False) :
        self._participant_listener = PubSubReader.ParticipantListener(self)
        self._listener = PubSubReader.Listener(self)
        self._participant = None
        self._participant_qos = fastdds.DomainParticipantQos()
        self._topic = None
        self._subscriber = None
        self._subscriber_qos = fastdds.SubscriberQos()
        self._datareader = None
        self._datareader_qos = fastdds.DataReaderQos()
        self._status_mask = fastdds.StatusMask.all()
        self._topic_name = topic_name
        self._participant_guid = fastdds.GUID_t_unknown()
        self._datareader_guid = fastdds.GUID_t_unknown()
        self._initialized = False
        self._total_msgs = []
        self._cv = Condition()
        self._cvDiscovery = Condition()
        self._matched_writers = 0
        self._matched_participants = 0
        self._receiving = 0
        self._data_type = data_type
        self._topic_data_type = topic_data_type
        self._last_seq = {}
        self._current_processed_count = 0
        self._number_samples_expected = 0
        self._discovery_result = False
        self._xml_file = ""
        self._participant_profile = ""
        self._datareader_profile = ""
        self._onDiscovery = None
        self._onEndpointDiscovery = None
        self._take = take
        self._statistics = statistics
# if HAVE_SECURITY
        self._cvAuthentication = Condition()
        self._authorized_participants = 0
        self._unauthorized = 0
# endif HAVE_SECURITY
        self._liveliness_cv = Condition()
        self._times_liveliness_lost = 0
        self._times_liveliness_recovered = 0
        self._liveliness_changed_status = fastdds.LivelinessChangedStatus()
        self._incompatible_qos_cv = Condition()
        self._times_incompatible_qos = 0
        self._last_incompatible_qos = fastdds.INVALID_QOS_POLICY_ID
        self._message_receive_cv = Condition()
        self._message_receive_count = 0


        # Generate topic name
        if (not statistics) :
            self._topic_name = "{topic}_{host}_{pid}".format(topic=self._topic_name, host=gethostname(), pid=getpid())

        if (enable_datasharing) :
            self._datareader_qos.data_sharing().automatic()
        else :
            self._datareader_qos.data_sharing().off()

        # By default, memory mode is preallocated (the most restrictive)
        self._datareader_qos.endpoint().history_memory_policy = fastdds.PREALLOCATED_MEMORY_MODE

        # By default, heartbeat period delay is 100 milliseconds.
        self._datareader_qos.reliable_reader_qos().times.heartbeatResponseDelay.seconds = 0
        self._datareader_qos.reliable_reader_qos().times.heartbeatResponseDelay.nanosec = 100000000


    def __del__(self) :
        self.destroy()

    def get_native_reader(self) :
        return self._datareader

    def init(self) :
        assert(not self._initialized)
        self._matched_writers = 0

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

            # Create subscriber
            self.createSubscriber()

    def createSubscriber(self) :
        if (self._participant != None) :
            self._subscriber = self._participant.create_subscriber(self._subscriber_qos)
            assert(self._subscriber != None)
            assert(self._subscriber.is_enabled())

            if (self._xml_file) :
                if (self._datareader_profile) :
                    self._datareader = self._subscriber.create_datareader_with_profile(self._topic, self._datareader_profile, self._listener,
                                    self._status_mask)
                    assert(self._datareader != None)
                    assert(self._datareader.is_enabled())
            if (self._datareader == None) :
                self._datareader = self._subscriber.create_datareader(self._topic, self._datareader_qos, self._listener, self._status_mask)

            if (self._datareader != None) :
                print ("Created datareader {guid} for topic {topic}".format (guid=self._datareader.guid(), topic=self._topic_name))
                self._initialized = True;
                self._datareader_guid = self._datareader.guid()

    def isInitialized(self) :
        return self._initialized

    def destroy(self) :
        if (self._participant != None) :
            if (self._datareader) :
                self._subscriber.delete_datareader(self._datareader)
                self._datareader = None
            if (self._subscriber) :
                self._participant.delete_subscriber(self._subscriber)
                self._subscriber = None
            if (self._topic) :
                self._participant.delete_topic(self._topic)
                self._topic = None
            fastdds.DomainParticipantFactory.get_instance().delete_participant(self._participant)
            self._participant = None

        self.initialized_ = False

    def data_not_received(self) :
        self._cv.acquire()
        ret = self._total_msgs
        self._cv.release()
        return ret

    def startReception( self, msgs) :
        self._cv.acquire()
        self._total_msgs = copy.copy(msgs)
        self._number_samples_expected = len(self._total_msgs)
        self._current_processed_count = 0
        self._last_seq.clear()
        self._cv.release()

        print("Starting reception")
        while self.receive_one(self._datareader) :
            pass

        self._receiving = True
        return self.get_last_sequence_received()

    def stopReception(self) :
        self._receiving = False

    def wait_for_all_received(self, max_wait, num_messages) :
        if (num_messages == 0) :
            num_messages = self._number_samples_expected
        self._message_receive_cv.acquire()
        ret = self._message_receive_cv.wait(lambda : num_messages == self._message_receive_count, timeout=max_wait)
        self._message_receive_cv.release()
        return ret

    def block_for_all(self, max_wait=None) :
        return self.block(lambda : self._number_samples_expected == self._current_processed_count, max_wait)

    def block_for_seq(self, seq, max_wait=None) :
        return self.block(lambda : self.get_last_sequence_received() == seq, max_wait)

    def block_for_at_least(self, at_least, max_wait=None) :
        self.block(lambda : self._current_processed_count >= at_least, max_wait)
        return self._current_processed_count;

    def block(self, checker, max_wait=None) :
        self._cv.acquire()
        ret = self._cv.wait_for(checker, timeout=max_wait)
        self._cv.release()
        return ret

    def wait_discovery(self, timeout=None, min_writers=1) :
        self._cvDiscovery.acquire()
        print ("Reader is waiting discovery...")
        ret = self._cvDiscovery.wait_for(lambda : self._matched_writers >= min_writers, timeout)
        self._cvDiscovery.release()
        print("Reader discovery finished...")
        return ret

    def wait_participant_discovery(self, min_participants = 1, timeout = None) :
        ret_value = True
        self._cvDiscovery.acquire()
        print("Reader is waiting discovery of at least {} participants...".format(min_participants))
        ret_value = self._cvDiscovery.wait_for(lambda : self._matched_participants >= min_participants, timeout)
        self._cvDiscovery.release()

        if (ret_value) :
            print("Reader participant discovery finished successfully...")
        else :
            print("Reader participant discovery finished unsuccessfully...")

        return ret_value

    def wait_participant_undiscovery(self, timeout=None) :
        ret_value = True;
        self._cvDiscovery.acquire()
        print("Reader is waiting participant undiscovery...")
        ret_value = self._cvDiscovery.wait_for(lambda : self._matched_participants == 0, timeout)
        self._cvDiscovery.release()

        if (ret_value) :
            print("Reader participant undiscovery finished successfully...")
        else :
            print("Reader participant undiscovery finished unsuccessfully...")

        return ret_value


    def wait_writer_undiscovery(self) :
        self._cvDiscovery.acquire()
        print ("Reader is waiting removal...")
        self._cvDiscovery.wait_for(lambda : self._matched_writers == 0)
        self._cvDiscovery.release()
        print("Reader removal finished...")


    def wait_liveliness_recovered(self, times = 1) :
        self._liveliness_cv.acquire()
        self._liveliness_cv.wait_for(lambda : self._times_liveliness_recovered >= times)
        self._liveliness_cv.release()

    def wait_liveliness_lost(self, times = 1) :
        self._liveliness_cv.acquire()
        self._liveliness_cv.wait_for(lambda : self._times_liveliness_lost >= times)
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
        self._cvAuthentication.wait_for(lambda : self._authorized_participants > 0)
        self._cvAuthentication.release()
        print("Reader authorization finished...")

    def waitUnauthorized(self) :
        self._cvAuthentication.acquire()
        print ("Reader is waiting unauthorization...")
        self._cvAuthentication.wait_for(lambda : self._unauthorized > 0)
        self._cvAuthentication.release()
        print("Reader unauthorization finished...")
#endif // if HAVE_SECURITY

    def getReceivedCount(self) :
        return self._current_processed_count

    def get_last_sequence_received(self) :
        #last_seq is a list of pairs (tuples), we compare only the second term
        if not self._last_seq :
            return fastdds.SequenceNumber_t()

        ret = max(self._last_seq, key=lambda x : x[1])
        return ret[1]

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
        self._datareader_qos.reliability().kind = kind
        return self

    def mem_policy(self, mem_policy) :
        self._datareader_qos.endpoint().history_memory_policy = mem_policy
        return self

    def deadline_period(self, deadline_period) :
        self._datareader_qos.deadline().period = deadline_period
        return self

    def update_deadline_period(self, deadline_period) :
        datareader_qos = fastdds.DataReaderQos()
        self._datareader.get_qos(datareader_qos)
        datareader_qos.deadline().period = deadline_period

        return self._datareader.set_qos(datareader_qos) == fastdds.ReturnCode_t.RETCODE_OK

    def liveliness_kind(self, kind) :
        self._datareader_qos.liveliness().kind = kind
        return self

    def liveliness_lease_duration(self, lease_duration) :
        self._datareader_qos.liveliness().lease_duration = lease_duration
        return self

    def latency_budget_duration(self, latency_duration) :
        self._datareader_qos.latency_budget().duration = latency_duration
        return self

    def get_latency_budget_duration(self) :
        return self._datareader_qos.latency_budget().duration

    def lifespan_period(self, lifespan_period) :
        self._datareader_qos.lifespan().duration = lifespan_period
        return self

    def keep_duration(self, duration) :
        self._datareader_qos.reliable_reader_qos().disable_positive_ACKs.enabled = True
        self._datareader_qos.reliable_reader_qos().disable_positive_ACKs.duration = duration
        return self

    def history_kind(self, kind) :
        self._datareader_qos.history().kind = kind
        return self

    def history_depth(self, depth) :
        self._datareader_qos.history().depth = depth
        return self

    def disable_builtin_transport(self,) :
        self._participant_qos.transport().use_builtin_transports = False
        return self

    def add_user_transport_to_pparams(self, userTransportDescriptor) :
        self._participant_qos.transport().user_transports.push_back(userTransportDescriptor)
        return self

    def resource_limits_allocated_samples(self, initial) :
        self._datareader_qos.resource_limits().allocated_samples = initial
        return self

    def resource_limits_max_samples(self, max) :
        self._datareader_qos.resource_limits().max_samples = max
        return self

    def resource_limits_max_instances(self, max) :
        self._datareader_qos.resource_limits().max_instances = max
        return self

    def resource_limits_max_samples_per_instance(self, max) :
        self._datareader_qos.resource_limits().max_samples_per_instance = max
        return self

    def matched_writers_allocation(self, initial, maximum) :
        self._datareader_qos.reader_resource_limits().matched_publisher_allocation.initial = initial
        self._datareader_qos.reader_resource_limits().matched_publisher_allocation.maximum = maximum
        return self

    def expect_no_allocs(self) :
        # TODO(Mcc): Add no allocations check code when feature is completely ready
        return self

    def heartbeatResponseDelay(self, secs, frac) :
        self._datareader_qos.reliable_reader_qos().times.heartbeatResponseDelay.seconds = secs
        self._datareader_qos.reliable_reader_qos().times.heartbeatResponseDelay.fraction = frac
        return self

    def unicastLocatorList(self, unicast_locators) :
        self._datareader_qos.endpoint().unicast_locator_list = unicast_locators
        return self

    def add_to_unicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._datareader_qos.endpoint().unicast_locator_list.push_back(loc)

        return self

    def multicastLocatorList(self, multicast_locators) :
        self._datareader_qos.endpoint().multicast_locators = multicast_locators
        return self

    def add_to_multicast_locator_list(self, ip, port) :
        loc = fastdds.Locator_t()
        if (not fastdds.IPLocator.setIPv4(loc, ip)) :
            loc.kind = fastdds.LOCATOR_KIND_UDPv6
            if (not fastdds.IPLocator.setIPv6(loc, ip)) :
                return self

        loc.port = port
        self._datareader_qos.endpoint().multicast_locator_list.push_back(loc)

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

    def ignore_participant_flags(self, flags) :
        self._participant_qos.wire_protocol().builtin.discovery_config.ignoreParticipantFlags = flags
        return self

    def socket_buffer_size(self, sockerBufferSize) :
        self._participant_qos.transport().listen_socket_buffer_size = sockerBufferSize
        return self

    def durability_kind(self, kind) :
        self._datareader_qos.durability().kind = kind
        return self

    def static_discovery(self, filename) :
        self._participant_qos.wire_protocol().builtin.discovery_config.use_SIMPLE_EndpointDiscoveryProtocol = False
        self._participant_qos.wire_protocol().builtin.discovery_config.use_STATIC_EndpointDiscoveryProtocol = True
        self._participant_qos.wire_protocol().builtin.discovery_config.static_edp_xml_config(filename)
        return self

    def setSubscriberIDs(self, UserID, EntityID) :
        self._datareader_qos.endpoint().user_defined_id = UserID
        self._datareader_qos.endpoint().entity_id = EntityID
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

    def property_policy(self, property_policy) :
        self._participant_qos.properties(property_policy)
        return self

    def entity_property_policy(self, property_policy) :
        self._datareader_qos.properties(property_policy)
        return self

    def partition(self, partition) :
        self._subscriber_qos.partition().push_back(partition)
        return self

    def userData(self, user_data) :
        self._participant_qos.user_data(user_data)
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

    def load_subscriber_attr(self, xml) :
        # TODO
        return self

    def participant_id(self, participantId) :
        self._participant_qos.wire_protocol().participant_id = participantId
        return self

    def datasharing_off(self) :
        self._datareader_qos.data_sharing().off()
        return self

    def datasharing_auto(self, domain_id) :
        self._datareader_qos.data_sharing().automatic(domain_id)
        return self

    def datasharing_auto(self, directory, domain_id) :
        self._datareader_qos.data_sharing().automatic(directory, domain_id)
        return self

    def datasharing_on(self, directory, domain_id) :
        self._datareader_qos.data_sharing().on(directory, domain_id)
        return self

#if HAVE_SQLITE3
    def make_persistent(self, filename, persistence_guid) :
        self._participant_qos.properties().properties().emplace_back("dds.persistence.plugin", "builtin.SQLITE3")
        self._participant_qos.properties().properties().emplace_back("dds.persistence.sqlite3.filename", filename)
        self._datareader_qos.durability().kind = fastdds.TRANSIENT_DURABILITY_QOS
        self._datareader_qos.properties().properties().emplace_back("dds.persistence.guid", persistence_guid)

        return self
#endif // if HAVE_SQLITE3

    def update_partition(self, partition) :
        self._subscriber_qos.partition().clear()
        self._subscriber_qos.partition().push_back(partition)
        return (fastdds.ReturnCode_t.RETCODE_OK == self._subscriber.set_qos(self._subscriber_qos))

    def clear_partitions(self) :
        self._subscriber_qos.partition().clear()
        return (fastdds.ReturnCode_t.RETCODE_OK == self._subscriber.set_qos(self._subscriber_qos))

    def wait_discovery_result(self) :
        self._cvDiscovery.acquire()
        print("Reader is waiting discovery result...")

        self._cvDiscovery.wait_for(lambda : self._discovery_result)
        print("Reader gets discovery result...")
        self._cvDiscovery.release()

    def setOnDiscoveryFunction( self, f) :
        self._cvDiscovery = f

    def setOnEndpointDiscoveryFunction(self, f) :
        self._onEndpointDiscovery_ = f

    def takeNextData( self, data) :
        dds_info = fastdds.SampleInfo()
        if (self._datareader.take_next_sample(data, dds_info) == fastdds.ReturnCode_t.RETCODE_OK) :
            self._current_processed_count+=1
            return True
        return False

    def missed_deadlines(self) :
        return self._listener.missed_deadlines()

    def liveliness_lost(self) :
        self._liveliness_cv.acquire()
        self._times_liveliness_lost += 1
        self._liveliness_cv.notify()
        self._liveliness_cv.release()

    def liveliness_recovered(self) :
        self._liveliness_cv.acquire()
        self._times_liveliness_recovered += 1
        self._liveliness_cv.notify()
        self._liveliness_cv.release()

    def set_liveliness_changed_status(self, status) :
        self._liveliness_cv.acquire()
        self._liveliness_changed_status = status
        self._liveliness_cv.release()

    def times_liveliness_lost(self) :
        self._liveliness_cv.acquire()
        ret = self._times_liveliness_lost
        self._liveliness_cv.release()
        return ret

    def times_liveliness_recovered(self) :
        self._liveliness_cv.acquire()
        ret = self._times_liveliness_recovered
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
        ret = fastdds.RequestedIncompatibleQosStatus()
        self._datareader.get_requested_incompatible_qos_status(ret)
        return ret

    def liveliness_changed_status(self) :
        self._liveliness_cv.acquire()
        ret = self._liveliness_changed_status
        self._liveliness_cv.release()
        return ret

    def get_liveliness_changed_status(self) :
        ret = fastdds.LivelinessChangedStatus()
        self._datareader.get_liveliness_changed_status(ret)
        return ret

    def is_matched(self) :
        return self._matched_writers > 0

    def set_xml_filename(self, name) :
        self._xml_file = name

    def set_participant_profile(self, profile) :
        self._participant_profile = profile

    def set_datareader_profile(self, profile) :
        self._datareader_profile = profile

    def get_statuscondition(self) :
        return self._datareader.get_statuscondition()

    def datareader_guid(self) :
        return self._datareader_guid

    def receive_one(self, datareader) :
        ret = False
        data = self._data_type()
        info = fastdds.SampleInfo()

        if (self._take) :
            success = self._datareader.take_next_sample(data, info)
        else :
            success = self._datareader.read_next_sample(data, info)
        if (success == fastdds.ReturnCode_t.RETCODE_OK) :
            ret = True
            self._cv.acquire()

            # Check order of changes
            if not (info.instance_handle in self._last_seq) :
                self._last_seq[info.instance_handle] = fastdds.SequenceNumber_t()
            assert self._last_seq[info.instance_handle] < info.sample_identity.sequence_number()
            self._last_seq[info.instance_handle] = fastdds.SequenceNumber_t(info.sample_identity.sequence_number().to64long())

            if (info.instance_state == fastdds.ALIVE_INSTANCE_STATE) :
                assert data in self._total_msgs
                self._total_msgs.remove(data)
                self._current_processed_count += 1
                default_receive_print(data);
                self._cv.notify()

            self._cv.release()
        return ret

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
        self._matched_writers += 1
        self._cvDiscovery.notify()
        self._cvDiscovery.release()

    def _unmatched(self) :
        self._cvDiscovery.acquire()
        self._matched_writers -= 1
        self._cvDiscovery.notify()
        self._cvDiscovery.release()

#if HAVE_SECURITY
    def _authorized(self) :
        self._cvAuthentication.acquire()
        self._authorized_participants += 1
        self._cvAuthentication.notify_all()
        self._cvAuthentication.release()

    def _unauthorized(self) :
        self._cvAuthentication.acquire()
        self._unauthorized += 1
        self._cvAuthentication.notify_all()
        self._cvAuthentication.release()
#endif // if HAVE_SECURITY
