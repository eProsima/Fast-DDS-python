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
#include "fastdds/rtps/common/GuidPrefix_t.hpp"

// Define a hash method in global scope for GuidPrefix_t types
// This is necessary if we want other classes to hash an internal GuidPrefix_t
long hash(const eprosima::fastrtps::rtps::GuidPrefix_t& prefix)
{
    long ret = 0;
    for (unsigned int i = 0; i < eprosima::fastrtps::rtps::GuidPrefix_t::size; ++i)
    {
        ret = (ret * 31) ^ prefix.value[i];
    }
    return ret;
}
%}

%include "fastdds/rtps/common/GuidPrefix_t.hpp"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::GuidPrefix_t {
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

