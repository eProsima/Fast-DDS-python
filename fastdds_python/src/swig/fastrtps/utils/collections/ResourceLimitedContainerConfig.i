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
#include "fastrtps/utils/collections/ResourceLimitedContainerConfig.hpp"
%}

// SWIG does not support parsing this default argument:
//    size_t max = (std::numeric_limits<size_t>::max)()
// This issues a parsing error and stops SWIG
// We are forced to reimplement the interface here
// Due to the way SWIG creates the wrapper, the default values can be substituted by any value
// since the wrapper will not use them anywhere,
// they are used only to detect when arguments are optional

namespace eprosima {
namespace fastrtps {

struct ResourceLimitedContainerConfig
{

    ResourceLimitedContainerConfig(
            size_t ini = 0,
            size_t max = 0,
            size_t inc = 1u)
        : initial(ini)
        , maximum(max)
        , increment(inc);
    inline static ResourceLimitedContainerConfig fixed_size_configuration(
            size_t size);

    inline static ResourceLimitedContainerConfig dynamic_allocation_configuration(
            size_t increment = 1u);

};

inline bool operator == (
        const ResourceLimitedContainerConfig& lhs,
        const ResourceLimitedContainerConfig& rhs);

}  // namespace fastrtps
}  // namespace eprosima

//%include "fastrtps/utils/collections/ResourceLimitedContainerConfig.hpp"
