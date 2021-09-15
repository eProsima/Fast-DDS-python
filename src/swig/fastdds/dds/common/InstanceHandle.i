%{
#include "fastdds/dds/common/InstanceHandle.hpp"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastdds::dds::InstanceHandle_t::operator const GUID_t&;

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastdds::dds::operator<<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastdds::dds::operator>>(std::ostream&, const InstanceHandle_t&);

%include "fastdds/dds/common/InstanceHandle.hpp"
