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
#include "fastdds/rtps/common/BinaryProperty.hpp"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%copyctor eprosima::fastdds::rtps::BinaryProperty;
%ignore eprosima::fastdds::rtps::BinaryProperty::name(std::string &&);
%ignore eprosima::fastdds::rtps::BinaryProperty::value(std::vector<uint8_t> &&);
%ignore eprosima::fastdds::rtps::BinaryProperty::propagate() const;
%ignore eprosima::fastdds::rtps::BinaryProperty::name() const;
%ignore eprosima::fastdds::rtps::BinaryProperty::value() const;

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(BinaryPropertySeq) std::vector<eprosima::fastdds::rtps::BinaryProperty>;

%include "fastdds/rtps/common/BinaryProperty.hpp"
