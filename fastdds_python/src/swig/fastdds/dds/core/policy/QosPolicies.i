// This class contains a 'const char*' member that may leak on destruction
// However, converting it to a 'char*' does not
// SWIG is very special)
%typemap(out) char const *flow_controller_name = char *;
%typemap(memberin) char const *flow_controller_name = char *;

%{
#include "fastdds/dds/core/policy/QosPolicies.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(OctetResourceLimitedVector) eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>;

// The class PartitionQosPolicy::const_iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastdds::dds::PartitionQosPolicy::const_iterator;

// Once flattened, these give very unusual errors
%ignore eprosima::fastdds::dds::PartitionQosPolicy::const_iterator::operator->;

// Need to create a custom name for the flattened iterator
// since other classes also define the same inner class
%rename (PartitionQosPolicy_const_iterator) eprosima::fastdds::dds::PartitionQosPolicy::const_iterator;

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastdds::dds::TypeIdV1::TypeIdV1(TypeIdV1 &&);
%ignore eprosima::fastdds::dds::TypeObjectV1::TypeObjectV1(TypeObjectV1 &&);
%ignore eprosima::fastdds::dds::xtypes::TypeInformation::TypeInformation(TypeInformation &&);

%include "fastdds/dds/core/policy/QosPolicies.hpp"

// Deactivate class flattening
%feature("flatnested", "0");

// Undo the mapping for future classes
%typemap(out) char const *flow_controller_name;
%typemap(memberin) char const *flow_controller_name;
