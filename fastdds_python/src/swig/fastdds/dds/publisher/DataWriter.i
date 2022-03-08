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
#include "fastdds/dds/publisher/DataWriter.hpp"
%}


%ignore eprosima::fastdds::dds::DataWriter::write_w_timestamp(void*, const InstanceHandle_t&,
            const fastrtps::rtps::Time_t&);
%ignore eprosima::fastdds::dds::DataWriter::register_instance_w_timestamp(void*,
            const fastrtps::rtps::Time_t&);
%ignore eprosima::fastdds::dds::DataWriter::unregister_instance_w_timestamp(void*, const InstanceHandle_t&,
            const fastrtps::rtps::Time_t&);
%ignore eprosima::fastdds::dds::DataWriter::get_matched_subscriptions(
            std::vector<InstanceHandle_t*>&) const;

// Tell SWIG to convert parameter size_t* removed in an output parameter
%apply size_t* OUTPUT { size_t* removed }
// Ignore C++ clear_history because we need to overload it in Python.
%extend eprosima::fastdds::dds::DataWriter
{
    // TODO Document with %feature("autodoc")
    eprosima::fastrtps::types::ReturnCode_t clear_history(size_t* removed)
    {
        eprosima::fastrtps::types::ReturnCode_t ret = self->clear_history(removed);
        return ret;
    }
}
%ignore eprosima::fastdds::dds::DataWriter::clear_history(size_t*);

// Template for std::vector<DataWriter*>
%template(DataWriterVector) std::vector<eprosima::fastdds::dds::DataWriter*>;

%include "fastdds/dds/publisher/DataWriter.hpp"

%clear size_t* removed;
