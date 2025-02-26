import fastdds
import pytest
import time

class DataReaderListener (fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()

@pytest.fixture(params=['no_module', 'module'], autouse=True)
def data_type(request):
    if request.param == 'no_module':
        pytest.dds_type = __import__("test_complete")
    else:
        pytest.dds_type = __import__("eprosima.test.test_modules",
                                    fromlist=["test_modules"])

@pytest.fixture
def participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)

@pytest.fixture
def subscriber(participant):
    return participant.create_subscriber(fastdds.SUBSCRIBER_QOS_DEFAULT)


@pytest.fixture
def test_type():
    return fastdds.TypeSupport(pytest.dds_type.CompleteTestTypePubSubType())


@pytest.fixture
def test_keyed_type(test_type):
    test_type.set(pytest.dds_type.KeyedCompleteTestTypePubSubType())


@pytest.fixture
def topic(participant, test_type):
    participant.register_type(test_type, test_type.get_type_name())
    return participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def datareader_qos():
    return fastdds.DataReaderQos()


@pytest.fixture
def transient_datareader_qos(datareader_qos):
    datareader_qos.durability().kind = fastdds.TRANSIENT_LOCAL_DURABILITY_QOS
    datareader_qos.reliability().kind = fastdds.RELIABLE_RELIABILITY_QOS
    return datareader_qos


@pytest.fixture
def datareader(participant, topic, subscriber, datareader_qos):
    datareader = subscriber.create_datareader(topic, datareader_qos)

    yield datareader

    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))


@pytest.fixture
def writer_participant():
    factory = fastdds.DomainParticipantFactory.get_instance()
    return factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)


@pytest.fixture
def writer_topic(writer_participant, test_type):
    writer_participant.register_type(test_type, test_type.get_type_name())
    return writer_participant.create_topic(
            "Complete", test_type.get_type_name(), fastdds.TOPIC_QOS_DEFAULT)


@pytest.fixture
def publisher(writer_participant):
    return writer_participant.create_publisher(fastdds.PUBLISHER_QOS_DEFAULT)


@pytest.fixture
def datawriter(writer_participant, writer_topic, publisher):
    datawriter = publisher.create_datawriter(
            writer_topic, fastdds.DATAWRITER_QOS_DEFAULT)

    yield datawriter

    assert(fastdds.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.RETCODE_OK ==
           writer_participant.delete_topic(writer_topic))
    assert(fastdds.RETCODE_OK ==
           writer_participant.delete_publisher(publisher))
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(writer_participant))


