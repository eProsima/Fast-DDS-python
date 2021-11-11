%{
#include "fastdds/rtps/common/LocatorSelector.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// The class LocatorSelector does not have default constructor
// This tells SWIG it must wrap the constructor or the compilation will fail
%feature("valuewrapper") eprosima::fastrtps::rtps::LocatorSelector;

// The class LocatorSelector::iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastrtps::rtps::LocatorSelector::iterator;

// Once flattened, these give very unusual errors
%ignore eprosima::fastrtps::rtps::LocatorSelector::iterator::operator->;

// Need to create a custom name for the flattened iterator
// since other classes also define the same inner class
%rename (LocatorSelector_iterator) eprosima::fastrtps::rtps::LocatorSelector::iterator;

%include "fastdds/rtps/common/LocatorSelector.hpp"

// Deactivate class flattening
%feature("flatnested", "0");
