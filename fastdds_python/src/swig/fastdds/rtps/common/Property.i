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
#include "fastdds/rtps/common/Property.h"
%}

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastrtps::rtps::Property::Property(Property &&);
%ignore eprosima::fastrtps::rtps::Property::propagate();
%template(PropertySeq) std::vector<eprosima::fastrtps::rtps::Property>;

%extend eprosima::fastrtps::rtps::Property {

    /**
     * Getter for the Property name
     *
     * @return name
     */
    const std::string name() const
    {
        return self->name();
    }

    /**
     * Setter for the Property name
     *
     * @param value New name to be set.
     */
    void name(
            const std::string& value)
    {
        self->name(value);
    }

    /**
     * Getter for the Property value
     *
     * @return value
     */
    const std::string value() const
    {
        return self->value();
    }

    /**
     * Setter for the Property value
     *
     * @param value New value to be set.
     */
    void value(
            const std::string& value)
    {
        self->value(value);
    }
};

%ignore eprosima::fastrtps::rtps::Property::name;
%ignore eprosima::fastrtps::rtps::Property::value;

%include "fastdds/rtps/common/Property.h"