def fill_keyed_complete_test_type(data):
    # Auxiliary StructTypes
    struct_type1 = pytest.dds_type.StructType()
    struct_type1.char_field('\x01')
    struct_type1.uint8_field(254)
    struct_type1.int16_field(-10)
    struct_type1.uint16_field(10)
    struct_type1.int32_field(-1000)
    struct_type1.uint32_field(1000)
    struct_type1.int64_field(-36000)
    struct_type1.uint64_field(36000)
    struct_type1.float_field(1.0)
    struct_type1.double_field(1200.5)
    struct_type1.bool_field(False)
    struct_type1.enum_field(pytest.dds_type.Color_RED)
    struct_type1.enum2_field(pytest.dds_type.Material_STONE)
    struct_type2 = pytest.dds_type.StructType()
    struct_type2.char_field('\x02')
    struct_type2.uint8_field(255)
    struct_type2.int16_field(10)
    struct_type2.uint16_field(35)
    struct_type2.int32_field(1000)
    struct_type2.uint32_field(200)
    struct_type2.int64_field(36000)
    struct_type2.uint64_field(128000)
    struct_type2.float_field(2.0)
    struct_type2.double_field(1202.5)
    struct_type2.bool_field(True)
    struct_type2.enum_field(pytest.dds_type.Color_BLUE)
    struct_type2.enum2_field(pytest.dds_type.Material_PLASTIC)
    struct_type3 = pytest.dds_type.StructType()
    struct_type3.char_field('\x03')
    struct_type3.uint8_field(1)
    struct_type3.int16_field(-20)
    struct_type3.uint16_field(60)
    struct_type3.int32_field(-2000)
    struct_type3.uint32_field(3000)
    struct_type3.int64_field(-1)
    struct_type3.uint64_field(3)
    struct_type3.float_field(3.0)
    struct_type3.double_field(3.5)
    struct_type3.bool_field(False)
    struct_type3.enum_field(pytest.dds_type.Color_MAGENTA)
    struct_type3.enum2_field(pytest.dds_type.Material_METAL)

    data.char_field('\x01')
    data.uint8_field(254)
    data.int16_field(-10)
    data.uint16_field(10)
    data.int32_field(-1000)
    data.uint32_field(1000)
    data.int64_field(-36000)
    data.uint64_field(36000)
    data.float_field(1.0)
    data.double_field(1202.5)
    data.bool_field(True)
    data.string_field("Test string")
    fixed_string = pytest.dds_type.fixed_string_16("Fixed string")
    data.fixed_string_field(fixed_string)
    data.enum_field(pytest.dds_type.Color_MAGENTA)
    data.enum2_field(pytest.dds_type.Material_METAL)
    data.struct_field().char_field('\x01')
    data.struct_field().uint8_field(254)
    data.struct_field().int16_field(-10)
    data.struct_field().uint16_field(10)
    data.struct_field().int32_field(-1000)
    data.struct_field().uint32_field(1000)
    data.struct_field().int64_field(-36000)
    data.struct_field().uint64_field(36000)
    data.struct_field().float_field(1.0)
    data.struct_field().double_field(1202.5)
    data.struct_field().bool_field(False)
    data.struct_field().string_field("Test string")
    data.struct_field().fixed_string_field("Fixed string")
    data.struct_field().enum_field(pytest.dds_type.Color_MAGENTA)
    data.struct_field().enum2_field(pytest.dds_type.Material_METAL)
    data.char_opt_field().set_value('\x01')
    data.uint8_opt_field().set_value(254)
    data.int16_opt_field().set_value(-10)
    data.uint16_opt_field().set_value(10)
    data.int32_opt_field().set_value(-1000)
    data.uint32_opt_field().set_value(1000)
    data.int64_opt_field().set_value(-36000)
    data.uint64_opt_field().set_value(36000)
    data.float_opt_field().set_value(1.0)
    data.double_opt_field().set_value(1202.5)
    data.bool_opt_field().set_value(True)
    data.string_opt_field().set_value("Test string")
    data.enum_opt_field().set_value(pytest.dds_type.Color_MAGENTA)
    struct_field = pytest.dds_type.StructType()
    struct_field.char_field('\x01')
    struct_field.uint8_field(254)
    struct_field.int16_field(-10)
    struct_field.uint16_field(10)
    struct_field.int32_field(-1000)
    struct_field.uint32_field(1000)
    struct_field.int64_field(-36000)
    struct_field.uint64_field(36000)
    struct_field.float_field(1.0)
    struct_field.double_field(1202.5)
    struct_field.bool_field(True)
    struct_field.string_field("Test string")
    struct_field.fixed_string_field("Fixed string")
    struct_field.enum_field(pytest.dds_type.Color_MAGENTA)
    struct_field.enum2_field(pytest.dds_type.Material_METAL)
    data.struct_opt_field().set_value(struct_field)
    data.array_char_field(['\x01', '\x02', '\x03'])
    data.array_uint8_field([254, 255, 1])
    data.array_int16_field([-10, 10, -20])
    data.array_uint16_field([10, 35, 60])
    data.array_int32_field([-1000, 1000, -2000])
    data.array_uint32_field([1000, 200, 3000])
    data.array_int64_field([-36000, 36000, -1])
    data.array_uint64_field([36000, 128000, 3])
    data.array_float_field([1.0, 2.0, 3.0])
    data.array_double_field([1200.5, 1202.5, 3.5])
    data.array_bool_field([False, True, False])
    data.array_enum_field([pytest.dds_type.Color_RED, pytest.dds_type.Color_BLUE, pytest.dds_type.Color_MAGENTA])
    data.array_enum2_field()[0] = pytest.dds_type.Material_METAL
    data.array_enum2_field()[1] = pytest.dds_type.Material_STONE
    data.array_enum2_field()[2] = pytest.dds_type.Material_PLASTIC
    data.array_struct_field([struct_type1, struct_type2, struct_type3])
    data.bounded_sequence_char_field(['\x01', '\x02', '\x03'])
    data.bounded_sequence_uint8_field([254, 255, 1])
    data.bounded_sequence_int16_field([-10, 10, -20])
    data.bounded_sequence_uint16_field([10, 35, 60])
    data.bounded_sequence_int32_field([-1000, 1000, -2000])
    data.bounded_sequence_uint32_field([1000, 200, 3000])
    data.bounded_sequence_int64_field([-36000, 36000, -1])
    data.bounded_sequence_uint64_field([36000, 128000, 3])
    data.bounded_sequence_float_field([1.0, 2.0, 3.0])
    data.bounded_sequence_double_field([1200.5, 1202.5, 3.5])
    data.bounded_sequence_bool_field([False, True, False])
    data.bounded_sequence_enum_field([pytest.dds_type.Color_RED, pytest.dds_type.Color_BLUE, pytest.dds_type.Color_MAGENTA])
    data.bounded_sequence_enum2_field().push_back(pytest.dds_type.Material_METAL)
    data.bounded_sequence_enum2_field().push_back(pytest.dds_type.Material_STONE)
    data.bounded_sequence_enum2_field().push_back(pytest.dds_type.Material_PLASTIC)
    data.bounded_sequence_struct_field([struct_type1, struct_type2, struct_type3])
    data.unbounded_sequence_char_field(['\x01', '\x02', '\x03'])
    data.unbounded_sequence_uint8_field([254, 255, 1])
    data.unbounded_sequence_int16_field([-10, 10, -20])
    data.unbounded_sequence_uint16_field([10, 35, 60])
    data.unbounded_sequence_int32_field([-1000, 1000, -2000])
    data.unbounded_sequence_uint32_field([1000, 200, 3000])
    data.unbounded_sequence_int64_field([-36000, 36000, -1])
    data.unbounded_sequence_uint64_field([36000, 128000, 3])
    data.unbounded_sequence_float_field([1.0, 2.0, 3.0])
    data.unbounded_sequence_double_field([1200.5, 1202.5, 3.5])
    data.unbounded_sequence_bool_field([False, True, False])
    data.unbounded_sequence_enum_field([pytest.dds_type.Color_RED, pytest.dds_type.Color_BLUE, pytest.dds_type.Color_MAGENTA])
    data.unbounded_sequence_enum2_field().push_back(pytest.dds_type.Material_METAL)
    data.unbounded_sequence_enum2_field().push_back(pytest.dds_type.Material_STONE)
    data.unbounded_sequence_enum2_field().push_back(pytest.dds_type.Material_PLASTIC)
    data.unbounded_sequence_struct_field([struct_type1, struct_type2, struct_type3])


