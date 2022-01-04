%{
#include "fastdds/dds/common/InstanceHandle.hpp"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

%ignore eprosima::fastrtps::rtps::InstanceHandleValue_t::operator [] const;
%rename(read_pointer_cast) eprosima::fastrtps::rtps::InstanceHandleValue_t::operator const octet* () const;
%rename(write_pointer_cast) eprosima::fastrtps::rtps::InstanceHandleValue_t::operator octet* ();

%include "fastdds/rtps/common/InstanceHandle.h"

namespace eprosima {
namespace fastdds {
namespace dds {

using InstanceHandle_t = eprosima::fastrtps::rtps::InstanceHandle_t;

} // namespace dds
} // namespace fastdds
} // namespace eprosima

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::InstanceHandle_t {

    bool operator==(const eprosima::fastrtps::rtps::InstanceHandle_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::InstanceHandle_t& other) const
    {
        return *$self != other;
    }

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastdds::dds::operator<<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastdds::dds::operator>>(std::ostream&, const InstanceHandle_t&);

%include "fastdds/dds/common/InstanceHandle.hpp"
