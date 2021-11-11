%{
#include "fastdds/dds/common/InstanceHandle.hpp"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastdds::dds::InstanceHandle_t::operator const GUID_t&;

%include "fastdds/dds/common/InstanceHandle.hpp"
