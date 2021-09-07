%{
#include "fastdds/rtps/common/InstanceHandle.h"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator==(const InstanceHandle_t&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator!=(const InstanceHandle_t&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator<(const InstanceHandle_t&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const InstanceHandle_t&);

%include "fastdds/rtps/common/InstanceHandle.h"
