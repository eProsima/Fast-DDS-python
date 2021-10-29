// Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

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
