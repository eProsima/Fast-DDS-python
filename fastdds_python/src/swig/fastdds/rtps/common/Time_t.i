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
#include <fastdds/rtps/common/Time_t.hpp>
%}

// There are two definitions of Time_t in different namespaces
// As SWIG flattens the namespaces, we cannot have two classes with the same name
// We remove the one that is not used in the user API
// We also remove all the related operators
%rename(RTPSTime_t) eprosima::fastdds::rtps::Time_t;
%ignore eprosima::fastdds::rtps::operator==(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator!=(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator<(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator<=(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator>(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator>=(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator+(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator-(const Time_t&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator<<(std::ostream&, const Time_t&);
%ignore eprosima::fastdds::rtps::operator>>(std::istream&, Time_t&);

%include <fastdds/rtps/common/Time_t.hpp>
