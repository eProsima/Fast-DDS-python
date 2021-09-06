%{
#include "fastdds/dds/core/policy/QosPolicies.hpp"
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(OctetResourceLimitedVector) eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>;

// The class PartitionQosPolicy::const_iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastdds::dds::PartitionQosPolicy::const_iterator;

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastdds::dds::TypeIdV1::TypeIdV1(TypeIdV1 &&);
%ignore eprosima::fastdds::dds::TypeObjectV1::TypeObjectV1(TypeObjectV1 &&);
%ignore eprosima::fastdds::dds::xtypes::TypeInformation::TypeInformation(TypeInformation &&);

%include "fastdds/dds/core/policy/QosPolicies.hpp"