def check_keyed_complete_test_type(data):
    assert(data.char_field() == '\x01')
    assert(data.uint8_field() == 254)
    assert(data.int16_field() == -10)
    assert(data.uint16_field() == 10)
    assert(data.int32_field() == -1000)
    assert(data.uint32_field() == 1000)
    assert(data.int64_field() == -36000)
    assert(data.uint64_field() == 36000)
    assert(data.float_field() == 1.0)
    assert(data.double_field() == 1202.5)
    assert(data.bool_field() == True)
    assert(data.string_field() == "Test string")
    assert(data.fixed_string_field() == "Fixed string")
    assert(data.enum_field() == pytest.dds_type.Color_MAGENTA)
    assert(data.enum2_field() == pytest.dds_type.Material_METAL)
    assert(data.struct_field().char_field() == '\x01')
    assert(data.struct_field().uint8_field() == 254)
    assert(data.struct_field().int16_field() == -10)
    assert(data.struct_field().uint16_field() == 10)
    assert(data.struct_field().int32_field() == -1000)
    assert(data.struct_field().uint32_field() == 1000)
    assert(data.struct_field().int64_field() == -36000)
    assert(data.struct_field().uint64_field() == 36000)
    assert(data.struct_field().float_field() == 1.0)
    assert(data.struct_field().double_field() == 1202.5)
    assert(data.struct_field().bool_field() == False)
    assert(data.struct_field().string_field() == "Test string")
    assert(data.struct_field().fixed_string_field() == "Fixed string")
    assert(data.struct_field().enum_field() == pytest.dds_type.Color_MAGENTA)
    assert(data.struct_field().enum2_field() == pytest.dds_type.Material_METAL)
    assert(data.char_opt_field().has_value())
    assert(data.char_opt_field().get_value() == '\x01')
    assert(data.uint8_opt_field().has_value())
    assert(data.uint8_opt_field().get_value() == 254)
    assert(data.int16_opt_field().has_value())
    assert(data.int16_opt_field().get_value() == -10)
    assert(data.uint16_opt_field().has_value())
    assert(data.uint16_opt_field().get_value() == 10)
    assert(data.int32_opt_field().has_value())
    assert(data.int32_opt_field().get_value() == -1000)
    assert(data.uint32_opt_field().has_value())
    assert(data.uint32_opt_field().get_value() == 1000)
    assert(data.int64_opt_field().has_value())
    assert(data.int64_opt_field().get_value() == -36000)
    assert(data.uint64_opt_field().has_value())
    assert(data.uint64_opt_field().get_value() == 36000)
    assert(data.float_opt_field().has_value())
    assert(data.float_opt_field().get_value() == 1.0)
    assert(data.double_opt_field().has_value())
    assert(data.double_opt_field().get_value() == 1202.5)
    assert(data.bool_opt_field().has_value())
    assert(data.bool_opt_field().get_value() == True)
    assert(data.string_opt_field().has_value())
    assert(data.string_opt_field().get_value() == "Test string")
    assert(data.enum_opt_field().has_value())
    assert(data.enum_opt_field().get_value() == pytest.dds_type.Color_MAGENTA)
    assert(not data.enum2_opt_field().has_value())
    assert(data.struct_opt_field().has_value())
    assert(data.struct_opt_field().char_field() == '\x01')
    assert(data.struct_opt_field().uint8_field() == 254)
    assert(data.struct_opt_field().int16_field() == -10)
    assert(data.struct_opt_field().uint16_field() == 10)
    assert(data.struct_opt_field().int32_field() == -1000)
    assert(data.struct_opt_field().uint32_field() == 1000)
    assert(data.struct_opt_field().int64_field() == -36000)
    assert(data.struct_opt_field().uint64_field() == 36000)
    assert(data.struct_opt_field().float_field() == 1.0)
    assert(data.struct_opt_field().double_field() == 1202.5)
    assert(data.struct_opt_field().bool_field() == True)
    assert(data.struct_opt_field().string_field() == "Test string")
    assert(data.struct_opt_field().fixed_string_field() == "Fixed string")
    assert(data.struct_opt_field().enum_field() == pytest.dds_type.Color_MAGENTA)
    assert(data.struct_opt_field().enum2_field() == pytest.dds_type.Material_METAL)
    assert(data.array_char_field()[0] == '\x01')
    assert(data.array_char_field()[1] == '\x02')
    assert(data.array_char_field()[2] == '\x03')
    assert(data.array_uint8_field()[0] == 254)
    assert(data.array_uint8_field()[1] == 255)
    assert(data.array_uint8_field()[2] == 1)
    assert(data.array_int16_field()[0] == -10)
    assert(data.array_int16_field()[1] == 10)
    assert(data.array_int16_field()[2] == -20)
    assert(data.array_uint16_field()[0] == 10)
    assert(data.array_uint16_field()[1] == 35)
    assert(data.array_uint16_field()[2] == 60)
    assert(data.array_int32_field()[0] == -1000)
    assert(data.array_int32_field()[1] == 1000)
    assert(data.array_int32_field()[2] == -2000)
    assert(data.array_uint32_field()[0] == 1000)
    assert(data.array_uint32_field()[1] == 200)
    assert(data.array_uint32_field()[2] == 3000)
    assert(data.array_int64_field()[0] == -36000)
    assert(data.array_int64_field()[1] == 36000)
    assert(data.array_int64_field()[2] == -1)
    assert(data.array_uint64_field()[0] == 36000)
    assert(data.array_uint64_field()[1] == 128000)
    assert(data.array_uint64_field()[2] == 3)
    assert(data.array_float_field()[0] == 1.0)
    assert(data.array_float_field()[1] == 2.0)
    assert(data.array_float_field()[2] == 3.0)
    assert(data.array_double_field()[0] == 1200.5)
    assert(data.array_double_field()[1] == 1202.5)
    assert(data.array_double_field()[2] == 3.5)
    assert(data.array_bool_field()[0] == False)
    assert(data.array_bool_field()[1] == True)
    assert(data.array_bool_field()[2] == False)
    assert(data.array_enum_field()[0] == pytest.dds_type.Color_RED)
    assert(data.array_enum_field()[1] == pytest.dds_type.Color_BLUE)
    assert(data.array_enum_field()[2] == pytest.dds_type.Color_MAGENTA)
    assert(data.array_enum2_field()[0] == pytest.dds_type.Material_METAL)
    assert(data.array_enum2_field()[1] == pytest.dds_type.Material_STONE)
    assert(data.array_enum2_field()[2] == pytest.dds_type.Material_PLASTIC)
    assert(data.array_struct_field()[0].char_field() == '\x01')
    assert(data.array_struct_field()[0].uint8_field() == 254)
    assert(data.array_struct_field()[0].int16_field() == -10)
    assert(data.array_struct_field()[0].uint16_field() == 10)
    assert(data.array_struct_field()[0].int32_field() == -1000)
    assert(data.array_struct_field()[0].uint32_field() == 1000)
    assert(data.array_struct_field()[0].int64_field() == -36000)
    assert(data.array_struct_field()[0].uint64_field() == 36000)
    assert(data.array_struct_field()[0].float_field() == 1.0)
    assert(data.array_struct_field()[0].double_field() == 1200.5)
    assert(data.array_struct_field()[0].bool_field() == False)
    assert(data.array_struct_field()[0].enum_field() == pytest.dds_type.Color_RED)
    assert(data.array_struct_field()[0].enum2_field() == pytest.dds_type.Material_STONE)
    assert(data.array_struct_field()[1].char_field() == '\x02')
    assert(data.array_struct_field()[1].uint8_field() == 255)
    assert(data.array_struct_field()[1].int16_field() == 10)
    assert(data.array_struct_field()[1].uint16_field() == 35)
    assert(data.array_struct_field()[1].int32_field() == 1000)
    assert(data.array_struct_field()[1].uint32_field() == 200)
    assert(data.array_struct_field()[1].int64_field() == 36000)
    assert(data.array_struct_field()[1].uint64_field() == 128000)
    assert(data.array_struct_field()[1].float_field() == 2.0)
    assert(data.array_struct_field()[1].double_field() == 1202.5)
    assert(data.array_struct_field()[1].bool_field() == True)
    assert(data.array_struct_field()[1].enum_field() == pytest.dds_type.Color_BLUE)
    assert(data.array_struct_field()[1].enum2_field() == pytest.dds_type.Material_PLASTIC)
    assert(data.array_struct_field()[2].char_field() == '\x03')
    assert(data.array_struct_field()[2].uint8_field() == 1)
    assert(data.array_struct_field()[2].int16_field() == -20)
    assert(data.array_struct_field()[2].uint16_field() == 60)
    assert(data.array_struct_field()[2].int32_field() == -2000)
    assert(data.array_struct_field()[2].uint32_field() == 3000)
    assert(data.array_struct_field()[2].int64_field() == -1)
    assert(data.array_struct_field()[2].uint64_field() == 3)
    assert(data.array_struct_field()[2].float_field() == 3.0)
    assert(data.array_struct_field()[2].double_field() == 3.5)
    assert(data.array_struct_field()[2].bool_field() == False)
    assert(data.array_struct_field()[2].enum_field() == pytest.dds_type.Color_MAGENTA)
    assert(data.array_struct_field()[2].enum2_field() == pytest.dds_type.Material_METAL)
    assert(data.bounded_sequence_char_field().size() == 3)
    assert(data.bounded_sequence_char_field()[0] == '\x01')
    assert(data.bounded_sequence_char_field()[1] == '\x02')
    assert(data.bounded_sequence_char_field()[2] == '\x03')
    assert(data.bounded_sequence_uint8_field().size() == 3)
    assert(data.bounded_sequence_uint8_field()[0] == 254)
    assert(data.bounded_sequence_uint8_field()[1] == 255)
    assert(data.bounded_sequence_uint8_field()[2] == 1)
    assert(data.bounded_sequence_int16_field().size() == 3)
    assert(data.bounded_sequence_int16_field()[0] == -10)
    assert(data.bounded_sequence_int16_field()[1] == 10)
    assert(data.bounded_sequence_int16_field()[2] == -20)
    assert(data.bounded_sequence_uint16_field().size() == 3)
    assert(data.bounded_sequence_uint16_field()[0] == 10)
    assert(data.bounded_sequence_uint16_field()[1] == 35)
    assert(data.bounded_sequence_uint16_field()[2] == 60)
    assert(data.bounded_sequence_int32_field().size() == 3)
    assert(data.bounded_sequence_int32_field()[0] == -1000)
    assert(data.bounded_sequence_int32_field()[1] == 1000)
    assert(data.bounded_sequence_int32_field()[2] == -2000)
    assert(data.bounded_sequence_uint32_field().size() == 3)
    assert(data.bounded_sequence_uint32_field()[0] == 1000)
    assert(data.bounded_sequence_uint32_field()[1] == 200)
    assert(data.bounded_sequence_uint32_field()[2] == 3000)
    assert(data.bounded_sequence_int64_field().size() == 3)
    assert(data.bounded_sequence_int64_field()[0] == -36000)
    assert(data.bounded_sequence_int64_field()[1] == 36000)
    assert(data.bounded_sequence_int64_field()[2] == -1)
    assert(data.bounded_sequence_uint64_field().size() == 3)
    assert(data.bounded_sequence_uint64_field()[0] == 36000)
    assert(data.bounded_sequence_uint64_field()[1] == 128000)
    assert(data.bounded_sequence_uint64_field()[2] == 3)
    assert(data.bounded_sequence_float_field().size() == 3)
    assert(data.bounded_sequence_float_field()[0] == 1.0)
    assert(data.bounded_sequence_float_field()[1] == 2.0)
    assert(data.bounded_sequence_float_field()[2] == 3.0)
    assert(data.bounded_sequence_double_field().size() == 3)
    assert(data.bounded_sequence_double_field()[0] == 1200.5)
    assert(data.bounded_sequence_double_field()[1] == 1202.5)
    assert(data.bounded_sequence_double_field()[2] == 3.5)
    assert(data.bounded_sequence_bool_field().size() == 3)
    assert(data.bounded_sequence_bool_field()[0] == False)
    assert(data.bounded_sequence_bool_field()[1] == True)
    assert(data.bounded_sequence_bool_field()[2] == False)
    assert(data.bounded_sequence_enum_field().size() == 3)
    assert(data.bounded_sequence_enum_field()[0] == pytest.dds_type.Color_RED)
    assert(data.bounded_sequence_enum_field()[1] == pytest.dds_type.Color_BLUE)
    assert(data.bounded_sequence_enum_field()[2] == pytest.dds_type.Color_MAGENTA)
    assert(data.bounded_sequence_enum2_field().size() == 3)
    assert(data.bounded_sequence_enum2_field()[0] == pytest.dds_type.Material_METAL)
    assert(data.bounded_sequence_enum2_field()[1] == pytest.dds_type.Material_STONE)
    assert(data.bounded_sequence_enum2_field()[2] == pytest.dds_type.Material_PLASTIC)
    assert(data.bounded_sequence_struct_field().size() == 3)
    assert(data.bounded_sequence_struct_field()[0].char_field() == '\x01')
    assert(data.bounded_sequence_struct_field()[0].uint8_field() == 254)
    assert(data.bounded_sequence_struct_field()[0].int16_field() == -10)
    assert(data.bounded_sequence_struct_field()[0].uint16_field() == 10)
    assert(data.bounded_sequence_struct_field()[0].int32_field() == -1000)
    assert(data.bounded_sequence_struct_field()[0].uint32_field() == 1000)
    assert(data.bounded_sequence_struct_field()[0].int64_field() == -36000)
    assert(data.bounded_sequence_struct_field()[0].uint64_field() == 36000)
    assert(data.bounded_sequence_struct_field()[0].float_field() == 1.0)
    assert(data.bounded_sequence_struct_field()[0].double_field() == 1200.5)
    assert(data.bounded_sequence_struct_field()[0].bool_field() == False)
    assert(data.bounded_sequence_struct_field()[0].enum_field() == pytest.dds_type.Color_RED)
    assert(data.bounded_sequence_struct_field()[0].enum2_field() == pytest.dds_type.Material_STONE)
    assert(data.bounded_sequence_struct_field()[1].char_field() == '\x02')
    assert(data.bounded_sequence_struct_field()[1].uint8_field() == 255)
    assert(data.bounded_sequence_struct_field()[1].int16_field() == 10)
    assert(data.bounded_sequence_struct_field()[1].uint16_field() == 35)
    assert(data.bounded_sequence_struct_field()[1].int32_field() == 1000)
    assert(data.bounded_sequence_struct_field()[1].uint32_field() == 200)
    assert(data.bounded_sequence_struct_field()[1].int64_field() == 36000)
    assert(data.bounded_sequence_struct_field()[1].uint64_field() == 128000)
    assert(data.bounded_sequence_struct_field()[1].float_field() == 2.0)
    assert(data.bounded_sequence_struct_field()[1].double_field() == 1202.5)
    assert(data.bounded_sequence_struct_field()[1].bool_field() == True)
    assert(data.bounded_sequence_struct_field()[1].enum_field() == pytest.dds_type.Color_BLUE)
    assert(data.bounded_sequence_struct_field()[1].enum2_field() == pytest.dds_type.Material_PLASTIC)
    assert(data.bounded_sequence_struct_field()[2].char_field() == '\x03')
    assert(data.bounded_sequence_struct_field()[2].uint8_field() == 1)
    assert(data.bounded_sequence_struct_field()[2].int16_field() == -20)
    assert(data.bounded_sequence_struct_field()[2].uint16_field() == 60)
    assert(data.bounded_sequence_struct_field()[2].int32_field() == -2000)
    assert(data.bounded_sequence_struct_field()[2].uint32_field() == 3000)
    assert(data.bounded_sequence_struct_field()[2].int64_field() == -1)
    assert(data.bounded_sequence_struct_field()[2].uint64_field() == 3)
    assert(data.bounded_sequence_struct_field()[2].float_field() == 3.0)
    assert(data.bounded_sequence_struct_field()[2].double_field() == 3.5)
    assert(data.bounded_sequence_struct_field()[2].bool_field() == False)
    assert(data.bounded_sequence_struct_field()[2].enum_field() == pytest.dds_type.Color_MAGENTA)
    assert(data.bounded_sequence_struct_field()[2].enum2_field() == pytest.dds_type.Material_METAL)
    assert(data.unbounded_sequence_char_field().size() == 3)
    assert(data.unbounded_sequence_char_field()[0] == '\x01')
    assert(data.unbounded_sequence_char_field()[1] == '\x02')
    assert(data.unbounded_sequence_char_field()[2] == '\x03')
    assert(data.unbounded_sequence_uint8_field().size() == 3)
    assert(data.unbounded_sequence_uint8_field()[0] == 254)
    assert(data.unbounded_sequence_uint8_field()[1] == 255)
    assert(data.unbounded_sequence_uint8_field()[2] == 1)
    assert(data.unbounded_sequence_int16_field().size() == 3)
    assert(data.unbounded_sequence_int16_field()[0] == -10)
    assert(data.unbounded_sequence_int16_field()[1] == 10)
    assert(data.unbounded_sequence_int16_field()[2] == -20)
    assert(data.unbounded_sequence_uint16_field().size() == 3)
    assert(data.unbounded_sequence_uint16_field()[0] == 10)
    assert(data.unbounded_sequence_uint16_field()[1] == 35)
    assert(data.unbounded_sequence_uint16_field()[2] == 60)
    assert(data.unbounded_sequence_int32_field().size() == 3)
    assert(data.unbounded_sequence_int32_field()[0] == -1000)
    assert(data.unbounded_sequence_int32_field()[1] == 1000)
    assert(data.unbounded_sequence_int32_field()[2] == -2000)
    assert(data.unbounded_sequence_uint32_field().size() == 3)
    assert(data.unbounded_sequence_uint32_field()[0] == 1000)
    assert(data.unbounded_sequence_uint32_field()[1] == 200)
    assert(data.unbounded_sequence_uint32_field()[2] == 3000)
    assert(data.unbounded_sequence_int64_field().size() == 3)
    assert(data.unbounded_sequence_int64_field()[0] == -36000)
    assert(data.unbounded_sequence_int64_field()[1] == 36000)
    assert(data.unbounded_sequence_int64_field()[2] == -1)
    assert(data.unbounded_sequence_uint64_field().size() == 3)
    assert(data.unbounded_sequence_uint64_field()[0] == 36000)
    assert(data.unbounded_sequence_uint64_field()[1] == 128000)
    assert(data.unbounded_sequence_uint64_field()[2] == 3)
    assert(data.unbounded_sequence_float_field().size() == 3)
    assert(data.unbounded_sequence_float_field()[0] == 1.0)
    assert(data.unbounded_sequence_float_field()[1] == 2.0)
    assert(data.unbounded_sequence_float_field()[2] == 3.0)
    assert(data.unbounded_sequence_double_field().size() == 3)
    assert(data.unbounded_sequence_double_field()[0] == 1200.5)
    assert(data.unbounded_sequence_double_field()[1] == 1202.5)
    assert(data.unbounded_sequence_double_field()[2] == 3.5)
    assert(data.unbounded_sequence_bool_field().size() == 3)
    assert(data.unbounded_sequence_bool_field()[0] == False)
    assert(data.unbounded_sequence_bool_field()[1] == True)
    assert(data.unbounded_sequence_bool_field()[2] == False)
    assert(data.unbounded_sequence_enum_field().size() == 3)
    assert(data.unbounded_sequence_enum_field()[0] == pytest.dds_type.Color_RED)
    assert(data.unbounded_sequence_enum_field()[1] == pytest.dds_type.Color_BLUE)
    assert(data.unbounded_sequence_enum_field()[2] == pytest.dds_type.Color_MAGENTA)
    assert(data.unbounded_sequence_enum2_field().size() == 3)
    assert(data.unbounded_sequence_enum2_field()[0] == pytest.dds_type.Material_METAL)
    assert(data.unbounded_sequence_enum2_field()[1] == pytest.dds_type.Material_STONE)
    assert(data.unbounded_sequence_enum2_field()[2] == pytest.dds_type.Material_PLASTIC)
    assert(data.unbounded_sequence_struct_field().size() == 3)
    assert(data.unbounded_sequence_struct_field()[0].char_field() == '\x01')
    assert(data.unbounded_sequence_struct_field()[0].uint8_field() == 254)
    assert(data.unbounded_sequence_struct_field()[0].int16_field() == -10)
    assert(data.unbounded_sequence_struct_field()[0].uint16_field() == 10)
    assert(data.unbounded_sequence_struct_field()[0].int32_field() == -1000)
    assert(data.unbounded_sequence_struct_field()[0].uint32_field() == 1000)
    assert(data.unbounded_sequence_struct_field()[0].int64_field() == -36000)
    assert(data.unbounded_sequence_struct_field()[0].uint64_field() == 36000)
    assert(data.unbounded_sequence_struct_field()[0].float_field() == 1.0)
    assert(data.unbounded_sequence_struct_field()[0].double_field() == 1200.5)
    assert(data.unbounded_sequence_struct_field()[0].bool_field() == False)
    assert(data.unbounded_sequence_struct_field()[0].enum_field() == pytest.dds_type.Color_RED)
    assert(data.unbounded_sequence_struct_field()[0].enum2_field() == pytest.dds_type.Material_STONE)
    assert(data.unbounded_sequence_struct_field()[1].char_field() == '\x02')
    assert(data.unbounded_sequence_struct_field()[1].uint8_field() == 255)
    assert(data.unbounded_sequence_struct_field()[1].int16_field() == 10)
    assert(data.unbounded_sequence_struct_field()[1].uint16_field() == 35)
    assert(data.unbounded_sequence_struct_field()[1].int32_field() == 1000)
    assert(data.unbounded_sequence_struct_field()[1].uint32_field() == 200)
    assert(data.unbounded_sequence_struct_field()[1].int64_field() == 36000)
    assert(data.unbounded_sequence_struct_field()[1].uint64_field() == 128000)
    assert(data.unbounded_sequence_struct_field()[1].float_field() == 2.0)
    assert(data.unbounded_sequence_struct_field()[1].double_field() == 1202.5)
    assert(data.unbounded_sequence_struct_field()[1].bool_field() == True)
    assert(data.unbounded_sequence_struct_field()[1].enum_field() == pytest.dds_type.Color_BLUE)
    assert(data.unbounded_sequence_struct_field()[1].enum2_field() == pytest.dds_type.Material_PLASTIC)
    assert(data.unbounded_sequence_struct_field()[2].char_field() == '\x03')
    assert(data.unbounded_sequence_struct_field()[2].uint8_field() == 1)
    assert(data.unbounded_sequence_struct_field()[2].int16_field() == -20)
    assert(data.unbounded_sequence_struct_field()[2].uint16_field() == 60)
    assert(data.unbounded_sequence_struct_field()[2].int32_field() == -2000)
    assert(data.unbounded_sequence_struct_field()[2].uint32_field() == 3000)
    assert(data.unbounded_sequence_struct_field()[2].int64_field() == -1)
    assert(data.unbounded_sequence_struct_field()[2].uint64_field() == 3)
    assert(data.unbounded_sequence_struct_field()[2].float_field() == 3.0)
    assert(data.unbounded_sequence_struct_field()[2].double_field() == 3.5)
    assert(data.unbounded_sequence_struct_field()[2].bool_field() == False)
    assert(data.unbounded_sequence_struct_field()[2].enum_field() == pytest.dds_type.Color_MAGENTA)
    assert(data.unbounded_sequence_struct_field()[2].enum2_field() == pytest.dds_type.Material_METAL)


