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
#include "fastdds/dds/core/condition/Condition.hpp"
#include "fastdds/dds/core/condition/StatusCondition.hpp"
#include "fastdds/dds/core/condition/GuardCondition.hpp"
%}

// Ignore StatusCondition constructor
%ignore eprosima::fastdds::dds::StatusCondition::StatusCondition;

%exception eprosima::fastdds::dds::Condition::to_status_condition()
{
    try
    {
        $action
    }
    catch(std::bad_cast ex)
    {
        SWIG_exception(SWIG_TypeError, "Bad cast of Condition");
    }
}

%exception eprosima::fastdds::dds::Condition::to_guard_condition()
{
    try
    {
        $action
    }
    catch(std::bad_cast ex)
    {
        SWIG_exception(SWIG_TypeError, "Bad cast of Condition");
    }
}

%extend eprosima::fastdds::dds::Condition
{
    std::string __str__()
    {
        if (nullptr != dynamic_cast<eprosima::fastdds::dds::StatusCondition*>(self))
        {
            return "StatusCondition";
        }
        else if (nullptr != dynamic_cast<eprosima::fastdds::dds::GuardCondition*>(self))
        {
            return "GuardCondition";
        }

        return "None";
    }

    eprosima::fastdds::dds::StatusCondition* to_status_condition()
    {
        eprosima::fastdds::dds::StatusCondition* status_cond =
            dynamic_cast<eprosima::fastdds::dds::StatusCondition*>(self);

        if (nullptr == status_cond)
        {
            throw std::bad_cast();
        }

        return status_cond;
    }

    eprosima::fastdds::dds::GuardCondition* to_guard_condition()
    {
        eprosima::fastdds::dds::GuardCondition* guard_cond =
            dynamic_cast<eprosima::fastdds::dds::GuardCondition*>(self);

        if (nullptr == guard_cond)
        {
            throw std::bad_cast();
        }

        return guard_cond;
    }
}

%extend eprosima::fastdds::dds::StatusCondition
{
    std::string __str__()
    {
        return "StatusCondition";
    }

    bool __eq__(
            const eprosima::fastdds::dds::StatusCondition* s1)
    {
        return s1 == self;
    }
}

%extend eprosima::fastdds::dds::GuardCondition
{
    std::string __str__()
    {
        return "GuardCondition";
    }

    bool __eq__(
            const eprosima::fastdds::dds::GuardCondition* s1)
    {
        return s1 == self;
    }
}

// Template for ConditionSeq
%template(ConditionSeq) std::vector<eprosima::fastdds::dds::Condition*>;

%include "fastdds/dds/core/condition/Condition.hpp"
%include "fastdds/dds/core/condition/StatusCondition.hpp"
%include "fastdds/dds/core/condition/GuardCondition.hpp"
