// Copyright 2016 Proyectos y Sistemas de Mantenimiento SL (eProsima).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*!
 * @file test_modulesPubSubTypes.cpp
 * This header file contains the implementation of the serialization functions.
 *
 * This file was generated by the tool fastddsgen.
 */


#include <fastcdr/FastBuffer.h>
#include <fastcdr/Cdr.h>
#include <fastcdr/CdrSizeCalculator.hpp>

#include "test_modulesPubSubTypes.h"
#include "test_modulesCdrAux.hpp"

using SerializedPayload_t = eprosima::fastrtps::rtps::SerializedPayload_t;
using InstanceHandle_t = eprosima::fastrtps::rtps::InstanceHandle_t;
using DataRepresentationId_t = eprosima::fastdds::dds::DataRepresentationId_t;

namespace eprosima {
    namespace test {
        StructTypePubSubType::StructTypePubSubType()
        {
            setName("eprosima::test::StructType");
            uint32_t type_size = eprosima_test_StructType_max_cdr_typesize;
            type_size += static_cast<uint32_t>(eprosima::fastcdr::Cdr::alignment(type_size, 4)); /* possible submessage alignment */
            m_typeSize = type_size + 4; /*encapsulation*/
            m_isGetKeyDefined = false;
            uint32_t keyLength = eprosima_test_StructType_max_key_cdr_typesize > 16 ? eprosima_test_StructType_max_key_cdr_typesize : 16;
            m_keyBuffer = reinterpret_cast<unsigned char*>(malloc(keyLength));
            memset(m_keyBuffer, 0, keyLength);
        }

        StructTypePubSubType::~StructTypePubSubType()
        {
            if (m_keyBuffer != nullptr)
            {
                free(m_keyBuffer);
            }
        }

        bool StructTypePubSubType::serialize(
                void* data,
                SerializedPayload_t* payload,
                DataRepresentationId_t data_representation)
        {
            StructType* p_type = static_cast<StructType*>(data);

            // Object that manages the raw buffer.
            eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(payload->data), payload->max_size);
            // Object that serializes the data.
            eprosima::fastcdr::Cdr ser(fastbuffer, eprosima::fastcdr::Cdr::DEFAULT_ENDIAN,
                    data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                    eprosima::fastcdr::CdrVersion::XCDRv1 : eprosima::fastcdr::CdrVersion::XCDRv2);
            payload->encapsulation = ser.endianness() == eprosima::fastcdr::Cdr::BIG_ENDIANNESS ? CDR_BE : CDR_LE;
            ser.set_encoding_flag(
                data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                eprosima::fastcdr::EncodingAlgorithmFlag::PLAIN_CDR  :
                eprosima::fastcdr::EncodingAlgorithmFlag::DELIMIT_CDR2);

            try
            {
                // Serialize encapsulation
                ser.serialize_encapsulation();
                // Serialize the object.
                ser << *p_type;
            }
            catch (eprosima::fastcdr::exception::Exception& /*exception*/)
            {
                return false;
            }

            // Get the serialized length
            payload->length = static_cast<uint32_t>(ser.get_serialized_data_length());
            return true;
        }

        bool StructTypePubSubType::deserialize(
                SerializedPayload_t* payload,
                void* data)
        {
            try
            {
                // Convert DATA to pointer of your type
                StructType* p_type = static_cast<StructType*>(data);

                // Object that manages the raw buffer.
                eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(payload->data), payload->length);

                // Object that deserializes the data.
                eprosima::fastcdr::Cdr deser(fastbuffer, eprosima::fastcdr::Cdr::DEFAULT_ENDIAN);

                // Deserialize encapsulation.
                deser.read_encapsulation();
                payload->encapsulation = deser.endianness() == eprosima::fastcdr::Cdr::BIG_ENDIANNESS ? CDR_BE : CDR_LE;

                // Deserialize the object.
                deser >> *p_type;
            }
            catch (eprosima::fastcdr::exception::Exception& /*exception*/)
            {
                return false;
            }

