%{
#include "fastdds/rtps/common/EntityId_t.hpp"
%}

// Overloaded constructor ignored
%ignore eprosima::fastrtps::rtps::EntityId_t::EntityId_t(EntityId_t &&);

// Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const EntityId_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const EntityId_t&);

// Declare hash so that we do not get a warning
// This will make an empty class on the target, but the user should not need this anyway.
namespace std {
    template <typename T>
    struct hash;
}

%include "fastdds/rtps/common/EntityId_t.hpp"
