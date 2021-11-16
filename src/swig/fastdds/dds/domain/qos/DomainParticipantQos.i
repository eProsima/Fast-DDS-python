%{
#include "fastdds/dds/domain/qos/DomainParticipantQos.hpp"
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(FlowControllerDescriptorShrPtr) std::shared_ptr<eprosima::fastdds::rtps::FlowControllerDescriptor>;
%template(FlowControllerDescriptor_vector) std::vector<std::shared_ptr<eprosima::fastdds::rtps::FlowControllerDescriptor>>;

%include "fastdds/dds/domain/qos/DomainParticipantQos.hpp"

