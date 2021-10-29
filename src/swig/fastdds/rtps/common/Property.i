%{
#include "fastdds/rtps/common/Property.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::Property::Property(Property &&);
%ignore eprosima::fastrtps::rtps::Property::propagate() const;

%include "fastdds/rtps/common/Property.h"
