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
#include "fastdds/rtps/common/Guid.h"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_instance_handle) eprosima::fastrtps::rtps::GUID_t::operator const InstanceHandle_t&;

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const GUID_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const GUID_t&);

// Ignore the global comparison operators and make them class-internal
%ignore eprosima::fastrtps::operator==(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator!=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator<(const Time_t&, const Time_t&);

%include "fastdds/rtps/common/Guid.h"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::GUID_t {
    bool operator==(const eprosima::fastrtps::rtps::GUID_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::GUID_t& other) const
    {
        return *$self != other;
    }

    bool operator<(const eprosima::fastrtps::rtps::GUID_t& other) const
    {
        return *$self < other;
    }
}

