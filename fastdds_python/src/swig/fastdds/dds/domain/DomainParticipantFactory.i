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
#include "fastdds/dds/domain/DomainParticipantFactory.hpp"
%}

/*
%extend eprosima::fastdds::dds::DomainParticipantFactory
{
}
*/
%extend eprosima::fastdds::dds::DomainParticipantFactory
{
    DomainParticipant* create_participant(
            DomainId_t domain_id,
            const DomainParticipantQos& qos,
            DomainParticipantListener* listener = nullptr,
            const StatusMask& mask = eprosima::fastdds::dds::StatusMask::all())
    {
        if (nullptr != listener)
        {
            Swig::Director* director = SWIG_DIRECTOR_CAST(listener);

            if (nullptr != director)
            {
                SWIG_PYTHON_THREAD_BEGIN_BLOCK;
                Py_INCREF(director->swig_get_self());
                SWIG_PYTHON_THREAD_END_BLOCK;
            }
        }

        return self->create_participant(domain_id, qos, listener, mask);
    }

    ReturnCode_t delete_participant(
            DomainParticipant* part)
    {
        eprosima::fastdds::dds::DomainParticipantListener* listener =
            const_cast<eprosima::fastdds::dds::DomainParticipantListener*>(part->get_listener());
        eprosima::fastrtps::types::ReturnCode_t ret = self->delete_participant(part);

        if (nullptr != listener)
        {
            Swig::Director* director = SWIG_DIRECTOR_CAST(listener);

            if (nullptr != director)
            {
                SWIG_PYTHON_THREAD_BEGIN_BLOCK;
                Py_DECREF(director->swig_get_self());
                SWIG_PYTHON_THREAD_END_BLOCK;
            }
        }

        return ret;
    }
}

%ignore eprosima::fastdds::dds::DomainParticipantFactory::create_participant;
%ignore eprosima::fastdds::dds::DomainParticipantFactory::delete_participant;

%include "fastdds/dds/domain/DomainParticipantFactory.hpp"
