%{
#include "fastdds/rtps/common/Guid.h"
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_instance_handle) eprosima::fastrtps::rtps::GUID_t::operator const InstanceHandle_t&;

// Ignore the global comparison operators and make them class-internal
%ignore eprosima::fastrtps::operator==(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator!=(const Time_t&, const Time_t&);
%ignore eprosima::fastrtps::operator<(const Time_t&, const Time_t&);

%include "fastdds/rtps/common/Guid.h"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::GUID_t {
    bool operator==(const eprosima::fastrtps::rtps::GUID_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::GUID_t& other) const
    {
        return *$self != other;
    }

    bool operator<(const eprosima::fastrtps::rtps::GUID_t& other) const
    {
        return *$self < other;
    }
}

