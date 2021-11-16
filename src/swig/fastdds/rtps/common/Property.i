%{
#include "fastdds/rtps/common/Property.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::Property::Property(Property &&);
%ignore eprosima::fastrtps::rtps::Property::name(std::string &&);
%ignore eprosima::fastrtps::rtps::Property::value(std::string &&);
%ignore eprosima::fastrtps::rtps::Property::propagate() const;
%ignore eprosima::fastrtps::rtps::Property::name() const;
%ignore eprosima::fastrtps::rtps::Property::value() const;

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(PropertySeq) std::vector<eprosima::fastrtps::rtps::Property>;

%include "fastdds/rtps/common/Property.h"
