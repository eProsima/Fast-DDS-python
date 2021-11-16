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
#include "fastdds/rtps/common/LocatorList.hpp"
%}

// Ignore deprecated methods
%ignore eprosima::fastdds::rtps::LocatorList::contains;

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastdds::rtps::LocatorList::LocatorList(LocatorList &&);

// For some reason, these need to be explicitly ignored, the global ignore is not enough
%ignore eprosima::fastdds::rtps::operator<<(std::ostream& output,const LocatorList& locList);
%ignore eprosima::fastdds::rtps::operator>>(std::istream& output,LocatorList& locList);

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(Locator_vector) std::vector<eprosima::fastdds::rtps::Locator>;

%include "fastdds/rtps/common/LocatorList.hpp"
