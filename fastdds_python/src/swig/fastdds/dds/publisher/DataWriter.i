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


// Ignore unimplemented method (the wrapper will try to use it)
%ignore eprosima::fastdds::dds::DataWriter::dispose_w_timestamp;
%ignore eprosima::fastdds::dds::DataWriter::write_w_timestamp(void*, const InstanceHandle_t&,
            const fastrtps::rtps::Time_t&);

// Template for std::vector<DataWriter*>
%template(DataWriterVector) std::vector<eprosima::fastdds::dds::DataWriter*>;

%include "fastdds/dds/publisher/DataWriter.hpp"
