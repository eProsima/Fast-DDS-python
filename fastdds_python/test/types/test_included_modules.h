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
 * @file test_included_modules.h
 * This header file contains the declaration of the described types in the IDL file.
 *
 * This file was generated by the tool gen.
 */

#ifndef _FAST_DDS_GENERATED_EPROSIMA_TEST2_TEST_INCLUDED_MODULES_H_
#define _FAST_DDS_GENERATED_EPROSIMA_TEST2_TEST_INCLUDED_MODULES_H_


#include <fastrtps/utils/fixed_size_string.hpp>

#include <stdint.h>
#include <array>
#include <string>
#include <vector>
#include <map>
#include <bitset>

#if defined(_WIN32)
#if defined(EPROSIMA_USER_DLL_EXPORT)
#define eProsima_user_DllExport __declspec( dllexport )
#else
#define eProsima_user_DllExport
#endif  // EPROSIMA_USER_DLL_EXPORT
#else
#define eProsima_user_DllExport
#endif  // _WIN32

#if defined(_WIN32)
#if defined(EPROSIMA_USER_DLL_EXPORT)
#if defined(TEST_INCLUDED_MODULES_SOURCE)
#define TEST_INCLUDED_MODULES_DllAPI __declspec( dllexport )
#else
#define TEST_INCLUDED_MODULES_DllAPI __declspec( dllimport )
#endif // TEST_INCLUDED_MODULES_SOURCE
#else
#define TEST_INCLUDED_MODULES_DllAPI
#endif  // EPROSIMA_USER_DLL_EXPORT
#else
#define TEST_INCLUDED_MODULES_DllAPI
#endif // _WIN32

namespace eprosima {
namespace fastcdr {
class Cdr;
} // namespace fastcdr
} // namespace eprosima


namespace eprosima {
    namespace test2 {
        /*!
         * @brief This class represents the enumeration Color2 defined by the user in the IDL file.
         * @ingroup test_included_modules
         */
        enum Color2 : uint32_t
        {
            RED2,
            GREEN2,
            BLUE2,
            YELLOW2,
            MAGENTA2
        };
        /*!
         * @brief This class represents the enumeration Material2 defined by the user in the IDL file.
         * @ingroup test_included_modules
         */
        enum Material2 : uint32_t
        {
            WOOD2,
            PLASTIC2,
            METAL2,
            CONCRETE2,
            STONE2
        };
        /*!
         * @brief This class represents the structure StructType2 defined by the user in the IDL file.
         * @ingroup test_included_modules
         */
        class StructType2
        {
        public:

            /*!
             * @brief Default constructor.
             */
            eProsima_user_DllExport StructType2();

            /*!
             * @brief Default destructor.
             */
            eProsima_user_DllExport ~StructType2();

            /*!
             * @brief Copy constructor.
             * @param x Reference to the object eprosima::test2::StructType2 that will be copied.
             */
            eProsima_user_DllExport StructType2(
                    const StructType2& x);

            /*!
             * @brief Move constructor.
             * @param x Reference to the object eprosima::test2::StructType2 that will be copied.
             */
            eProsima_user_DllExport StructType2(
                    StructType2&& x) noexcept;

            /*!
             * @brief Copy assignment.
             * @param x Reference to the object eprosima::test2::StructType2 that will be copied.
             */
            eProsima_user_DllExport StructType2& operator =(
                    const StructType2& x);

            /*!
             * @brief Move assignment.
             * @param x Reference to the object eprosima::test2::StructType2 that will be copied.
             */
            eProsima_user_DllExport StructType2& operator =(
                    StructType2&& x) noexcept;

            /*!
             * @brief Comparison operator.
             * @param x eprosima::test2::StructType2 object to compare.
             */
            eProsima_user_DllExport bool operator ==(
                    const StructType2& x) const;

            /*!
             * @brief Comparison operator.
             * @param x eprosima::test2::StructType2 object to compare.
             */
            eProsima_user_DllExport bool operator !=(
                    const StructType2& x) const;

            /*!
             * @brief This function sets a value in member char_field
             * @param _char_field New value for member char_field
             */
            eProsima_user_DllExport void char_field(
                    char _char_field);

            /*!
             * @brief This function returns the value of member char_field
             * @return Value of member char_field
             */
            eProsima_user_DllExport char char_field() const;

            /*!
             * @brief This function returns a reference to member char_field
             * @return Reference to member char_field
             */
            eProsima_user_DllExport char& char_field();

            /*!
             * @brief This function sets a value in member uint8_field
             * @param _uint8_field New value for member uint8_field
             */
            eProsima_user_DllExport void uint8_field(
                    uint8_t _uint8_field);

