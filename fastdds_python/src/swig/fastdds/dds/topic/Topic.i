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
#include "fastdds/dds/topic/Topic.hpp"
%}

// Ignore get_inconsistent_topic_status which is not exported
%ignore eprosima::fastdds::dds::Topic::get_inconsistent_topic_status;
%ignore eprosima::fastdds::dds::Topic::Topic;
%ignore eprosima::fastdds::dds::Topic::~Topic;

%include "fastdds/dds/topic/Topic.hpp"
