%{
#include "fastdds/rtps/common/Token.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::DataHolder::DataHolder(DataHolder &&);
%ignore eprosima::fastrtps::rtps::DataHolderHelper::DataHolderHelper(DataHolderHelper &&);
%ignore eprosima::fastrtps::rtps::DataHolderHelper::find_property_value(const DataHolder& data_holder, const std::string& name);
%ignore eprosima::fastrtps::rtps::DataHolderHelper::find_property(const DataHolder& data_holder, const std::string& name);
%ignore eprosima::fastrtps::rtps::DataHolderHelper::find_binary_property_value(const DataHolder& data_holder, const std::string& name);
%ignore eprosima::fastrtps::rtps::DataHolderHelper::find_binary_property(const DataHolder& data_holder, const std::string& name);

%include "fastdds/rtps/common/Token.h"