            /*!
             * @brief This function returns the value of member uint8_field
             * @return Value of member uint8_field
             */
            eProsima_user_DllExport uint8_t uint8_field() const;

            /*!
             * @brief This function returns a reference to member uint8_field
             * @return Reference to member uint8_field
             */
            eProsima_user_DllExport uint8_t& uint8_field();

            /*!
             * @brief This function sets a value in member int16_field
             * @param _int16_field New value for member int16_field
             */
            eProsima_user_DllExport void int16_field(
                    int16_t _int16_field);

            /*!
             * @brief This function returns the value of member int16_field
             * @return Value of member int16_field
             */
            eProsima_user_DllExport int16_t int16_field() const;

            /*!
             * @brief This function returns a reference to member int16_field
             * @return Reference to member int16_field
             */
            eProsima_user_DllExport int16_t& int16_field();

            /*!
             * @brief This function sets a value in member uint16_field
             * @param _uint16_field New value for member uint16_field
             */
            eProsima_user_DllExport void uint16_field(
                    uint16_t _uint16_field);

            /*!
             * @brief This function returns the value of member uint16_field
             * @return Value of member uint16_field
             */
            eProsima_user_DllExport uint16_t uint16_field() const;

            /*!
             * @brief This function returns a reference to member uint16_field
             * @return Reference to member uint16_field
             */
            eProsima_user_DllExport uint16_t& uint16_field();

            /*!
             * @brief This function sets a value in member int32_field
             * @param _int32_field New value for member int32_field
             */
            eProsima_user_DllExport void int32_field(
                    int32_t _int32_field);

            /*!
             * @brief This function returns the value of member int32_field
             * @return Value of member int32_field
             */
            eProsima_user_DllExport int32_t int32_field() const;

            /*!
             * @brief This function returns a reference to member int32_field
             * @return Reference to member int32_field
             */
            eProsima_user_DllExport int32_t& int32_field();

            /*!
             * @brief This function sets a value in member uint32_field
             * @param _uint32_field New value for member uint32_field
             */
            eProsima_user_DllExport void uint32_field(
                    uint32_t _uint32_field);

            /*!
             * @brief This function returns the value of member uint32_field
             * @return Value of member uint32_field
             */
            eProsima_user_DllExport uint32_t uint32_field() const;

            /*!
             * @brief This function returns a reference to member uint32_field
             * @return Reference to member uint32_field
             */
            eProsima_user_DllExport uint32_t& uint32_field();

            /*!
             * @brief This function sets a value in member int64_field
             * @param _int64_field New value for member int64_field
             */
            eProsima_user_DllExport void int64_field(
                    int64_t _int64_field);

            /*!
             * @brief This function returns the value of member int64_field
             * @return Value of member int64_field
             */
            eProsima_user_DllExport int64_t int64_field() const;

            /*!
             * @brief This function returns a reference to member int64_field
             * @return Reference to member int64_field
             */
            eProsima_user_DllExport int64_t& int64_field();

            /*!
             * @brief This function sets a value in member uint64_field
             * @param _uint64_field New value for member uint64_field
             */
            eProsima_user_DllExport void uint64_field(
                    uint64_t _uint64_field);

            /*!
             * @brief This function returns the value of member uint64_field
             * @return Value of member uint64_field
             */
            eProsima_user_DllExport uint64_t uint64_field() const;

            /*!
             * @brief This function returns a reference to member uint64_field
             * @return Reference to member uint64_field
             */
            eProsima_user_DllExport uint64_t& uint64_field();

            /*!
             * @brief This function sets a value in member float_field
             * @param _float_field New value for member float_field
             */
            eProsima_user_DllExport void float_field(
                    float _float_field);

            /*!
             * @brief This function returns the value of member float_field
             * @return Value of member float_field
             */
            eProsima_user_DllExport float float_field() const;

            /*!
             * @brief This function returns a reference to member float_field
             * @return Reference to member float_field
             */
            eProsima_user_DllExport float& float_field();

            /*!
             * @brief This function sets a value in member double_field
             * @param _double_field New value for member double_field
             */
            eProsima_user_DllExport void double_field(
                    double _double_field);

            /*!
             * @brief This function returns the value of member double_field
             * @return Value of member double_field
             */
            eProsima_user_DllExport double double_field() const;

            /*!
             * @brief This function returns a reference to member double_field
             * @return Reference to member double_field
             */
            eProsima_user_DllExport double& double_field();

            /*!
             * @brief This function sets a value in member bool_field
             * @param _bool_field New value for member bool_field
             */
            eProsima_user_DllExport void bool_field(
                    bool _bool_field);

