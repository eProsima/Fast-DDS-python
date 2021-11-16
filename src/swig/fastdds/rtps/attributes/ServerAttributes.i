%{
#include "fastdds/rtps/attributes/ServerAttributes.h"
%}

// Ignore deprecated methods
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPPublicationsReader;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPSubscriptionsWriter;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPPublicationsWriter;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPSubscriptionsReader;

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(RemoteServerAttributes_list) std::list<eprosima::fastdds::rtps::RemoteServerAttributes>;

%include "fastdds/rtps/attributes/ServerAttributes.h"
