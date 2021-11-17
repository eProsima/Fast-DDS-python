# Copyright 2021 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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

import TestTypes
import fastdds_wrapper as fastdds
from blackbox_common import *
from PubSubReader import PubSubReader
from PubSubWriter import PubSubWriter

from time import sleep
import copy

class TestPubSubBasic(TestCase):

    def test_PubSubAsNonReliableHelloworld(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.init()
        self.assertTrue(reader.isInitialized())

        writer.reliability(fastdds.BEST_EFFORT_RELIABILITY_QOS).init()
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery()
        reader.wait_discovery()

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_at_least(2)


    def test_AsyncPubSubAsNonReliableHelloworld(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.init()
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).asynchronously(fastdds.ASYNCHRONOUS_PUBLISH_MODE).init()
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery()
        reader.wait_discovery()

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_at_least(2)


    def test_PubSubAsReliableHelloworld(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).init()
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).init()
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery()
        reader.wait_discovery()

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()


    def test_AsyncPubSubAsReliableHelloworld(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).init()
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).asynchronously(fastdds.ASYNCHRONOUS_PUBLISH_MODE).init()
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery()
        reader.wait_discovery()

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()


    def test_PubSubAsReliableData64kb(self):
        reader = PubSubReader(TestTypes.Data64kb, TestTypes.Data64kbPubSubType, self.id())
        writer = PubSubWriter(TestTypes.Data64kb, TestTypes.Data64kbPubSubType, self.id())

        reader.history_depth(10).reliability(fastdds.RELIABLE_RELIABILITY_QOS).init()
        self.assertTrue(reader.isInitialized())

        writer.history_depth(10).init()
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery()
        reader.wait_discovery()

        data = default_data64kb_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()


    def test_PubSubMoreThan256Unacknowledged(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        writer.history_kind(fastdds.KEEP_ALL_HISTORY_QOS).durability_kind(fastdds.TRANSIENT_LOCAL_DURABILITY_QOS).init()
        self.assertTrue(writer.isInitialized())

        data = default_helloworld_data_generator()
        expected_data = copy.copy(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)

        reader.reliability(fastdds.RELIABLE_RELIABILITY_QOS).history_kind(fastdds.KEEP_ALL_HISTORY_QOS).durability_kind(fastdds.TRANSIENT_LOCAL_DURABILITY_QOS).init()
        self.assertTrue(reader.isInitialized())

        reader.startReception(expected_data)
        reader.block_for_all()
        self.assertTrue(writer.waitForAllAcked(10))


    def test_PubSubAsReliableHelloworldMulticastDisabled(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).disable_multicast(0).init()
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).disable_multicast(1).init()
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery()
        reader.wait_discovery()

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()
        self.assertTrue(writer.waitForAllAcked(10))


    def test_ReceivedDynamicDataWithNoSizeLimit(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.history_depth(100).partition("A").reliability(fastdds.RELIABLE_RELIABILITY_QOS).init();
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).partition("A").partition("B").partition("C").init();
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery(3)
        reader.wait_discovery(3)

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()


    '''
    # Fails because the user data cannot be set in python
    def test_ReceivedDynamicDataWithNoSizeLimit(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.history_depth(100).partition("A").reliability(fastdds.RELIABLE_RELIABILITY_QOS).init();
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).partition("A").partition("B").partition("C").userData({'a', 'b', 'c', 'd'}).init();
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery(3)
        reader.wait_discovery(3)

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()

    # Fails because the user data cannot be set in python
    def test_ReceivedDynamicDataWithNoSizeLimit(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.user_data_max_size(4).partitions_max_size(28).history_depth(100).partition("A").history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).init();
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).partition("A").partition("B").partition("C").userData({'a', 'b', 'c', 'd'}).init();
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery(3)
        reader.wait_discovery(3)

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()


    # Fails because the user data cannot be set in python
    def test_ReceivedUserDataExceedsSizeLimit(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.user_data_max_size(4).history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).init();
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).userData({'a', 'b', 'c', 'd', 'e', 'f'}).init();
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        writer.wait_discovery(3)
        reader.wait_discovery(3)

        data = default_helloworld_data_generator()
        reader.startReception(data)
        writer.send(data)
        self.assertTrue(len(data) == 0)
        reader.block_for_all()
    '''

    def test_ReceivedPartitionDataExceedsSizeLimit(self):
        reader = PubSubReader(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())
        writer = PubSubWriter(TestTypes.HelloWorld, TestTypes.HelloWorldPubSubType, self.id())

        reader.partitions_max_size(20).partition("A").history_depth(100).reliability(fastdds.RELIABLE_RELIABILITY_QOS).init();
        self.assertTrue(reader.isInitialized())

        writer.history_depth(100).partition("A").partition("B").partition("C").init();
        self.assertTrue(writer.isInitialized())

        # wait for discovery
        self.assertTrue(writer.wait_discovery(3))
        self.assertTrue(reader.wait_discovery(3))

