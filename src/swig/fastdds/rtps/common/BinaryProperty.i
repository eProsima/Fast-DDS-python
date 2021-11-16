%{
#include "fastdds/rtps/common/BinaryProperty.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::BinaryProperty::BinaryProperty(BinaryProperty &&);
%ignore eprosima::fastrtps::rtps::BinaryProperty::name(std::string &&);
%ignore eprosima::fastrtps::rtps::BinaryProperty::value(std::vector<uint8_t> &&);
%ignore eprosima::fastrtps::rtps::BinaryProperty::propagate() const;
%ignore eprosima::fastrtps::rtps::BinaryProperty::name() const;
%ignore eprosima::fastrtps::rtps::BinaryProperty::value() const;

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(BinaryPropertySeq) std::vector<eprosima::fastrtps::rtps::BinaryProperty>;

%include "fastdds/rtps/common/BinaryProperty.h"
