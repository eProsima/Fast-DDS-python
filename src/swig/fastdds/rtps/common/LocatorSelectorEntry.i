%{
#include "fastdds/rtps/common/LocatorSelectorEntry.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// Need to create a custom name for the flattened classes
// since other classes also define the same inner class
%rename (LocatorSelectorEntry_EntryState) eprosima::fastrtps::rtps::LocatorSelectorEntry::EntryState;

%include "fastdds/rtps/common/LocatorSelectorEntry.hpp"

// Deactivate class flattening
%feature("flatnested", "0");