            /*!
             * @brief This function returns the value of member bool_field
             * @return Value of member bool_field
             */
            eProsima_user_DllExport bool bool_field() const;

            /*!
             * @brief This function returns a reference to member bool_field
             * @return Reference to member bool_field
             */
            eProsima_user_DllExport bool& bool_field();

            /*!
             * @brief This function copies the value in member string_field
             * @param _string_field New value to be copied in member string_field
             */
            eProsima_user_DllExport void string_field(
                    const std::string& _string_field);

            /*!
             * @brief This function moves the value in member string_field
             * @param _string_field New value to be moved in member string_field
             */
            eProsima_user_DllExport void string_field(
                    std::string&& _string_field);

            /*!
             * @brief This function returns a constant reference to member string_field
             * @return Constant reference to member string_field
             */
            eProsima_user_DllExport const std::string& string_field() const;

            /*!
             * @brief This function returns a reference to member string_field
             * @return Reference to member string_field
             */
            eProsima_user_DllExport std::string& string_field();
            /*!
             * @brief This function sets a value in member enum_field
             * @param _enum_field New value for member enum_field
             */
            eProsima_user_DllExport void enum_field(
                    eprosima::test2::Color2 _enum_field);

            /*!
             * @brief This function returns the value of member enum_field
             * @return Value of member enum_field
             */
            eProsima_user_DllExport eprosima::test2::Color2 enum_field() const;

            /*!
             * @brief This function returns a reference to member enum_field
             * @return Reference to member enum_field
             */
            eProsima_user_DllExport eprosima::test2::Color2& enum_field();

            /*!
             * @brief This function sets a value in member enum2_field
             * @param _enum2_field New value for member enum2_field
             */
            eProsima_user_DllExport void enum2_field(
                    eprosima::test2::Material2 _enum2_field);

            /*!
             * @brief This function returns the value of member enum2_field
             * @return Value of member enum2_field
             */
            eProsima_user_DllExport eprosima::test2::Material2 enum2_field() const;

            /*!
             * @brief This function returns a reference to member enum2_field
             * @return Reference to member enum2_field
             */
            eProsima_user_DllExport eprosima::test2::Material2& enum2_field();


            /*!
            * @brief This function returns the maximum serialized size of an object
            * depending on the buffer alignment.
            * @param current_alignment Buffer alignment.
            * @return Maximum serialized size.
            */
            eProsima_user_DllExport static size_t getMaxCdrSerializedSize(
                    size_t current_alignment = 0);

            /*!
             * @brief This function returns the serialized size of a data depending on the buffer alignment.
             * @param data Data which is calculated its serialized size.
             * @param current_alignment Buffer alignment.
             * @return Serialized size.
             */
            eProsima_user_DllExport static size_t getCdrSerializedSize(
                    const eprosima::test2::StructType2& data,
                    size_t current_alignment = 0);


            /*!
             * @brief This function serializes an object using CDR serialization.
             * @param cdr CDR serialization object.
             */
            eProsima_user_DllExport void serialize(
                    eprosima::fastcdr::Cdr& cdr) const;

            /*!
             * @brief This function deserializes an object using CDR serialization.
             * @param cdr CDR serialization object.
             */
            eProsima_user_DllExport void deserialize(
                    eprosima::fastcdr::Cdr& cdr);



            /*!
             * @brief This function returns the maximum serialized size of the Key of an object
             * depending on the buffer alignment.
             * @param current_alignment Buffer alignment.
             * @return Maximum serialized size.
             */
            eProsima_user_DllExport static size_t getKeyMaxCdrSerializedSize(
                    size_t current_alignment = 0);

            /*!
             * @brief This function tells you if the Key has been defined for this type
             */
            eProsima_user_DllExport static bool isKeyDefined();

            /*!
             * @brief This function serializes the key members of an object using CDR serialization.
             * @param cdr CDR serialization object.
             */
            eProsima_user_DllExport void serializeKey(
                    eprosima::fastcdr::Cdr& cdr) const;

        private:

            char m_char_field;
            uint8_t m_uint8_field;
            int16_t m_int16_field;
            uint16_t m_uint16_field;
            int32_t m_int32_field;
            uint32_t m_uint32_field;
            int64_t m_int64_field;
            uint64_t m_uint64_field;
            float m_float_field;
            double m_double_field;
            bool m_bool_field;
            std::string m_string_field;
            eprosima::test2::Color2 m_enum_field;
            eprosima::test2::Material2 m_enum2_field;

        };
    } // namespace test2
} // namespace eprosima

#endif // _FAST_DDS_GENERATED_EPROSIMA_TEST2_TEST_INCLUDED_MODULES_H_