def test_create_querycondition(datareader):
    """
    This test checks:
    - DataReader::create_querycondition
    - DataReader::delete_contained_entities
    """
    sv = fastdds.ANY_SAMPLE_STATE
    vv = fastdds.ANY_VIEW_STATE
    iv = fastdds.ANY_INSTANCE_STATE
    qp = fastdds.StringVector()

    querycondition = datareader.create_querycondition(
               sv, vv, iv, "", qp)
    assert(querycondition is None)
    assert(fastdds.RETCODE_OK ==
           datareader.delete_contained_entities())


def test_create_readcondition(datareader):
    """
    This test checks:
    - DataReader::create_readcondition
    - DataReader::delete_readcondition
    """
    sv = fastdds.ANY_SAMPLE_STATE
    vv = fastdds.ANY_VIEW_STATE
    iv = fastdds.ANY_INSTANCE_STATE

    readcondition = datareader.create_readcondition(
               sv, vv, iv)
    assert(readcondition is not None)
    assert(fastdds.RETCODE_OK ==
           datareader.delete_readcondition(readcondition))


def test_get_first_untaken(transient_datareader_qos, datareader,
                           datawriter):
    """
    This test checks:
    - DataReader::get_first_untaken_info
    """
    info = fastdds.SampleInfo()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.get_first_untaken_info(info))
    qos = datareader.get_qos()
    assert(fastdds.TRANSIENT_LOCAL_DURABILITY_QOS == qos.durability().kind)
    qos = datawriter.get_qos()
    assert(fastdds.TRANSIENT_LOCAL_DURABILITY_QOS == qos.durability().kind)

    sample = pytest.dds_type.CompleteTestType()
    sample.int16_field(255)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.get_first_untaken_info(info))
    assert(info.valid_data)


