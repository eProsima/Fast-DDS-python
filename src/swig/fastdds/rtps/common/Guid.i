%{
#include "fastdds/rtps/common/Guid.h"

// Define a hash method in global scope for GUID_t types
// This is necessary if we want other classes to hash an internal GUID_t
long hash(const eprosima::fastrtps::rtps::GUID_t& guid)
{
    return (hash(guid.guidPrefix) * 31) ^ hash(guid.entityId);
}
%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_instance_handle) eprosima::fastrtps::rtps::GUID_t::operator const InstanceHandle_t&;

// Ignore the global comparison operators and make them class-internal
%ignore eprosima::fastrtps::operator==(const GUID_t&, const GUID_t&);
%ignore eprosima::fastrtps::operator!=(const GUID_t&, const GUID_t&);
%ignore eprosima::fastrtps::operator<(const GUID_t&, const GUID_t&);

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

    std::string __str__() const
    {
        std::ostringstream out;
        out << *$self;
        return out.str();
    }

    // Define the hash method using the global one
    long __hash__() const
    {
        return hash(*$self);
    }
}
