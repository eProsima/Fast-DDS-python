%{
#include "fastdds/dds/topic/TypeSupport.hpp"
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(TopicDataTypeShrPtr) std::shared_ptr<eprosima::fastdds::dds::TopicDataType>;

// Ignore overloaded method that has no application in python
// Otherwise it will issue a warning
%ignore eprosima::fastdds::dds::TypeSupport::TypeSupport(TypeSupport &&);

%include "fastdds/dds/topic/TypeSupport.hpp"
