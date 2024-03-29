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
 * @file test_included_modules.cpp
 * This source file contains the implementation of the described types in the IDL file.
 *
 * This file was generated by the tool fastddsgen.
 */

#ifdef _WIN32
// Remove linker warning LNK4221 on Visual Studio
namespace {
char dummy;
}  // namespace
#endif  // _WIN32

#include "test_included_modules.h"

#if FASTCDR_VERSION_MAJOR > 1

#include <fastcdr/Cdr.h>


#include <fastcdr/exceptions/BadParamException.h>
using namespace eprosima::fastcdr::exception;

#include <utility>


namespace eprosima {

namespace test2 {



StructType2::StructType2()
{
}

StructType2::~StructType2()
{
}

StructType2::StructType2(
        const StructType2& x)
{
    m_char_field = x.m_char_field;
    m_uint8_field = x.m_uint8_field;
    m_int16_field = x.m_int16_field;
    m_uint16_field = x.m_uint16_field;
    m_int32_field = x.m_int32_field;
    m_uint32_field = x.m_uint32_field;
    m_int64_field = x.m_int64_field;
    m_uint64_field = x.m_uint64_field;
    m_float_field = x.m_float_field;
    m_double_field = x.m_double_field;
    m_bool_field = x.m_bool_field;
    m_string_field = x.m_string_field;
    m_enum_field = x.m_enum_field;
    m_enum2_field = x.m_enum2_field;
}

StructType2::StructType2(
        StructType2&& x) noexcept
{
    m_char_field = x.m_char_field;
    m_uint8_field = x.m_uint8_field;
    m_int16_field = x.m_int16_field;
    m_uint16_field = x.m_uint16_field;
    m_int32_field = x.m_int32_field;
    m_uint32_field = x.m_uint32_field;
    m_int64_field = x.m_int64_field;
    m_uint64_field = x.m_uint64_field;
    m_float_field = x.m_float_field;
    m_double_field = x.m_double_field;
    m_bool_field = x.m_bool_field;
    m_string_field = std::move(x.m_string_field);
    m_enum_field = x.m_enum_field;
    m_enum2_field = x.m_enum2_field;
}

StructType2& StructType2::operator =(
        const StructType2& x)
{

    m_char_field = x.m_char_field;
    m_uint8_field = x.m_uint8_field;
    m_int16_field = x.m_int16_field;
    m_uint16_field = x.m_uint16_field;
    m_int32_field = x.m_int32_field;
    m_uint32_field = x.m_uint32_field;
    m_int64_field = x.m_int64_field;
    m_uint64_field = x.m_uint64_field;
    m_float_field = x.m_float_field;
    m_double_field = x.m_double_field;
    m_bool_field = x.m_bool_field;
    m_string_field = x.m_string_field;
    m_enum_field = x.m_enum_field;
    m_enum2_field = x.m_enum2_field;
    return *this;
}

StructType2& StructType2::operator =(
        StructType2&& x) noexcept
{

    m_char_field = x.m_char_field;
    m_uint8_field = x.m_uint8_field;
    m_int16_field = x.m_int16_field;
    m_uint16_field = x.m_uint16_field;
    m_int32_field = x.m_int32_field;
    m_uint32_field = x.m_uint32_field;
    m_int64_field = x.m_int64_field;
    m_uint64_field = x.m_uint64_field;
    m_float_field = x.m_float_field;
    m_double_field = x.m_double_field;
    m_bool_field = x.m_bool_field;
    m_string_field = std::move(x.m_string_field);
    m_enum_field = x.m_enum_field;
    m_enum2_field = x.m_enum2_field;
    return *this;
}

bool StructType2::operator ==(
        const StructType2& x) const
{
    return (m_char_field == x.m_char_field &&
           m_uint8_field == x.m_uint8_field &&
           m_int16_field == x.m_int16_field &&
           m_uint16_field == x.m_uint16_field &&
           m_int32_field == x.m_int32_field &&
           m_uint32_field == x.m_uint32_field &&
           m_int64_field == x.m_int64_field &&
           m_uint64_field == x.m_uint64_field &&
           m_float_field == x.m_float_field &&
           m_double_field == x.m_double_field &&
           m_bool_field == x.m_bool_field &&
           m_string_field == x.m_string_field &&
           m_enum_field == x.m_enum_field &&
           m_enum2_field == x.m_enum2_field);
}

bool StructType2::operator !=(
        const StructType2& x) const
{
    return !(*this == x);
}

/*!
 * @brief This function sets a value in member char_field
 * @param _char_field New value for member char_field
 */
void StructType2::char_field(
        char _char_field)
{
    m_char_field = _char_field;
}

/*!
 * @brief This function returns the value of member char_field
 * @return Value of member char_field
 */
char StructType2::char_field() const
{
    return m_char_field;
}

/*!
 * @brief This function returns a reference to member char_field
 * @return Reference to member char_field
 */
char& StructType2::char_field()
{
    return m_char_field;
}


/*!
 * @brief This function sets a value in member uint8_field
 * @param _uint8_field New value for member uint8_field
 */
void StructType2::uint8_field(
        uint8_t _uint8_field)
{
    m_uint8_field = _uint8_field;
}

/*!
 * @brief This function returns the value of member uint8_field
 * @return Value of member uint8_field
 */
uint8_t StructType2::uint8_field() const
{
    return m_uint8_field;
}

/*!
 * @brief This function returns a reference to member uint8_field
 * @return Reference to member uint8_field
 */
uint8_t& StructType2::uint8_field()
{
    return m_uint8_field;
}


/*!
 * @brief This function sets a value in member int16_field
 * @param _int16_field New value for member int16_field
 */
void StructType2::int16_field(
        int16_t _int16_field)
{
    m_int16_field = _int16_field;
}

/*!
 * @brief This function returns the value of member int16_field
 * @return Value of member int16_field
 */
int16_t StructType2::int16_field() const
{
    return m_int16_field;
}

/*!
 * @brief This function returns a reference to member int16_field
 * @return Reference to member int16_field
 */
int16_t& StructType2::int16_field()
{
    return m_int16_field;
}


/*!
 * @brief This function sets a value in member uint16_field
 * @param _uint16_field New value for member uint16_field
 */
void StructType2::uint16_field(
        uint16_t _uint16_field)
{
    m_uint16_field = _uint16_field;
}

/*!
 * @brief This function returns the value of member uint16_field
 * @return Value of member uint16_field
 */
uint16_t StructType2::uint16_field() const
{
    return m_uint16_field;
}

/*!
 * @brief This function returns a reference to member uint16_field
 * @return Reference to member uint16_field
 */
uint16_t& StructType2::uint16_field()
{
    return m_uint16_field;
}


/*!
 * @brief This function sets a value in member int32_field
 * @param _int32_field New value for member int32_field
 */
void StructType2::int32_field(
        int32_t _int32_field)
{
    m_int32_field = _int32_field;
}

/*!
 * @brief This function returns the value of member int32_field
 * @return Value of member int32_field
 */
int32_t StructType2::int32_field() const
{
    return m_int32_field;
}

/*!
 * @brief This function returns a reference to member int32_field
 * @return Reference to member int32_field
 */
int32_t& StructType2::int32_field()
{
    return m_int32_field;
}


/*!
 * @brief This function sets a value in member uint32_field
 * @param _uint32_field New value for member uint32_field
 */
void StructType2::uint32_field(
        uint32_t _uint32_field)
{
    m_uint32_field = _uint32_field;
}

/*!
 * @brief This function returns the value of member uint32_field
 * @return Value of member uint32_field
 */
uint32_t StructType2::uint32_field() const
{
    return m_uint32_field;
}

/*!
 * @brief This function returns a reference to member uint32_field
 * @return Reference to member uint32_field
 */
uint32_t& StructType2::uint32_field()
{
    return m_uint32_field;
}


/*!
 * @brief This function sets a value in member int64_field
 * @param _int64_field New value for member int64_field
 */
void StructType2::int64_field(
        int64_t _int64_field)
{
    m_int64_field = _int64_field;
}

/*!
 * @brief This function returns the value of member int64_field
 * @return Value of member int64_field
 */
int64_t StructType2::int64_field() const
{
    return m_int64_field;
}

/*!
 * @brief This function returns a reference to member int64_field
 * @return Reference to member int64_field
 */
int64_t& StructType2::int64_field()
{
    return m_int64_field;
}


/*!
 * @brief This function sets a value in member uint64_field
 * @param _uint64_field New value for member uint64_field
 */
void StructType2::uint64_field(
        uint64_t _uint64_field)
{
    m_uint64_field = _uint64_field;
}

/*!
 * @brief This function returns the value of member uint64_field
 * @return Value of member uint64_field
 */
uint64_t StructType2::uint64_field() const
{
    return m_uint64_field;
}

/*!
 * @brief This function returns a reference to member uint64_field
 * @return Reference to member uint64_field
 */
uint64_t& StructType2::uint64_field()
{
    return m_uint64_field;
}


/*!
 * @brief This function sets a value in member float_field
 * @param _float_field New value for member float_field
 */
void StructType2::float_field(
        float _float_field)
{
    m_float_field = _float_field;
}

/*!
 * @brief This function returns the value of member float_field
 * @return Value of member float_field
 */
float StructType2::float_field() const
{
    return m_float_field;
}

/*!
 * @brief This function returns a reference to member float_field
 * @return Reference to member float_field
 */
float& StructType2::float_field()
{
    return m_float_field;
}


/*!
 * @brief This function sets a value in member double_field
 * @param _double_field New value for member double_field
 */
void StructType2::double_field(
        double _double_field)
{
    m_double_field = _double_field;
}

/*!
 * @brief This function returns the value of member double_field
 * @return Value of member double_field
 */
double StructType2::double_field() const
{
    return m_double_field;
}

/*!
 * @brief This function returns a reference to member double_field
 * @return Reference to member double_field
 */
double& StructType2::double_field()
{
    return m_double_field;
}


/*!
 * @brief This function sets a value in member bool_field
 * @param _bool_field New value for member bool_field
 */
void StructType2::bool_field(
        bool _bool_field)
{
    m_bool_field = _bool_field;
}

/*!
 * @brief This function returns the value of member bool_field
 * @return Value of member bool_field
 */
bool StructType2::bool_field() const
{
    return m_bool_field;
}

/*!
 * @brief This function returns a reference to member bool_field
 * @return Reference to member bool_field
 */
bool& StructType2::bool_field()
{
    return m_bool_field;
}


/*!
 * @brief This function copies the value in member string_field
 * @param _string_field New value to be copied in member string_field
 */
void StructType2::string_field(
        const std::string& _string_field)
{
    m_string_field = _string_field;
}

/*!
 * @brief This function moves the value in member string_field
 * @param _string_field New value to be moved in member string_field
 */
void StructType2::string_field(
        std::string&& _string_field)
{
    m_string_field = std::move(_string_field);
}

/*!
 * @brief This function returns a constant reference to member string_field
 * @return Constant reference to member string_field
 */
const std::string& StructType2::string_field() const
{
    return m_string_field;
}

/*!
 * @brief This function returns a reference to member string_field
 * @return Reference to member string_field
 */
std::string& StructType2::string_field()
{
    return m_string_field;
}


/*!
 * @brief This function sets a value in member enum_field
 * @param _enum_field New value for member enum_field
 */
void StructType2::enum_field(
        eprosima::test2::Color2 _enum_field)
{
    m_enum_field = _enum_field;
}

/*!
 * @brief This function returns the value of member enum_field
 * @return Value of member enum_field
 */
eprosima::test2::Color2 StructType2::enum_field() const
{
    return m_enum_field;
}

/*!
 * @brief This function returns a reference to member enum_field
 * @return Reference to member enum_field
 */
eprosima::test2::Color2& StructType2::enum_field()
{
    return m_enum_field;
}


/*!
 * @brief This function sets a value in member enum2_field
 * @param _enum2_field New value for member enum2_field
 */
void StructType2::enum2_field(
        eprosima::test2::Material2 _enum2_field)
{
    m_enum2_field = _enum2_field;
}

/*!
 * @brief This function returns the value of member enum2_field
 * @return Value of member enum2_field
 */
eprosima::test2::Material2 StructType2::enum2_field() const
{
    return m_enum2_field;
}

/*!
 * @brief This function returns a reference to member enum2_field
 * @return Reference to member enum2_field
 */
eprosima::test2::Material2& StructType2::enum2_field()
{
    return m_enum2_field;
}




} // namespace test2


} // namespace eprosima
// Include auxiliary functions like for serializing/deserializing.
#include "test_included_modulesCdrAux.ipp"

#endif // FASTCDR_VERSION_MAJOR > 1
