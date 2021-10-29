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
#include "fastdds/rtps/attributes/ServerAttributes.h"
%}

// Ignore deprecated methods
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPPublicationsReader;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPSubscriptionsWriter;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPPublicationsWriter;
%ignore eprosima::fastdds::rtps::RemoteServerAttributes::GetEDPSubscriptionsReader;

%include "fastdds/rtps/attributes/ServerAttributes.h"
