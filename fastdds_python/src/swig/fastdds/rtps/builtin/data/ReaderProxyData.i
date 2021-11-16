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
#include "fastdds/rtps/builtin/data/ReaderProxyData.h"
%}

namespace eprosima {
namespace fastrtps {

using ReaderQos = eprosima::fastdds::dds::ReaderQos;

} // namespace fastrtps
} // namespace eprosima

// Ignore overloads that meake no sense on Python and cause warnings on compilation
%ignore eprosima::fastrtps::rtps::ReaderProxyData::guid(GUID_t&&);
%ignore eprosima::fastrtps::rtps::ReaderProxyData::guid() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::key(InstanceHandle_t&&);
%ignore eprosima::fastrtps::rtps::ReaderProxyData::key() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::RTPSParticipantKey(InstanceHandle_t&&);
%ignore eprosima::fastrtps::rtps::ReaderProxyData::RTPSParticipantKey() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::typeName(string_255&&);
%ignore eprosima::fastrtps::rtps::ReaderProxyData::typeName() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::topicName(string_255&&);
%ignore eprosima::fastrtps::rtps::ReaderProxyData::topicName() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::userDefinedId() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::isAlive() const;
%ignore eprosima::fastrtps::rtps::ReaderProxyData::topicKind() const;

%include "fastdds/rtps/builtin/data/ReaderProxyData.h"
