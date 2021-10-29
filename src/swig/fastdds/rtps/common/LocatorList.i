%{
#include "fastdds/rtps/common/LocatorList.hpp"
%}

// Ignore deprecated methods
%ignore eprosima::fastdds::rtps::LocatorList::contains;

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastdds::rtps::LocatorList::LocatorList(LocatorList &&);

%include "fastdds/rtps/common/LocatorList.hpp"
