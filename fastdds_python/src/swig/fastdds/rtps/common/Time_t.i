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
#include "fastdds/rtps/common/Time_t.h"
%}

// There are two definitions of Time_t in different namespaces
// As SWIG flattens the namespaces, we cannot have two classes with the same name
// We remove the one that is not used in the user API
// We also remove all the related operators
%ignore eprosima::fastrtps::rtps::Time_t;
%ignore eprosima::fastrtps::rtps::operator==(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator!=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator<(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator<=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator>(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator>=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator+(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator-(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const Time_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const Time_t&);

// Also ignore the insertion/exraction operator of the remaining Time_t,
// as it makes no sense on the target language
%ignore eprosima::fastrtps::operator<<(std::ostream&, const Time_t&);
%ignore eprosima::fastrtps::operator>>(std::ostream&, const Time_t&);

// Ignore the global comparison and arithmetic operators
// and make them class-internal
%ignore eprosima::fastrtps::operator==(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator!=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator<(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator<=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator>(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator>=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator+(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator-(const Time_t&, const Time_t&);

%include "fastdds/rtps/common/Time_t.h"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::Time_t {
    bool operator==(const eprosima::fastrtps::Time_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::Time_t& other) const
    {
        return *$self != other;
    }

    bool operator<(const eprosima::fastrtps::Time_t& other) const
    {
        return *$self < other;
    }

    bool operator>(const eprosima::fastrtps::Time_t& other) const
    {
        return *$self > other;
    }

    bool operator<=(const eprosima::fastrtps::Time_t& other) const
    {
        return *$self <= other;
    }

    bool operator>=(const eprosima::fastrtps::Time_t& other) const
    {
        return *$self >= other;
    }

    eprosima::fastrtps::Time_t operator+ (const eprosima::fastrtps::Time_t& other) const
    {
        return *$self + other;
    }

    eprosima::fastrtps::Time_t operator- (const eprosima::fastrtps::Time_t& other) const
    {
        return *$self - other;
    }
}

