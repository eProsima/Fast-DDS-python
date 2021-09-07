%{
#include "fastdds/rtps/common/EntityId_t.hpp"
%}

// Overloaded constructor ignored
%ignore eprosima::fastrtps::rtps::EntityId_t::EntityId_t(EntityId_t &&);

//Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator==(const EntityId_t&, const EntityId_t&);
%ignore eprosima::fastrtps::rtps::operator==(EntityId_t&, const uint32_t);
%ignore eprosima::fastrtps::rtps::operator!=(const EntityId_t&, const EntityId_t&);
%ignore eprosima::fastrtps::rtps::operator<<(std::ostream&, const EntityId_t&);
%ignore eprosima::fastrtps::rtps::operator>>(std::ostream&, const EntityId_t&);

%include "fastdds/rtps/common/EntityId_t.hpp"
