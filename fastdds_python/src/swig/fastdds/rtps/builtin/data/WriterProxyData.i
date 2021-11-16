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
#include "fastdds/rtps/builtin/data/WriterProxyData.h"
%}

namespace eprosima {
namespace fastrtps {

using WriterQos = eprosima::fastdds::dds::WriterQos;

} // namespace fastrtps
} // namespace eprosima

// Ignore overloads that meake no sense on Python and cause warnings on compilation
%ignore eprosima::fastrtps::rtps::WriterProxyData::guid(GUID_t&&);
%ignore eprosima::fastrtps::rtps::WriterProxyData::guid() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::persistence_guid(GUID_t&&);
%ignore eprosima::fastrtps::rtps::WriterProxyData::persistence_guid() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::key(InstanceHandle_t&&);
%ignore eprosima::fastrtps::rtps::WriterProxyData::key() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::RTPSParticipantKey(InstanceHandle_t&&);
%ignore eprosima::fastrtps::rtps::WriterProxyData::RTPSParticipantKey() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::typeName(string_255&&);
%ignore eprosima::fastrtps::rtps::WriterProxyData::typeName() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::topicName(string_255&&);
%ignore eprosima::fastrtps::rtps::WriterProxyData::topicName() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::userDefinedId() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::topicKind() const;
%ignore eprosima::fastrtps::rtps::WriterProxyData::typeMaxSerialized() const;

%include "fastdds/rtps/builtin/data/WriterProxyData.h"
