%{
#include "fastdds/rtps/common/BinaryProperty.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::BinaryProperty::BinaryProperty(BinaryProperty &&);
%ignore eprosima::fastrtps::rtps::BinaryProperty::name(std::string &&);
%ignore eprosima::fastrtps::rtps::BinaryProperty::value(std::vector<uint8_t> &&);
%ignore eprosima::fastrtps::rtps::BinaryProperty::propagate() const;

%include "fastdds/rtps/common/BinaryProperty.h"
