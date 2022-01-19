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
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const InstanceHandle_t&);

%include "fastdds/rtps/common/InstanceHandle.h"
