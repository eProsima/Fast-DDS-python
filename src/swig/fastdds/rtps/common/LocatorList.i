%{
#include "fastdds/rtps/common/LocatorList.hpp"
%}

// Ignore deprecated methods
%ignore eprosima::fastdds::rtps::LocatorList::contains;

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastdds::rtps::LocatorList::LocatorList(LocatorList &&);

// For some reason, these need to be explicitly ignored, the global ignore is not enough
%ignore eprosima::fastdds::rtps::operator<<(std::ostream& output,const LocatorList& locList);
%ignore eprosima::fastdds::rtps::operator>>(std::istream& output,LocatorList& locList);

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(Locator_vector) std::vector<eprosima::fastdds::rtps::Locator>;

%include "fastdds/rtps/common/LocatorList.hpp"
