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
%typemap(out) char const *flow_controller_name = char *;
%typemap(memberin) char const *flow_controller_name = char *;

%{
#include "fastdds/rtps/attributes/WriterAttributes.h"
%}

%include "fastdds/rtps/attributes/WriterAttributes.h"

// Undo the mapping for future classes
%typemap(out) char const *flow_controller_name;
%typemap(memberin) char const *flow_controller_name;
