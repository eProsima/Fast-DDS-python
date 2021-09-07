%{
#include "fastdds/rtps/common/Guid.h"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_instance_handle) eprosima::fastrtps::rtps::GUID_t::operator const InstanceHandle_t&;

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator==(const GUID_t&, const GUID_t&);
%ignore eprosima::fastrtps::rtps::operator!=(const GUID_t&, const GUID_t&);
%ignore eprosima::fastrtps::rtps::operator<(const GUID_t&, const GUID_t&);
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const GUID_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const GUID_t&);

%include "fastdds/rtps/common/Guid.h"
