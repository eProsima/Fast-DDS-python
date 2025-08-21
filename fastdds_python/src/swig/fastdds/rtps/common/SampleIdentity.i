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
#include "fastdds/rtps/common/SampleIdentity.hpp"
%}

// Ignore overloaded constructor and methods that have no effect on target language
//%ignore eprosima::fastdds::rtps::SampleIdentity::SampleIdentity(SampleIdentity &&);
%ignore eprosima::fastdds::rtps::SampleIdentity::writer_guid(GUID_t &&);
%ignore eprosima::fastdds::rtps::SampleIdentity::writer_guid() const;
%ignore eprosima::fastdds::rtps::SampleIdentity::sequence_number(SequenceNumber_t &&);
%ignore eprosima::fastdds::rtps::SampleIdentity::sequence_number(SequenceNumber_t) const;

// Ignore private methods that cannot be wrapped
%ignore operator >>(std::istream& input, SampleIdentity& sid);
%ignore operator <<(std::ostream& output, const SampleIdentity& sid);

%include "fastdds/rtps/common/SampleIdentity.hpp"

// Copy constructor
%extend eprosima::fastdds::rtps::SampleIdentity {

    SampleIdentity(const eprosima::fastdds::rtps::SampleIdentity& sample_identity_)
    {
        return new eprosima::fastdds::rtps::SampleIdentity(sample_identity_);
    }
}