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
#include "fastdds/dds/core/policy/ParameterTypes.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// Ignore unimplemented method (the wrapper will try to use it)
%ignore eprosima::fastdds::dds::ParameterSampleIdentity_t::addToCDRMessage;
%ignore eprosima::fastdds::dds::ParameterSampleIdentity_t::readFromCDRMessage;
%ignore eprosima::fastdds::dds::ParameterOriginalWriterInfo_t::addToCDRMessage;
%ignore eprosima::fastdds::dds::ParameterOriginalWriterInfo_t::readFromCDRMessage;

// The class ParameterPropertyList_t::iterator does not have default constructor
// This tells SWIG it must wrap the constructors or the compilation will fail
%feature("valuewrapper") eprosima::fastdds::dds::ParameterPropertyList_t::iterator;
%feature("valuewrapper") eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator;

// Once flattened, these give very unusual errors
%ignore eprosima::fastdds::dds::ParameterPropertyList_t::iterator::operator->;
%ignore eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator::operator->;

// Need to create a custom name for the flattened iterator
// since other classes also define the same inner class
%rename (ParameterPropertyList_t_iterator) eprosima::fastdds::dds::ParameterPropertyList_t::iterator;
%rename (ParameterPropertyList_t_const_iterator) eprosima::fastdds::dds::ParameterPropertyList_t::const_iterator;

%include "fastdds/dds/core/policy/ParameterTypes.hpp"

// Deactivate class flattening
%feature("flatnested", "0");
