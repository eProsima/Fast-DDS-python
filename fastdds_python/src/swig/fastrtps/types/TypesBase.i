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
#include <sstream>
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(OctetSeq) std::vector<eprosima::fastrtps::rtps::octet>;

// Ignore overloaded constructors
%ignore eprosima::fastrtps::types::MemberFlag::MemberFlag(MemberFlag &&);
%ignore eprosima::fastrtps::types::TypeFlag::TypeFlag(TypeFlag &&);

// Ignore type ancillary within the namespace
%ignore eprosima::fastrtps::types::to_size_t;

%ignore eprosima::fastrtps::types::MemberFlag::serialize;
%ignore eprosima::fastrtps::types::MemberFlag::deserialize;
%ignore eprosima::fastrtps::types::MemberFlag::getCdrSerializedSize;

%ignore eprosima::fastrtps::types::TypeFlag::serialize;
%ignore eprosima::fastrtps::types::TypeFlag::deserialize;
%ignore eprosima::fastrtps::types::TypeFlag::getCdrSerializedSize;

%ignore eprosima::fastrtps::types::operator==;
%ignore eprosima::fastrtps::types::operator!=;

%ignore eprosima::fastrtps::types::RETCODE_OK;
%ignore eprosima::fastrtps::types::RETCODE_ERROR;
%ignore eprosima::fastrtps::types::RETCODE_UNSUPPORTED;
%ignore eprosima::fastrtps::types::RETCODE_BAD_PARAMETER;
%ignore eprosima::fastrtps::types::RETCODE_PRECONDITION_NOT_MET;
%ignore eprosima::fastrtps::types::RETCODE_OUT_OF_RESOURCES;
%ignore eprosima::fastrtps::types::RETCODE_NOT_ENABLED;
%ignore eprosima::fastrtps::types::RETCODE_IMMUTABLE_POLICY;
%ignore eprosima::fastrtps::types::RETCODE_INCONSISTENT_POLICY;
%ignore eprosima::fastrtps::types::RETCODE_ALREADY_DELETED;
%ignore eprosima::fastrtps::types::RETCODE_TIMEOUT;
%ignore eprosima::fastrtps::types::RETCODE_NO_DATA;
%ignore eprosima::fastrtps::types::RETCODE_ILLEGAL_OPERATION;


%include "fastrtps/types/TypesBase.h"
