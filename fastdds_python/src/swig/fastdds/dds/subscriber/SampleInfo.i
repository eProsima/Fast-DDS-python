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
#include "fastdds/dds/subscriber/SampleInfo.hpp"
%}

%ignore eprosima::fastdds::dds::READ;
%ignore eprosima::fastdds::dds::NOT_READ;
%ignore eprosima::fastdds::dds::NEW;
%ignore eprosima::fastdds::dds::NOT_NEW;
%ignore eprosima::fastdds::dds::ALIVE;
%ignore eprosima::fastdds::dds::NOT_ALIVE_DISPOSED;
%ignore eprosima::fastdds::dds::NOT_ALIVE_NO_WRITERS;

%include "fastdds/dds/subscriber/SampleInfo.hpp"