'''

TEST_P(PubSubBasic, ReceivedPropertiesDataWithinSizeLimit)
{
    char* value = nullptr;
    std::string TOPIC_RANDOM_NUMBER;
    std::string W_UNICAST_PORT_RANDOM_NUMBER_STR;
    std::string R_UNICAST_PORT_RANDOM_NUMBER_STR;
    std::string MULTICAST_PORT_RANDOM_NUMBER_STR;

    // Get environment variables.
    value = std::getenv("TOPIC_RANDOM_NUMBER");
    if (value != nullptr)
    {
        TOPIC_RANDOM_NUMBER = value;
    }
    else
    {
        TOPIC_RANDOM_NUMBER = "1";
    }
    value = std::getenv("W_UNICAST_PORT_RANDOM_NUMBER");
    if (value != nullptr)
    {
        W_UNICAST_PORT_RANDOM_NUMBER_STR = value;
    }
    else
    {
        W_UNICAST_PORT_RANDOM_NUMBER_STR = "7411";
    }
    int32_t W_UNICAST_PORT_RANDOM_NUMBER = stoi(W_UNICAST_PORT_RANDOM_NUMBER_STR);
    value = std::getenv("R_UNICAST_PORT_RANDOM_NUMBER");
    if (value != nullptr)
    {
        R_UNICAST_PORT_RANDOM_NUMBER_STR = value;
    }
    else
    {
        R_UNICAST_PORT_RANDOM_NUMBER_STR = "7421";
    }
    int32_t R_UNICAST_PORT_RANDOM_NUMBER = stoi(R_UNICAST_PORT_RANDOM_NUMBER_STR);
    value = std::getenv("MULTICAST_PORT_RANDOM_NUMBER");
    if (value != nullptr)
    {
        MULTICAST_PORT_RANDOM_NUMBER_STR = value;
    }
    else
    {
        MULTICAST_PORT_RANDOM_NUMBER_STR = "7400";
    }
    int32_t MULTICAST_PORT_RANDOM_NUMBER = stoi(MULTICAST_PORT_RANDOM_NUMBER_STR);

    Locator_t LocatorBuffer;

    PubSubWriter<HelloWorldType> writer(TEST_TOPIC_NAME);

    LocatorList_t WriterUnicastLocators;
    LocatorBuffer.kind = LOCATOR_KIND_UDPv4;
    LocatorBuffer.port = static_cast<uint16_t>(W_UNICAST_PORT_RANDOM_NUMBER);
    IPLocator::setIPv4(LocatorBuffer, 127, 0, 0, 1);
    WriterUnicastLocators.push_back(LocatorBuffer);

    LocatorList_t WriterMulticastLocators;
    LocatorBuffer.port = static_cast<uint16_t>(MULTICAST_PORT_RANDOM_NUMBER);
    WriterMulticastLocators.push_back(LocatorBuffer);

    writer.static_discovery("file://PubSubWriter.xml").
            unicastLocatorList(WriterUnicastLocators).multicastLocatorList(WriterMulticastLocators).
            setPublisherIDs(1,
            2).setManualTopicName(std::string("BlackBox_StaticDiscovery_") + TOPIC_RANDOM_NUMBER).init();

    ASSERT_TRUE(writer.isInitialized());

    PubSubReader<HelloWorldType> reader(TEST_TOPIC_NAME);

    LocatorList_t ReaderUnicastLocators;
    LocatorBuffer.port = static_cast<uint16_t>(R_UNICAST_PORT_RANDOM_NUMBER);
    ReaderUnicastLocators.push_back(LocatorBuffer);

    LocatorList_t ReaderMulticastLocators;
    LocatorBuffer.port = static_cast<uint16_t>(MULTICAST_PORT_RANDOM_NUMBER);
    ReaderMulticastLocators.push_back(LocatorBuffer);

    //Expected properties have exactly size 92
    reader.properties_max_size(92).
            static_discovery("file://PubSubReader.xml").
            unicastLocatorList(ReaderUnicastLocators).multicastLocatorList(ReaderMulticastLocators).
            setSubscriberIDs(3,
            4).setManualTopicName(std::string("BlackBox_StaticDiscovery_") + TOPIC_RANDOM_NUMBER).init();

    ASSERT_TRUE(reader.isInitialized());

    // Wait for discovery.
    writer.wait_discovery(std::chrono::seconds(3));
    reader.wait_discovery(std::chrono::seconds(3));

    ASSERT_TRUE(writer.is_matched());
    ASSERT_TRUE(reader.is_matched());
}

TEST_P(PubSubBasic, ReceivedPropertiesDataExceedsSizeLimit)
{
    char* value = nullptr;
    std::string TOPIC_RANDOM_NUMBER;
    std::string W_UNICAST_PORT_RANDOM_NUMBER_STR;
    std::string R_UNICAST_PORT_RANDOM_NUMBER_STR;
    std::string MULTICAST_PORT_RANDOM_NUMBER_STR;

    // Get environment variables.
    value = std::getenv("TOPIC_RANDOM_NUMBER");
    if (value != nullptr)
    {
        TOPIC_RANDOM_NUMBER = value;
    }
    else
    {
        TOPIC_RANDOM_NUMBER = "1";
    }
    value = std::getenv("W_UNICAST_PORT_RANDOM_NUMBER");
    if (value != nullptr)
    {
        W_UNICAST_PORT_RANDOM_NUMBER_STR = value;
    }
    else
    {
        W_UNICAST_PORT_RANDOM_NUMBER_STR = "7411";
    }
    int32_t W_UNICAST_PORT_RANDOM_NUMBER = stoi(W_UNICAST_PORT_RANDOM_NUMBER_STR);
    value = std::getenv("R_UNICAST_PORT_RANDOM_NUMBER");
    if (value != nullptr)
    {
        R_UNICAST_PORT_RANDOM_NUMBER_STR = value;
    }
    else
    {
        R_UNICAST_PORT_RANDOM_NUMBER_STR = "7421";
    }
    int32_t R_UNICAST_PORT_RANDOM_NUMBER = stoi(R_UNICAST_PORT_RANDOM_NUMBER_STR);
    value = std::getenv("MULTICAST_PORT_RANDOM_NUMBER");
    if (value != nullptr)
    {
        MULTICAST_PORT_RANDOM_NUMBER_STR = value;
    }
    else
    {
        MULTICAST_PORT_RANDOM_NUMBER_STR = "7400";
    }
    int32_t MULTICAST_PORT_RANDOM_NUMBER = stoi(MULTICAST_PORT_RANDOM_NUMBER_STR);

    Locator_t LocatorBuffer;

    PubSubWriter<HelloWorldType> writer(TEST_TOPIC_NAME);

    LocatorList_t WriterUnicastLocators;
    LocatorBuffer.kind = LOCATOR_KIND_UDPv4;
    LocatorBuffer.port = static_cast<uint16_t>(W_UNICAST_PORT_RANDOM_NUMBER);
    IPLocator::setIPv4(LocatorBuffer, 127, 0, 0, 1);
    WriterUnicastLocators.push_back(LocatorBuffer);

    LocatorList_t WriterMulticastLocators;
    LocatorBuffer.port = static_cast<uint16_t>(MULTICAST_PORT_RANDOM_NUMBER);
    WriterMulticastLocators.push_back(LocatorBuffer);

    writer.static_discovery("file://PubSubWriter.xml").
            unicastLocatorList(WriterUnicastLocators).multicastLocatorList(WriterMulticastLocators).
            setPublisherIDs(1,
            2).setManualTopicName(std::string("BlackBox_StaticDiscovery_") + TOPIC_RANDOM_NUMBER).init();

    ASSERT_TRUE(writer.isInitialized());

    PubSubReader<HelloWorldType> reader(TEST_TOPIC_NAME);

    LocatorList_t ReaderUnicastLocators;
    LocatorBuffer.port = static_cast<uint16_t>(R_UNICAST_PORT_RANDOM_NUMBER);
    ReaderUnicastLocators.push_back(LocatorBuffer);

    LocatorList_t ReaderMulticastLocators;
    LocatorBuffer.port = static_cast<uint16_t>(MULTICAST_PORT_RANDOM_NUMBER);
    ReaderMulticastLocators.push_back(LocatorBuffer);

    //Expected properties have size 92
    reader.properties_max_size(50)
            .static_discovery("file://PubSubReader.xml")
            .unicastLocatorList(ReaderUnicastLocators).multicastLocatorList(ReaderMulticastLocators)
            .setSubscriberIDs(3,
            4).setManualTopicName(std::string("BlackBox_StaticDiscovery_") + TOPIC_RANDOM_NUMBER).init();

    ASSERT_TRUE(reader.isInitialized());

    // Wait for discovery.
    writer.wait_discovery(std::chrono::seconds(3));
    reader.wait_discovery(std::chrono::seconds(3));

    ASSERT_FALSE(writer.is_matched());
    ASSERT_FALSE(reader.is_matched());
}

TEST_P(PubSubBasic, unique_flows_one_writer_two_readers)
{
    PubSubParticipant<HelloWorldType> readers(0, 2, 0, 2);
    PubSubWriter<HelloWorldType> writer(TEST_TOPIC_NAME);

    PropertyPolicy properties;
    properties.properties().emplace_back("fastdds.unique_network_flows", "");

    readers.sub_topic_name(TEST_TOPIC_NAME).sub_property_policy(properties).reliability(RELIABLE_RELIABILITY_QOS);

    ASSERT_TRUE(readers.init_participant());
    ASSERT_TRUE(readers.init_subscriber(0));
    ASSERT_TRUE(readers.init_subscriber(1));

    writer.history_depth(100).init();

    ASSERT_TRUE(writer.isInitialized());

    // Wait for discovery.
    writer.wait_discovery();
    readers.sub_wait_discovery();

    // Send data
    auto data = default_helloworld_data_generator();
    writer.send(data);
    // In this test all data should be sent.
    ASSERT_TRUE(data.empty());
    // Block until readers have acknowledged all samples.
    EXPECT_TRUE(writer.waitForAllAcked(std::chrono::seconds(30)));
}

template<typename T>
static void two_consecutive_writers(
        PubSubReader<T>& reader,
        PubSubWriter<T>& writer,
        bool block_for_all)
{
    writer.init();
    EXPECT_TRUE(writer.isInitialized());

    // Wait for discovery.
    writer.wait_discovery();
    reader.wait_discovery();

    auto complete_data = default_helloworld_data_generator();

    reader.startReception(complete_data);

    // Send data
    writer.send(complete_data);
    EXPECT_TRUE(complete_data.empty());

    if (block_for_all)
    {
        reader.block_for_all();
    }
    else
    {
        reader.block_for_at_least(2);
    }
    reader.stopReception();

    writer.destroy();

    // Wait for undiscovery
    reader.wait_writer_undiscovery();
}

TEST_P(PubSubBasic, BestEffortTwoWritersConsecutives)
{
    // Pull mode incompatible with best effort
    if (use_pull_mode)
    {
        return;
    }

    PubSubReader<HelloWorldType> reader(TEST_TOPIC_NAME);

    reader.history_depth(10).init();
    EXPECT_TRUE(reader.isInitialized());

    for (int i = 0; i < 2; ++i)
    {
        PubSubWriter<HelloWorldType> writer(TEST_TOPIC_NAME);
        writer.history_depth(10).reliability(BEST_EFFORT_RELIABILITY_QOS);
        two_consecutive_writers(reader, writer, false);
    }
}


TEST_P(PubSubBasic, ReliableVolatileTwoWritersConsecutives)
{
    PubSubReader<HelloWorldType> reader(TEST_TOPIC_NAME);

    reader.history_depth(10).reliability(RELIABLE_RELIABILITY_QOS).init();
    EXPECT_TRUE(reader.isInitialized());

    for (int i = 0; i < 2; ++i)
    {
        PubSubWriter<HelloWorldType> writer(TEST_TOPIC_NAME);
        writer.history_depth(10).durability_kind(VOLATILE_DURABILITY_QOS);
        two_consecutive_writers(reader, writer, true);
    }
}

TEST_P(PubSubBasic, ReliableTransientLocalTwoWritersConsecutives)
{
    PubSubReader<HelloWorldType> reader(TEST_TOPIC_NAME);

    reader.history_depth(10).reliability(RELIABLE_RELIABILITY_QOS).durability_kind(TRANSIENT_LOCAL_DURABILITY_QOS);
    reader.init();
    EXPECT_TRUE(reader.isInitialized());

    for (int i = 0; i < 2; ++i)
    {
        PubSubWriter<HelloWorldType> writer(TEST_TOPIC_NAME);
        writer.history_depth(10).reliability(RELIABLE_RELIABILITY_QOS);
        two_consecutive_writers(reader, writer, true);
    }
}

#ifdef INSTANTIATE_TEST_SUITE_P
#define GTEST_INSTANTIATE_TEST_MACRO(x, y, z, w) INSTANTIATE_TEST_SUITE_P(x, y, z, w)
#else
#define GTEST_INSTANTIATE_TEST_MACRO(x, y, z, w) INSTANTIATE_TEST_CASE_P(x, y, z, w)
#endif // ifdef INSTANTIATE_TEST_SUITE_P

GTEST_INSTANTIATE_TEST_MACRO(PubSubBasic,
        PubSubBasic,
        testing::Combine(testing::Values(TRANSPORT, INTRAPROCESS, DATASHARING), testing::Values(false, true)),
        [](const testing::TestParamInfo<PubSubBasic::ParamType>& info)
        {
            bool pull_mode = std::get<1>(info.param);
            std::string suffix = pull_mode ? "_pull_mode" : "";
            switch (std::get<0>(info.param))
            {
                case INTRAPROCESS:
                    return "Intraprocess" + suffix;
                    break;
                case DATASHARING:
                    return "Datasharing" + suffix;
                    break;
                case TRANSPORT:
                default:
                    return "Transport" + suffix;
            }

        });
'''