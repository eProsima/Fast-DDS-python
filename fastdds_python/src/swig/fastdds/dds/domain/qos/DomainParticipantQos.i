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
#include "fastdds/dds/domain/qos/DomainParticipantQos.hpp"
%}


%template(FlowControllerDescriptorList) std::vector<std::shared_ptr<eprosima::fastdds::rtps::FlowControllerDescriptor>>;

%extend eprosima::fastdds::dds::DomainParticipantQos {

    /**
     * Getter for the Participant name
     *
     * @return name
     */
    const std::string name() const
    {
        return self->name().to_string();
    }

    /**
     * Setter for the Participant name
     *
     * @param value New name to be set.
     */
    void name(
            const std::string& value)
    {
        self->name(value);
    }
};

%ignore eprosima::fastdds::dds::DomainParticipantQos::name;

%include "fastdds/dds/domain/qos/DomainParticipantQos.hpp"
