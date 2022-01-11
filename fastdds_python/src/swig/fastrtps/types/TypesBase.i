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
#include "fastrtps/types/TypesBase.h"
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(OctetSeq) std::vector<eprosima::fastrtps::rtps::octet>;

// Although explicitly deleted, SWIG still tries to create this method
%ignore eprosima::fastrtps::types::ReturnCode_t::operator bool;

// Ignore overloaded constructors
%ignore eprosima::fastrtps::types::MemberFlag::MemberFlag(MemberFlag &&);
%ignore eprosima::fastrtps::types::TypeFlag::TypeFlag(TypeFlag &&);

%include "fastrtps/types/TypesBase.h"
