%{
#include "fastdds/rtps/attributes/RTPSParticipantAttributes.h"
%}

// Ignore deprecated methods
%ignore eprosima::fastrtps::rtps::DiscoverySettings::getStaticEndpointXMLFilename;
%ignore eprosima::fastrtps::rtps::DiscoverySettings::setStaticEndpointXMLFilename;

// This attribute is declared with a private alias and fails during compilation of the wrapper
// Ignore it and kind of substitute it by a getter/setter API
%ignore eprosima::fastrtps::rtps::RTPSParticipantAttributes::flow_controllers;

%include "fastdds/rtps/attributes/RTPSParticipantAttributes.h"

%extend eprosima::fastrtps::rtps::RTPSParticipantAttributes {
    std::vector<std::shared_ptr<eprosima::fastdds::rtps::FlowControllerDescriptor>>& get_flow_controllers()
    {
        return $self->flow_controllers;
    }

    void set_flow_controllers(const std::vector<std::shared_ptr<eprosima::fastdds::rtps::FlowControllerDescriptor>>& fc)
    {
        $self->flow_controllers = fc;
    }
}

