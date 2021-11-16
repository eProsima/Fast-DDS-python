%{
#include "fastdds/rtps/common/InstanceHandle.h"

// Define a hash method in global scope for GuidPrefix_t types
// This is necessary if we want other classes to hash an internal GuidPrefix_t
long hash(const eprosima::fastrtps::rtps::InstanceHandle_t& handle)
{
    long ret = 0;
    for (unsigned int i = 0; i < 16; ++i)
    {
        ret = (ret * 31) ^ handle.value[i];
    }
    return ret;
}

%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

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
