%{
#include "fastdds/dds/core/policy/ParameterTypes.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// Ignore unimplemented method (the wrapper will try to use it)
%ignore eprosima::fastdds::dds::ParameterSampleIdentity_t::addToCDRMessage;
%ignore eprosima::fastdds::dds::ParameterSampleIdentity_t::readFromCDRMessage;

// The class ParameterPropertyList_t::iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastdds::dds::ParameterPropertyList_t::iterator;
%feature("valuewrapper") eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator;

// Once flattened, these give very unusual errors
%ignore eprosima::fastdds::dds::ParameterPropertyList_t::iterator::operator->;
%ignore eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator::operator->;

// Need to create a custom name for the flattened iterator
// since other classes also define the same inner class
%rename (ParameterPropertyList_t_iterator) eprosima::fastdds::dds::ParameterPropertyList_t::iterator;
%rename (ParameterPropertyList_t_const_iterator) eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator;

%include "fastdds/dds/core/policy/ParameterTypes.hpp"

// Deactivate class flattening
%feature("flatnested", "0");
