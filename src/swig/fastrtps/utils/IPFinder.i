%{
#include "fastrtps/utils/IPFinder.h"
%}

// Flatten nested classes
%feature("flatnested", "1");

// Need to create a custom name for the flattened classes
// since other classes also define the same inner class
%rename (IPFinder_IPTYPE) eprosima::fastrtps::rtps::IPFinder::IPTYPE;
%rename (IPFinder_info_IP) eprosima::fastrtps::rtps::IPFinder::info_IP;
%rename (IPFinder_info_MAC) eprosima::fastrtps::rtps::IPFinder::info_MAC;

%include "fastrtps/utils/IPFinder.h"

// Deactivate class flattening
%feature("flatnested", "0");
