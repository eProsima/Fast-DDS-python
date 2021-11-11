%{
#include "fastdds/rtps/common/InstanceHandle.h"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

%include "fastdds/rtps/common/InstanceHandle.h"
