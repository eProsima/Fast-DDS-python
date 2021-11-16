%{
#include "fastdds/rtps/common/GuidPrefix_t.hpp"

// Define a hash method in global scope for GuidPrefix_t types
// This is necessary if we want other classes to hash an internal GuidPrefix_t
long hash(const eprosima::fastrtps::rtps::GuidPrefix_t& prefix)
{
    long ret = 0;
    for (unsigned int i = 0; i < eprosima::fastrtps::rtps::GuidPrefix_t::size; ++i)
    {
        ret = (ret * 31) ^ prefix.value[i];
    }
    return ret;
}
%}

%include "fastdds/rtps/common/GuidPrefix_t.hpp"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::GuidPrefix_t {
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

