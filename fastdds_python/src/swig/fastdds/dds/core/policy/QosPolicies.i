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
%{
#include "fastdds/dds/core/policy/QosPolicies.hpp"
%}

%ignore eprosima::fastdds::dds::WireProtocolConfigQos::throughput_controller;

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

namespace eprosima {
namespace fastdds {
namespace dds {
    struct ParticipantResourceLimitsQos : public fastrtps::rtps::RTPSParticipantAllocationAttributes {};
    struct PropertyPolicyQos : public fastrtps::rtps::PropertyPolicy {};
}
}
}

%inline %{
class OctetResourceLimitedVectorStopIterator {};
class OctetResourceLimitedVectorIterator {
public:
    OctetResourceLimitedVectorIterator(
            eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>::iterator _cur,
            eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>::iterator _end) : cur(_cur), end(_end) {}
    OctetResourceLimitedVectorIterator* __iter__()
    {
        return this;
    }
    eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>::iterator cur;
    eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>::iterator end;
};
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(OctetResourceLimitedVector) eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet>;

%include "fastdds/dds/core/policy/QosPolicies.hpp"

%include "exception.i"
%exception OctetResourceLimitedVectorIterator::__next__ {
    try
    {
        $action // calls %extend function __next__() below
    }
    catch (OctetResourceLimitedVectorStopIterator)
    {
        PyErr_SetString(PyExc_StopIteration, "End of iterator");
        return NULL;
    }
}

%extend OctetResourceLimitedVectorIterator
{
    eprosima::fastrtps::rtps::octet __next__()
    {
        if ($self->cur != $self->end)
        {
            // dereference the iterator and return reference to the object,
            // after that it increments the iterator
            return *$self->cur++;
        }
        throw OctetResourceLimitedVectorStopIterator();
    }
}

%extend eprosima::fastrtps::ResourceLimitedVector<eprosima::fastrtps::rtps::octet> {
    OctetResourceLimitedVectorIterator __iter__()
    {
        // return a constructed Iterator object
        return OctetResourceLimitedVectorIterator($self->begin(), $self->end());
    }
}
