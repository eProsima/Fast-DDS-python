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
#include "fastdds/dds/topic/TypeSupport.hpp"
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(TopicDataTypeShrPtr) std::shared_ptr<eprosima::fastdds::dds::TopicDataType>;

// Ignore overloaded method that has no application in python
// Otherwise it will issue a warning
%ignore eprosima::fastdds::dds::TypeSupport::TypeSupport(TypeSupport &&);

// This constructor takes ownership of the TopicDataType pointer
// We need SWIG to be aware of it, so we ignore it here and redefine it later
%ignore eprosima::fastdds::dds::TypeSupport::TypeSupport(TopicDataType*);

%ignore eprosima::fastdds::dds::TypeSupport::TypeSupport(DynamicPubSubType);

%include "fastdds/dds/topic/TypeSupport.hpp"

// To make SWIG aware of the loss of the ownership, use the DISOWN typemap
// Do not worry about the heap allocation, SWIG recognizes the method as a constructor
// and successfully deallocates on destruction
%extend eprosima::fastdds::dds::TypeSupport {
    %apply SWIGTYPE *DISOWN { TopicDataType* ptr };
    TypeSupport(TopicDataType* ptr)
    {
        return new eprosima::fastdds::dds::TypeSupport(ptr);
    }

    %apply SWIGTYPE *DISOWN { TopicDataType* ptr };
    void set(TopicDataType* ptr)
    {
        self->reset(ptr);
    }

}
