%{
#include "fastdds/rtps/common/EntityId_t.hpp"

// Define a hash method in global scope for EntityId_t types
// This is necessary if we want other classes to hash an internal EntityId_t
long hash(const eprosima::fastrtps::rtps::EntityId_t& id)
{
    long ret = 0;
    for (unsigned int i = 0; i < eprosima::fastrtps::rtps::EntityId_t::size; ++i)
    {
        ret = (ret * 31) ^ id.value[i];
    }
    return ret;
}
%}

// Overloaded constructor ignored
%ignore eprosima::fastrtps::rtps::EntityId_t::EntityId_t(EntityId_t &&);

// Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator==;
%ignore eprosima::fastrtps::rtps::operator!=;

// Declare hash so that we do not get a warning
// This will make an empty class on the target, but the user should not need this anyway.
namespace std {
    template <typename T>
    struct hash;
}

%include "fastdds/rtps/common/EntityId_t.hpp"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::EntityId_t {
    bool operator==(const eprosima::fastrtps::rtps::EntityId_t& other) const
    {
        return *$self == other;
    }

    bool operator==(uint32_t other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::EntityId_t& other) const
    {
        return *$self != other;
    }

    // Define the hash method using the global one
    std::string __str__() const
    {
        std::ostringstream out;
        out << *$self;
        return out.str();
    }

    long __hash__() const
    {
        return hash(*$self);
    }
}