            return true;
        }

        std::function<uint32_t()> StructTypePubSubType::getSerializedSizeProvider(
                void* data,
                DataRepresentationId_t data_representation)
        {
            return [data, data_representation]() -> uint32_t
                   {
                       eprosima::fastcdr::CdrSizeCalculator calculator(
                           data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                           eprosima::fastcdr::CdrVersion::XCDRv1 :eprosima::fastcdr::CdrVersion::XCDRv2);
                       size_t current_alignment {0};
                       return static_cast<uint32_t>(calculator.calculate_serialized_size(
                                   *static_cast<StructType*>(data), current_alignment)) +
                               4u /*encapsulation*/;
                   };
        }

        void* StructTypePubSubType::createData()
        {
            return reinterpret_cast<void*>(new StructType());
        }

        void StructTypePubSubType::deleteData(
                void* data)
        {
            delete(reinterpret_cast<StructType*>(data));
        }

        bool StructTypePubSubType::getKey(
                void* data,
                InstanceHandle_t* handle,
                bool force_md5)
        {
            if (!m_isGetKeyDefined)
            {
                return false;
            }

            StructType* p_type = static_cast<StructType*>(data);

            // Object that manages the raw buffer.
            eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(m_keyBuffer),
                    eprosima_test_StructType_max_key_cdr_typesize);

            // Object that serializes the data.
            eprosima::fastcdr::Cdr ser(fastbuffer, eprosima::fastcdr::Cdr::BIG_ENDIANNESS);
            eprosima::fastcdr::serialize_key(ser, *p_type);
            if (force_md5 || eprosima_test_StructType_max_key_cdr_typesize > 16)
            {
                m_md5.init();
                m_md5.update(m_keyBuffer, static_cast<unsigned int>(ser.get_serialized_data_length()));
                m_md5.finalize();
                for (uint8_t i = 0; i < 16; ++i)
                {
                    handle->value[i] = m_md5.digest[i];
                }
            }
            else
            {
                for (uint8_t i = 0; i < 16; ++i)
                {
                    handle->value[i] = m_keyBuffer[i];
                }
            }
            return true;
        }



        CompleteTestTypePubSubType::CompleteTestTypePubSubType()
        {
            setName("eprosima::test::CompleteTestType");
            uint32_t type_size = eprosima_test_CompleteTestType_max_cdr_typesize;
            type_size += static_cast<uint32_t>(eprosima::fastcdr::Cdr::alignment(type_size, 4)); /* possible submessage alignment */
            m_typeSize = type_size + 4; /*encapsulation*/
            m_isGetKeyDefined = false;
            uint32_t keyLength = eprosima_test_CompleteTestType_max_key_cdr_typesize > 16 ? eprosima_test_CompleteTestType_max_key_cdr_typesize : 16;
            m_keyBuffer = reinterpret_cast<unsigned char*>(malloc(keyLength));
            memset(m_keyBuffer, 0, keyLength);
        }

        CompleteTestTypePubSubType::~CompleteTestTypePubSubType()
        {
            if (m_keyBuffer != nullptr)
            {
                free(m_keyBuffer);
            }
        }

        bool CompleteTestTypePubSubType::serialize(
                void* data,
                SerializedPayload_t* payload,
                DataRepresentationId_t data_representation)
        {
            CompleteTestType* p_type = static_cast<CompleteTestType*>(data);

            // Object that manages the raw buffer.
            eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(payload->data), payload->max_size);
            // Object that serializes the data.
            eprosima::fastcdr::Cdr ser(fastbuffer, eprosima::fastcdr::Cdr::DEFAULT_ENDIAN,
                    data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                    eprosima::fastcdr::CdrVersion::XCDRv1 : eprosima::fastcdr::CdrVersion::XCDRv2);
            payload->encapsulation = ser.endianness() == eprosima::fastcdr::Cdr::BIG_ENDIANNESS ? CDR_BE : CDR_LE;
            ser.set_encoding_flag(
                data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                eprosima::fastcdr::EncodingAlgorithmFlag::PLAIN_CDR  :
                eprosima::fastcdr::EncodingAlgorithmFlag::DELIMIT_CDR2);

            try
            {
                // Serialize encapsulation
                ser.serialize_encapsulation();
                // Serialize the object.
                ser << *p_type;
            }
            catch (eprosima::fastcdr::exception::Exception& /*exception*/)
            {
                return false;
            }

            // Get the serialized length
            payload->length = static_cast<uint32_t>(ser.get_serialized_data_length());
            return true;
        }

        bool CompleteTestTypePubSubType::deserialize(
                SerializedPayload_t* payload,
                void* data)
        {
            try
            {
                // Convert DATA to pointer of your type
                CompleteTestType* p_type = static_cast<CompleteTestType*>(data);

                // Object that manages the raw buffer.
                eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(payload->data), payload->length);

                // Object that deserializes the data.
                eprosima::fastcdr::Cdr deser(fastbuffer, eprosima::fastcdr::Cdr::DEFAULT_ENDIAN);

                // Deserialize encapsulation.
                deser.read_encapsulation();
                payload->encapsulation = deser.endianness() == eprosima::fastcdr::Cdr::BIG_ENDIANNESS ? CDR_BE : CDR_LE;

                // Deserialize the object.
                deser >> *p_type;
            }
            catch (eprosima::fastcdr::exception::Exception& /*exception*/)
            {
                return false;
            }

            return true;
        }

        std::function<uint32_t()> CompleteTestTypePubSubType::getSerializedSizeProvider(
                void* data,
                DataRepresentationId_t data_representation)
        {
            return [data, data_representation]() -> uint32_t
                   {
                       eprosima::fastcdr::CdrSizeCalculator calculator(
                           data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                           eprosima::fastcdr::CdrVersion::XCDRv1 :eprosima::fastcdr::CdrVersion::XCDRv2);
                       size_t current_alignment {0};
                       return static_cast<uint32_t>(calculator.calculate_serialized_size(
                                   *static_cast<CompleteTestType*>(data), current_alignment)) +
                               4u /*encapsulation*/;
                   };
        }

        void* CompleteTestTypePubSubType::createData()
        {
            return reinterpret_cast<void*>(new CompleteTestType());
        }

        void CompleteTestTypePubSubType::deleteData(
                void* data)
        {
            delete(reinterpret_cast<CompleteTestType*>(data));
        }

        bool CompleteTestTypePubSubType::getKey(
                void* data,
                InstanceHandle_t* handle,
                bool force_md5)
        {
            if (!m_isGetKeyDefined)
            {
                return false;
            }

            CompleteTestType* p_type = static_cast<CompleteTestType*>(data);

            // Object that manages the raw buffer.
            eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(m_keyBuffer),
                    eprosima_test_CompleteTestType_max_key_cdr_typesize);

            // Object that serializes the data.
            eprosima::fastcdr::Cdr ser(fastbuffer, eprosima::fastcdr::Cdr::BIG_ENDIANNESS);
            eprosima::fastcdr::serialize_key(ser, *p_type);
            if (force_md5 || eprosima_test_CompleteTestType_max_key_cdr_typesize > 16)
            {
                m_md5.init();
                m_md5.update(m_keyBuffer, static_cast<unsigned int>(ser.get_serialized_data_length()));
                m_md5.finalize();
                for (uint8_t i = 0; i < 16; ++i)
                {
                    handle->value[i] = m_md5.digest[i];
                }
            }
            else
            {
                for (uint8_t i = 0; i < 16; ++i)
                {
                    handle->value[i] = m_keyBuffer[i];
                }
            }
            return true;
        }

        KeyedCompleteTestTypePubSubType::KeyedCompleteTestTypePubSubType()
        {
            setName("eprosima::test::KeyedCompleteTestType");
            uint32_t type_size = eprosima_test_KeyedCompleteTestType_max_cdr_typesize;
            type_size += static_cast<uint32_t>(eprosima::fastcdr::Cdr::alignment(type_size, 4)); /* possible submessage alignment */
            m_typeSize = type_size + 4; /*encapsulation*/
            m_isGetKeyDefined = true;
            uint32_t keyLength = eprosima_test_KeyedCompleteTestType_max_key_cdr_typesize > 16 ? eprosima_test_KeyedCompleteTestType_max_key_cdr_typesize : 16;
            m_keyBuffer = reinterpret_cast<unsigned char*>(malloc(keyLength));
            memset(m_keyBuffer, 0, keyLength);
        }

        KeyedCompleteTestTypePubSubType::~KeyedCompleteTestTypePubSubType()
        {
            if (m_keyBuffer != nullptr)
            {
                free(m_keyBuffer);
            }
        }

        bool KeyedCompleteTestTypePubSubType::serialize(
                void* data,
                SerializedPayload_t* payload,
                DataRepresentationId_t data_representation)
        {
            KeyedCompleteTestType* p_type = static_cast<KeyedCompleteTestType*>(data);

            // Object that manages the raw buffer.
            eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(payload->data), payload->max_size);
            // Object that serializes the data.
            eprosima::fastcdr::Cdr ser(fastbuffer, eprosima::fastcdr::Cdr::DEFAULT_ENDIAN,
                    data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                    eprosima::fastcdr::CdrVersion::XCDRv1 : eprosima::fastcdr::CdrVersion::XCDRv2);
            payload->encapsulation = ser.endianness() == eprosima::fastcdr::Cdr::BIG_ENDIANNESS ? CDR_BE : CDR_LE;
            ser.set_encoding_flag(
                data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                eprosima::fastcdr::EncodingAlgorithmFlag::PLAIN_CDR  :
                eprosima::fastcdr::EncodingAlgorithmFlag::DELIMIT_CDR2);

            try
            {
                // Serialize encapsulation
                ser.serialize_encapsulation();
                // Serialize the object.
                ser << *p_type;
            }
            catch (eprosima::fastcdr::exception::Exception& /*exception*/)
            {
                return false;
            }

            // Get the serialized length
            payload->length = static_cast<uint32_t>(ser.get_serialized_data_length());
            return true;
        }

        bool KeyedCompleteTestTypePubSubType::deserialize(
                SerializedPayload_t* payload,
                void* data)
        {
            try
            {
                // Convert DATA to pointer of your type
                KeyedCompleteTestType* p_type = static_cast<KeyedCompleteTestType*>(data);

                // Object that manages the raw buffer.
                eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(payload->data), payload->length);

                // Object that deserializes the data.
                eprosima::fastcdr::Cdr deser(fastbuffer, eprosima::fastcdr::Cdr::DEFAULT_ENDIAN);

                // Deserialize encapsulation.
                deser.read_encapsulation();
                payload->encapsulation = deser.endianness() == eprosima::fastcdr::Cdr::BIG_ENDIANNESS ? CDR_BE : CDR_LE;

                // Deserialize the object.
                deser >> *p_type;
            }
            catch (eprosima::fastcdr::exception::Exception& /*exception*/)
            {
                return false;
            }

            return true;
        }

        std::function<uint32_t()> KeyedCompleteTestTypePubSubType::getSerializedSizeProvider(
                void* data,
                DataRepresentationId_t data_representation)
        {
            return [data, data_representation]() -> uint32_t
                   {
                       eprosima::fastcdr::CdrSizeCalculator calculator(
                           data_representation == DataRepresentationId_t::XCDR_DATA_REPRESENTATION ?
                           eprosima::fastcdr::CdrVersion::XCDRv1 :eprosima::fastcdr::CdrVersion::XCDRv2);
                       size_t current_alignment {0};
                       return static_cast<uint32_t>(calculator.calculate_serialized_size(
                                   *static_cast<KeyedCompleteTestType*>(data), current_alignment)) +
                               4u /*encapsulation*/;
                   };
        }

        void* KeyedCompleteTestTypePubSubType::createData()
        {
            return reinterpret_cast<void*>(new KeyedCompleteTestType());
        }

        void KeyedCompleteTestTypePubSubType::deleteData(
                void* data)
        {
            delete(reinterpret_cast<KeyedCompleteTestType*>(data));
        }

        bool KeyedCompleteTestTypePubSubType::getKey(
                void* data,
                InstanceHandle_t* handle,
                bool force_md5)
        {
            if (!m_isGetKeyDefined)
            {
                return false;
            }

            KeyedCompleteTestType* p_type = static_cast<KeyedCompleteTestType*>(data);

            // Object that manages the raw buffer.
            eprosima::fastcdr::FastBuffer fastbuffer(reinterpret_cast<char*>(m_keyBuffer),
                    eprosima_test_KeyedCompleteTestType_max_key_cdr_typesize);

            // Object that serializes the data.
            eprosima::fastcdr::Cdr ser(fastbuffer, eprosima::fastcdr::Cdr::BIG_ENDIANNESS);
            eprosima::fastcdr::serialize_key(ser, *p_type);
            if (force_md5 || eprosima_test_KeyedCompleteTestType_max_key_cdr_typesize > 16)
            {
                m_md5.init();
                m_md5.update(m_keyBuffer, static_cast<unsigned int>(ser.get_serialized_data_length()));
                m_md5.finalize();
                for (uint8_t i = 0; i < 16; ++i)
                {
                    handle->value[i] = m_md5.digest[i];
                }
            }
            else
            {
                for (uint8_t i = 0; i < 16; ++i)
                {
                    handle->value[i] = m_keyBuffer[i];
                }
            }
            return true;
        }


    } //End of namespace test


} //End of namespace eprosima

