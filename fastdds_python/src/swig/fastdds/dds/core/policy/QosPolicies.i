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

// This class contains a 'const char*' member that may leak on destruction
// However, converting it to a 'char*' does not
// SWIG is very special)
%typemap(out) char const *flow_controller_name = char *;
%typemap(memberin) char const *flow_controller_name = char *;

%{
#include "fastdds/dds/core/policy/QosPolicies.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(octet_ResourceLimitedVector) eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>;
%template(TransportDescriptorInterfaceShrPtr) std::shared_ptr<eprosima::fastdds::rtps::TransportDescriptorInterface>;
%template(TransportDescriptorInterface_vector) std::vector<std::shared_ptr<eprosima::fastdds::rtps::TransportDescriptorInterface>>;
// The 'enum' here is very important, or SWIG will create a faulty wrapper
//    * Enums are mapped as integer constants
//    * The template expects a class type
//    * Trying to push a mapped enum value (integer) will result on an error because it is not the expected type
%template(DataRepresentationId_t_vector) std::vector<enum eprosima::fastdds::dds::DataRepresentationId>;

// The class PartitionQosPolicy::const_iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastdds::dds::PartitionQosPolicy::const_iterator;

// Once flattened, these give very unusual errors
%ignore eprosima::fastdds::dds::PartitionQosPolicy::const_iterator::operator->;

// Need to create a custom name for the flattened iterator
// since other classes also define the same inner class
%rename (PartitionQosPolicy_const_iterator) eprosima::fastdds::dds::PartitionQosPolicy::const_iterator;

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastdds::dds::TypeIdV1::TypeIdV1(TypeIdV1 &&);
%ignore eprosima::fastdds::dds::TypeObjectV1::TypeObjectV1(TypeObjectV1 &&);
%ignore eprosima::fastdds::dds::xtypes::TypeInformation::TypeInformation(TypeInformation &&);

// Some classes still use the old namespaces
namespace eprosima {
namespace fastrtps {

using QosPolicy = fastdds::dds::QosPolicy;
using DurabilityQosPolicyKind = fastdds::dds::DurabilityQosPolicyKind;
using DurabilityQosPolicy = fastdds::dds::DurabilityQosPolicy;
using DeadlineQosPolicy = fastdds::dds::DeadlineQosPolicy;
using LatencyBudgetQosPolicy  = fastdds::dds::LatencyBudgetQosPolicy;
using LivelinessQosPolicyKind = fastdds::dds::LivelinessQosPolicyKind;
using LivelinessQosPolicy = fastdds::dds::LivelinessQosPolicy;
using ReliabilityQosPolicyKind = fastdds::dds::ReliabilityQosPolicyKind;
using ReliabilityQosPolicy = fastdds::dds::ReliabilityQosPolicy;
using OwnershipQosPolicyKind =  fastdds::dds::OwnershipQosPolicyKind;
using OwnershipQosPolicy = fastdds::dds::OwnershipQosPolicy;
using DestinationOrderQosPolicyKind = fastdds::dds::DestinationOrderQosPolicyKind;
using DestinationOrderQosPolicy = fastdds::dds::DestinationOrderQosPolicy;
using TimeBasedFilterQosPolicy = fastdds::dds::TimeBasedFilterQosPolicy;
using PresentationQosPolicyAccessScopeKind = fastdds::dds::PresentationQosPolicyAccessScopeKind;
using PresentationQosPolicy = fastdds::dds::PresentationQosPolicy;
using PartitionQosPolicy = fastdds::dds::PartitionQosPolicy;
using UserDataQosPolicy = fastdds::dds::UserDataQosPolicy;
using TopicDataQosPolicy = fastdds::dds::TopicDataQosPolicy;
using GroupDataQosPolicy = fastdds::dds::GroupDataQosPolicy;
using HistoryQosPolicyKind = fastdds::dds::HistoryQosPolicyKind;
using HistoryQosPolicy = fastdds::dds::HistoryQosPolicy;
using ResourceLimitsQosPolicy = fastdds::dds::ResourceLimitsQosPolicy;
using DurabilityServiceQosPolicy = fastdds::dds::DurabilityServiceQosPolicy;
using LifespanQosPolicy = fastdds::dds::LifespanQosPolicy;
using OwnershipStrengthQosPolicy = fastdds::dds::OwnershipStrengthQosPolicy;
using TransportPriorityQosPolicy = fastdds::dds::TransportPriorityQosPolicy;
using PublishModeQosPolicyKind = fastdds::dds::PublishModeQosPolicyKind;
using PublishModeQosPolicy = fastdds::dds::PublishModeQosPolicy;
using DataRepresentationId = fastdds::dds::DataRepresentationId;
using DataRepresentationQosPolicy = fastdds::dds::DataRepresentationQosPolicy;
using TypeConsistencyKind = fastdds::dds::TypeConsistencyKind;
using TypeConsistencyEnforcementQosPolicy = fastdds::dds::TypeConsistencyEnforcementQosPolicy;
using DisablePositiveACKsQosPolicy = fastdds::dds::DisablePositiveACKsQosPolicy;
using DataSharingQosPolicy = fastdds::dds::DataSharingQosPolicy;
using DataSharingKind = fastdds::dds::DataSharingKind;
using TypeIdV1 = fastdds::dds::TypeIdV1;
using TypeObjectV1 = fastdds::dds::TypeObjectV1;

namespace xtypes {
using TypeInformation = fastdds::dds::xtypes::TypeInformation;
} //namespace xtypes

} // namespace fastrtps
} // namespace eprosima


%include "fastdds/dds/core/policy/QosPolicies.hpp"

// Deactivate class flattening
%feature("flatnested", "0");

// Undo the mapping for future classes
%typemap(out) char const *flow_controller_name;
%typemap(memberin) char const *flow_controller_name;
