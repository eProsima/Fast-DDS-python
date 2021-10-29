%{
#include "fastdds/rtps/common/LocatorSelector.hpp"
%}

// The class LocatorSelector does not have default constructor
// This tells SWIG it must wrap the constructor or the compilation will fail
%feature("valuewrapper") eprosima::fastrtps::rtps::LocatorSelector;

// The class LocatorSelector::iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastrtps::rtps::LocatorSelector::iterator;


%include "fastdds/rtps/common/LocatorSelector.hpp"
