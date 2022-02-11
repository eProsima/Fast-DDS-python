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
#include "fastdds/rtps/flowcontrol/FlowControllerDescriptor.hpp"
%}

// Avoid memory leak because a const char* in our API.
%nodefaultctor eprosima::fastdds::rtps::FlowControllerDescriptor;
%{
    struct _FlowControllerDescriptor : public eprosima::fastdds::rtps::FlowControllerDescriptor
    {
        std::string flow_name;
    };
%}
%extend eprosima::fastdds::rtps::FlowControllerDescriptor
{
    FlowControllerDescriptor()
    {
        return new _FlowControllerDescriptor();
    }

    std::string name;
}
%ignore eprosima::fastdds::rtps::FlowControllerDescriptor::name;

// In DomainParticipantQos is used the std::shared_ptr<FlowControllerDescriptor>
// instead of this structure directly.
%shared_ptr(eprosima::fastdds::rtps::FlowControllerDescriptor);

%include "fastdds/rtps/flowcontrol/FlowControllerDescriptor.hpp"

// Avoid memory leak because a const char* in our API.
%{
    void eprosima_fastdds_rtps_FlowControllerDescriptor_name_set(
            eprosima::fastdds::rtps::FlowControllerDescriptor* descriptor,
            const std::string& name)
    {
        //TODO (richiware) Should launch exception
        _FlowControllerDescriptor* desc = static_cast<_FlowControllerDescriptor*>(descriptor);
        desc->flow_name = name;
        desc->name = desc->flow_name.c_str();
    }

    std::string& eprosima_fastdds_rtps_FlowControllerDescriptor_name_get(
                eprosima::fastdds::rtps::FlowControllerDescriptor* descriptor)
    {
        //TODO (richiware) Should launch exception
        _FlowControllerDescriptor* desc = static_cast<_FlowControllerDescriptor*>(descriptor);
        desc->flow_name = desc->name;
        return desc->flow_name;
    }
%}
