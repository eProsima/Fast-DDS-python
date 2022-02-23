// Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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

%{
#include "fastdds/rtps/common/InstanceHandle.h"

// Define a hash method in global scope for GuidPrefix_t types
// This is necessary if we want other classes to hash an internal GuidPrefix_t
long hash(const eprosima::fastrtps::rtps::InstanceHandle_t& handle)
{
    long ret = 0;
    for (unsigned int i = 0; i < 16; ++i)
    {
        ret = (ret * 31) ^ handle.value[i];
    }
    return ret;
}

%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

%ignore eprosima::fastrtps::rtps::InstanceHandleValue_t::operator [] const;
%ignore eprosima::fastrtps::rtps::operator <<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator >>(std::istream&, InstanceHandle_t&);
%rename(read_pointer_cast) eprosima::fastrtps::rtps::InstanceHandleValue_t::operator const octet* () const;
%rename(write_pointer_cast) eprosima::fastrtps::rtps::InstanceHandleValue_t::operator octet* ();

%include "fastdds/rtps/common/InstanceHandle.h"

namespace eprosima {
namespace fastdds {
namespace dds {

using InstanceHandle_t = eprosima::fastrtps::rtps::InstanceHandle_t;

} // namespace dds
} // namespace fastdds
} // namespace eprosima

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::InstanceHandle_t {

    bool operator==(const eprosima::fastrtps::rtps::InstanceHandle_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::InstanceHandle_t& other) const
    {
        return *$self != other;
    }

    std::string __str__() const
    {
        std::ostringstream out;
        out << *$self;
        return out.str();
    }

    // Define the hash method using the global one
    long __hash__() const
    {
        return hash(*$self);
    }
}
