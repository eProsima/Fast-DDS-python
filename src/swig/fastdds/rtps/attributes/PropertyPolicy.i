%{
#include "fastdds/rtps/attributes/PropertyPolicy.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::PropertyPolicy::PropertyPolicy(PropertyPolicy &&);
%ignore eprosima::fastrtps::rtps::PropertyPolicyHelper::find_property(const PropertyPolicy& property_policy, const std::string& name);

%include "fastdds/rtps/attributes/PropertyPolicy.h"