def test_get_instance_handle(datareader):
    """
    This test checks:
    - DataReader::guid
    - DataReader::get_instance_handle
    """
    guid = datareader.guid()
    assert(fastdds.c_Guid_Unknown != guid)
    ih = datareader.get_instance_handle()
    assert(fastdds.c_InstanceHandle_Unknown != ih)

    for i in range(0, 12):
        assert(guid.guidPrefix.value[i] == ih.value[i])

    for i in range(0, 4):
        assert(guid.entityId.value[i] == ih.value[12+i])


def test_get_key_value(test_keyed_type, datareader):
    """
    This test checks:
    - DataReader::get_key_value
    """
    sample = pytest.dds_type.KeyedCompleteTestType()
    sample.id(255)
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.RETCODE_UNSUPPORTED ==
           datareader.get_key_value(sample, ih))
    assert(fastdds.c_InstanceHandle_Unknown == ih)


def test_get_set_listener(datareader):
    """
    This test checks:
    - DataReader::get_listener
    - DataReader::set_listener
    - DataReader::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    # Overload 1
    listener = DataReaderListener()
    assert(listener is not None)
    assert(fastdds.RETCODE_OK ==
           datareader.set_listener(listener))
    assert(datareader.get_listener() == listener)
    assert(fastdds.StatusMask.all() ==
           datareader.get_status_mask())

    def test(status_mask):
        """
        Test the entity creation using the type of StatusMask.
        """
        listener = DataReaderListener()
        assert(listener is not None)
        assert(fastdds.RETCODE_OK ==
               datareader.set_listener(listener, status_mask))
        assert(datareader.get_listener() == listener)
        assert(status_mask == datareader.get_status_mask())

    # Overload 2: Different status masks
    test(fastdds.StatusMask.all())
    test(fastdds.StatusMask.none())
    test(fastdds.StatusMask.data_available())
    test(fastdds.StatusMask.data_on_readers())
    test(fastdds.StatusMask.inconsistent_topic())
    test(fastdds.StatusMask.liveliness_changed())
    test(fastdds.StatusMask.liveliness_lost())
    test(fastdds.StatusMask.offered_deadline_missed())
    test(fastdds.StatusMask.offered_incompatible_qos())
    test(fastdds.StatusMask.publication_matched())
    test(fastdds.StatusMask.requested_deadline_missed())
    test(fastdds.StatusMask.requested_incompatible_qos())
    test(fastdds.StatusMask.sample_lost())
    test(fastdds.StatusMask.sample_rejected())
    test(fastdds.StatusMask.subscription_matched())

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched())


def test_get_listening_locators(datareader):
    """
    This test checks:
    - DataReader::get_listening_locators
    """
    locator_list = fastdds.LocatorList()
    assert(fastdds.RETCODE_OK ==
           datareader.get_listening_locators(locator_list))
    assert(0 < locator_list.size())


def test_get_liveliness_changed_status(datareader):
    """
    This test checks:
    - DataReader::get_liveliness_changed_status
    """
    status = fastdds.LivelinessChangedStatus()
    assert(fastdds.RETCODE_OK ==
           datareader.get_liveliness_changed_status(status))
    assert(0 == status.alive_count)
    assert(0 == status.alive_count_change)
    assert(0 == status.not_alive_count)
    assert(0 == status.not_alive_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_publication_handle)


def test_get_matched_publication_data(datareader):
    """
    This test checks:
    - DataReader::get_matched_publication_data
    """
    pub_data = fastdds.PublicationBuiltinTopicData()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.RETCODE_UNSUPPORTED ==
           datareader.get_matched_publication_data(pub_data, ih))


def test_get_matched_publications(datareader):
    """
    This test checks:
    - DataReader::get_matched_publications
    """
    ihs = fastdds.InstanceHandleVector()
    assert(fastdds.RETCODE_UNSUPPORTED ==
           datareader.get_matched_publications(ihs))


def test_get_requested_deadline_missed_status(datareader):
    """
    This test checks:
    - DataReader::get_requested_deadline_missed_status
    """
    status = fastdds.RequestedDeadlineMissedStatus()
    assert(fastdds.RETCODE_OK ==
           datareader.get_requested_deadline_missed_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_instance_handle)


def test_get_requested_incompatible_qos_status(datareader):
    """
    This test checks:
    - DataReader::get_requested_deadline_missed_status
    """
    status = fastdds.RequestedIncompatibleQosStatus()
    assert(fastdds.RETCODE_OK ==
           datareader.get_requested_incompatible_qos_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(fastdds.INVALID_QOS_POLICY_ID == status.last_policy_id)
    assert(fastdds.NEXT_QOS_POLICY_ID == status.policies.size())
    id = 0
    for policy in status.policies:
        assert(0 == policy.count)
        assert(id == policy.policy_id)
        id += 1


def test_get_sample_lost_status(datareader):
    """
    This test checks:
    - DataReader::get_sample_lost_status
    """
    status = fastdds.SampleLostStatus()
    assert(fastdds.RETCODE_OK ==
           datareader.get_sample_lost_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)


def test_get_sample_rejected_status(datareader):
    """
    This test checks:
    - DataReader::get_sample_rejected_status
    """
    status = fastdds.SampleRejectedStatus()
    assert(fastdds.RETCODE_OK ==
           datareader.get_sample_rejected_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)


def test_get_subscription_matched_status(datareader):
    """
    This test checks:
    - DataReader::get_subscription_matched_status
    """
    status = fastdds.SubscriptionMatchedStatus()
    assert(fastdds.RETCODE_OK ==
           datareader.get_subscription_matched_status(status))
    assert(0 == status.total_count)
    assert(0 == status.total_count_change)
    assert(0 == status.current_count)
    assert(0 == status.current_count_change)
    assert(fastdds.c_InstanceHandle_Unknown == status.last_publication_handle)


def test_get_subscriber(subscriber, datareader):
    """
    This test checks:
    - DataReader::get_subscriber
    """
    sub = datareader.get_subscriber()
    assert(sub == subscriber)


def test_get_topicdescription(topic, datareader):
    """
    This test checks:
    - DataReader::get_topicdescription
    """
    topic_aux = datareader.get_topicdescription()
    assert(topic.get_impl() == topic_aux.get_impl())
    assert(topic.get_type_name() == topic_aux.get_type_name())


def test_get_unread_count(transient_datareader_qos, datareader,
                          datawriter):
    """
    This test checks:
    - DataReader::get_unread_count
    """
    assert(0 == datareader.get_unread_count())

    sample = pytest.dds_type.CompleteTestType()
    sample.int16_field(255)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(1 == datareader.get_unread_count())


def test_is_sample_valid(transient_datareader_qos, datareader,
                         datawriter):
    """
    This test checks:
    - DataReader::is_sample_valid
    """
    sample = pytest.dds_type.CompleteTestType()
    sample.int16_field(255)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    data = pytest.dds_type.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.RETCODE_OK ==
           datareader.read_next_sample(data, info))
    assert(datareader.is_sample_valid(data, info))
    assert(sample.int16_field() == data.int16_field())


def test_lookup_instance(transient_datareader_qos, test_keyed_type, datareader,
                         datawriter):
    """
    This test checks:
    - DataReader::lookup_instance
    """

    # Test when parameter is None
    ih = datareader.lookup_instance(None)
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    # Test when instance is not registered
    sample = pytest.dds_type.KeyedCompleteTestType()
    sample.id(3)
    ih = datareader.lookup_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown == ih)

    # Test when instance is registered
    writer_ih = datawriter.register_instance(sample)
    assert(fastdds.c_InstanceHandle_Unknown != writer_ih)
    assert(fastdds.RETCODE_OK ==
           datawriter.write(sample, writer_ih))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    ih = datareader.lookup_instance(sample)
    assert(writer_ih == ih)


def test_read(transient_datareader_qos, datareader, datawriter):
    """
    This test checks:
    - DataReader::read
    - DataReader::return_loan
    """
    data_seq = pytest.dds_type.CompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.read(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = pytest.dds_type.CompleteTestType()
    fill_keyed_complete_test_type(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK == datareader.read(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(0 < info_seq[0].source_timestamp.to_ns())
    assert(0 < info_seq[0].reception_timestamp.to_ns())
    assert(sample == data_seq[0])
    check_keyed_complete_test_type(data_seq[0])
    assert(fastdds.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_read_instance(transient_datareader_qos, test_keyed_type,
                       datareader, datawriter):
    """
    This test checks:
    - DataReader::read_instance
    - DataReader::return_loan
    """
    data_seq = pytest.dds_type.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.RETCODE_BAD_PARAMETER ==
           datareader.read_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = pytest.dds_type.KeyedCompleteTestType()
    fill_keyed_complete_test_type(sample)
    ih = datawriter.register_instance(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample, ih))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.read_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(0 < info_seq[0].source_timestamp.to_ns())
    assert(0 < info_seq[0].reception_timestamp.to_ns())
    assert(sample == data_seq[0])
    check_keyed_complete_test_type(data_seq[0])
    assert(fastdds.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_read_next_instance(transient_datareader_qos, test_keyed_type,
                            datareader, datawriter):
    """
    This test checks:
    - DataReader::read_next_instance
    - DataReader::return_loan
    """
    data_seq = pytest.dds_type.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.read_next_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = pytest.dds_type.KeyedCompleteTestType()
    fill_keyed_complete_test_type(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.read_next_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(0 < info_seq[0].source_timestamp.to_ns())
    assert(0 < info_seq[0].reception_timestamp.to_ns())
    assert(sample == data_seq[0])
    check_keyed_complete_test_type(data_seq[0])
    assert(fastdds.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_read_next_sample(transient_datareader_qos, datareader,
                          datawriter):
    """
    This test checks:
    - DataReader::read_next_sample
    """
    data = pytest.dds_type.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.read_next_sample(
                data, info))

    sample = pytest.dds_type.CompleteTestType()
    fill_keyed_complete_test_type(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.read_next_sample(data, info))
    assert(info.valid_data)
    assert(0 < info.source_timestamp.to_ns())
    assert(0 < info.reception_timestamp.to_ns())
    assert(sample == data)
    check_keyed_complete_test_type(data)


def test_take(transient_datareader_qos, datareader,
              datawriter):
    """
    This test checks:
    - DataReader::take
    - DataReader::return_loan
    """
    data_seq = pytest.dds_type.CompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.take(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = pytest.dds_type.CompleteTestType()
    fill_keyed_complete_test_type(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK == datareader.take(
        data_seq, info_seq, fastdds.LENGTH_UNLIMITED,
        fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
        fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(0 < info_seq[0].source_timestamp.to_ns())
    assert(0 < info_seq[0].reception_timestamp.to_ns())
    assert(sample == data_seq[0])
    check_keyed_complete_test_type(data_seq[0])
    assert(fastdds.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_take_instance(transient_datareader_qos, test_keyed_type,
                       datareader, datawriter):
    """
    This test checks:
    - DataReader::take_instance
    - DataReader::return_loan
    """
    data_seq = pytest.dds_type.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.RETCODE_BAD_PARAMETER ==
           datareader.take_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = pytest.dds_type.KeyedCompleteTestType()
    fill_keyed_complete_test_type(sample)
    ih = datawriter.register_instance(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample, ih))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.take_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(0 < info_seq[0].source_timestamp.to_ns())
    assert(0 < info_seq[0].reception_timestamp.to_ns())
    assert(sample == data_seq[0])
    check_keyed_complete_test_type(data_seq[0])
    assert(fastdds.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_take_next_instance(transient_datareader_qos, test_keyed_type,
                            datareader, datawriter):
    """
    This test checks:
    - DataReader::take_next_instance
    - DataReader::return_loan
    """
    data_seq = pytest.dds_type.KeyedCompleteTestTypeSeq()
    info_seq = fastdds.SampleInfoSeq()
    ih = fastdds.InstanceHandle_t()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.take_next_instance(
               data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
               fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
               fastdds.ANY_INSTANCE_STATE))
    assert(0 == len(data_seq))
    assert(0 == len(info_seq))

    sample = pytest.dds_type.KeyedCompleteTestType()
    fill_keyed_complete_test_type(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.take_next_instance(
                data_seq, info_seq, fastdds.LENGTH_UNLIMITED, ih,
                fastdds.ANY_SAMPLE_STATE, fastdds.ANY_VIEW_STATE,
                fastdds.ANY_INSTANCE_STATE))
    assert(1 == len(data_seq))
    assert(1 == len(info_seq))
    assert(info_seq[0].valid_data is True)
    assert(0 < info_seq[0].source_timestamp.to_ns())
    assert(0 < info_seq[0].reception_timestamp.to_ns())
    assert(sample == data_seq[0])
    check_keyed_complete_test_type(data_seq[0])
    assert(fastdds.RETCODE_OK ==
           datareader.return_loan(data_seq, info_seq))


def test_take_next_sample(transient_datareader_qos, datareader,
                          datawriter):
    """
    This test checks:
    - DataReader::take_next_sample
    """
    data = pytest.dds_type.CompleteTestType()
    info = fastdds.SampleInfo()
    assert(fastdds.RETCODE_NO_DATA ==
           datareader.take_next_sample(
                data, info))

    sample = pytest.dds_type.CompleteTestType()
    fill_keyed_complete_test_type(sample)
    assert(fastdds.RETCODE_OK == datawriter.write(sample))

    assert(datareader.wait_for_unread_message(
        fastdds.Duration_t(5, 0)))
    assert(fastdds.RETCODE_OK ==
           datareader.take_next_sample(data, info))
    assert(info.valid_data)
    assert(0 < info.source_timestamp.to_ns())
    assert(0 < info.reception_timestamp.to_ns())
    assert(sample == data)
    check_keyed_complete_test_type(data)


def test_get_type(test_type, datareader):
    """
    This test checks:
    - DataReader::type
    """
    test_type_aux = datareader.type()
    assert(test_type == test_type_aux)
    assert(test_type.get_type_name() == test_type_aux.get_type_name())


def test_wait_for_historical_data(datareader):
    """
    This test checks:
    - DataReader::wait_for_historical_data
    """
    assert(fastdds.RETCODE_UNSUPPORTED ==
           datareader.wait_for_historical_data(
               fastdds.Duration_t(0, 100)))


def test_wait_for_unread_message(datareader):
    """
    This test checks:
    - DataReader::wait_for_unread_message
    """
    assert(not datareader.wait_for_unread_message(fastdds.Duration_t(0, 100)))


def test_listener_ownership(participant, writer_participant, topic,
                            writer_topic, subscriber, publisher):

    def create_datareader():
        listener = DataReaderListener()
        return subscriber.create_datareader(
                topic, fastdds.DATAREADER_QOS_DEFAULT, listener)

    datareader = create_datareader()
    datawriter = publisher.create_datawriter(
                writer_topic, fastdds.DATAWRITER_QOS_DEFAULT)
    time.sleep(1)
    factory = fastdds.DomainParticipantFactory.get_instance()
    assert(fastdds.RETCODE_OK ==
           publisher.delete_datawriter(datawriter))
    assert(fastdds.RETCODE_OK ==
           writer_participant.delete_topic(writer_topic))
    assert(fastdds.RETCODE_OK ==
           writer_participant.delete_publisher(publisher))
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(writer_participant))
    assert(fastdds.RETCODE_OK ==
           subscriber.delete_datareader(datareader))
    assert(fastdds.RETCODE_OK ==
           participant.delete_topic(topic))
    assert(fastdds.RETCODE_OK ==
           participant.delete_subscriber(subscriber))
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))
