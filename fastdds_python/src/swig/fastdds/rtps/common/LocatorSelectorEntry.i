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
#include "fastdds/rtps/common/LocatorSelectorEntry.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

// Need to create a custom name for the flattened classes
// since other classes also define the same inner class
%rename (LocatorSelectorEntry_EntryState) eprosima::fastdds::rtps::LocatorSelectorEntry::EntryState;

%include "fastdds/rtps/common/LocatorSelectorEntry.hpp"

// Deactivate class flattening
%feature("flatnested", "0");
