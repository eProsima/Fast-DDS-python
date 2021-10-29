%{
#include "fastdds/rtps/attributes/ServerAttributes.h"
%}

// Ignore deprecated methods
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPPublicationsReader;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPSubscriptionsWriter;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPPublicationsWriter;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPSubscriptionsReader;

%include "fastdds/rtps/attributes/ServerAttributes.h"
