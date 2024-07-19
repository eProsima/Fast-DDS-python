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

%typemap(in) (eprosima::fastdds::dds::DomainParticipantListener* listener) %{
    $typemap(in, eprosima::fastdds::dds::DomainParticipantListener* DISOWN)
    {
        Swig::Director* director = SWIG_DIRECTOR_CAST($1);

        if (nullptr != director)
        {
            SWIG_PYTHON_THREAD_BEGIN_BLOCK;
            director->swig_incref();
            SWIG_PYTHON_THREAD_END_BLOCK;
        }
    }
    %}

%extend eprosima::fastdds::dds::DomainParticipantFactory
{
    /**
     * Remove a Participant and all associated publishers and subscribers.
     *
     * @param part Pointer to the participant.
     * @return RETCODE_PRECONDITION_NOT_MET if the participant has active entities, RETCODE_OK if the participant is correctly
     * deleted and RETCODE_ERROR otherwise.
     */
    ReturnCode_t delete_participant(
            DomainParticipant* part)
    {
        eprosima::fastdds::dds::DomainParticipantListener* listener =
            const_cast<eprosima::fastdds::dds::DomainParticipantListener*>(part->get_listener());
        eprosima::fastdds::dds::ReturnCode_t ret = self->delete_participant(part);

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

%ignore eprosima::fastdds::dds::DomainParticipantFactory::delete_participant;
%ignore eprosima::fastdds::dds::DomainParticipantFactory::get_dynamic_type_builder_from_xml_by_name;

%include "fastdds/dds/domain/DomainParticipantFactory.hpp"
