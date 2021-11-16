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
