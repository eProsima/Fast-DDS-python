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
#include "fastdds/dds/core/status/StatusMask.hpp"
%}

// This class is defined as a subclass of std::bitset<size_t(16)>
// However, SWIG choked parsing this, but could parse std::bitset<16>
// Furthermore, SWIG does not have any wrapper for std::bitset
//  - We create a workaround defining sizet(16)=16
//  - We ignore the warning about not knowing bitset.
// This will only affect in that the resulting class cannot be used in a polymorphic way, but we so not need it.
#define size_t(n) n
%warnfilter(401) eprosima::fastdds::dds::StatusMask;

%extend eprosima::fastdds::dds::StatusMask
{
    bool operator ==(const StatusMask& other_mask) const
    {
        std::cout << "self = " << self->to_string() << std::endl;
        std::cout << "other = " << other_mask.to_string() << std::endl;
        return *self == other_mask;
    }

    StatusMask operator <<(const StatusMask& mask)
    {
        eprosima::fastdds::dds::StatusMask result(*self << mask);
        return result;
    }
}

%ignore eprosima::fastdds::dds::StatusMask::operator <<(const StatusMask&);

%include "fastdds/dds/core/status/StatusMask.hpp"

#undef size_t(n)
