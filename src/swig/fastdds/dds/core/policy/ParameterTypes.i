%{
#include "fastdds/dds/core/policy/ParameterTypes.hpp"
%}

// The class ParameterPropertyList_t::iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastdds::dds::ParameterPropertyList_t::iterator;
%feature("valuewrapper") eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator;

// Ignore unimplemented method (the wrapper will try to use it)
%ignore eprosima::fastdds::dds::ParameterSampleIdentity_t::addToCDRMessage;
%ignore eprosima::fastdds::dds::ParameterSampleIdentity_t::readFromCDRMessage;

%include "fastdds/dds/core/policy/ParameterTypes.hpp"
