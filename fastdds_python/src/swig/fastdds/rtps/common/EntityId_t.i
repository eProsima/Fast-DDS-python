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
#include "fastdds/rtps/common/EntityId_t.hpp"
%}

// Overloaded constructor ignored
%ignore eprosima::fastrtps::rtps::EntityId_t::EntityId_t(EntityId_t &&);

// Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator==;
%ignore eprosima::fastrtps::rtps::operator!=;

// Declare hash so that we do not get a warning
// This will make an empty class on the target, but the user should not need this anyway.
namespace std {
    template <typename T>
    struct hash;
}

%include "fastdds/rtps/common/EntityId_t.hpp"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::EntityId_t {
    bool operator==(const eprosima::fastrtps::rtps::EntityId_t& other) const
    {
        return *$self == other;
    }

    bool operator==(uint32_t other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::EntityId_t& other) const
    {
        return *$self != other;
    }
}
