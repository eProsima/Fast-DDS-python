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
#include "fastdds/dds/subscriber/DataReader.hpp"
%}

// Template for std::vector<DataReader*>
%template(DataReaderVector) std::vector<eprosima::fastdds::dds::DataReader*>;
%template(SampleInfoSeq) eprosima::fastdds::dds::LoanableSequence<eprosima::fastdds::dds::SampleInfo>;
%extend eprosima::fastdds::dds::LoanableSequence<eprosima::fastdds::dds::SampleInfo>
{
    size_t __len__() const
    {
        return self->length();
    }

    const eprosima::fastdds::dds::SampleInfo& __getitem__(size_t i) const
    {
        return (*self)[i];
    }
}

%include "fastdds/dds/subscriber/DataReader.hpp"
