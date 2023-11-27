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
    /**
     * Create a Participant.
     *
     * @param domain_id Domain Id.
     * @param qos DomainParticipantQos Reference.
     * @param listener DomainParticipantListener Pointer (default: nullptr)
     * @param mask StatusMask Reference (default: all)
     * @return DomainParticipant pointer. (nullptr if not created.)
     */
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

    /**
     * Create a Participant.
     *
     * @param domain_id Domain Id.
     * @param profile_name Participant profile name.
     * @param listener DomainParticipantListener Pointer (default: nullptr)
     * @param mask StatusMask Reference (default: all)
     * @return DomainParticipant pointer. (nullptr if not created.)
     */
    DomainParticipant* create_participant_with_profile(
            DomainId_t domain_id,
            const std::string& profile_name,
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

        return self->create_participant_with_profile(domain_id, profile_name, listener, mask);
    }

    /**
     * Create a Participant.
     *
     * @param profile_name Participant profile name.
     * @param listener DomainParticipantListener Pointer (default: nullptr)
     * @param mask StatusMask Reference (default: all)
     * @return DomainParticipant pointer. (nullptr if not created.)
     */
    DomainParticipant* create_participant_with_profile(
            const std::string& profile_name,
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

        return self->create_participant_with_profile(profile_name, listener, mask);
    }

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

%ignore eprosima::fastdds::dds::DomainParticipantFactory::create_participant;
%ignore eprosima::fastdds::dds::DomainParticipantFactory::create_participant_with_profile;
%ignore eprosima::fastdds::dds::DomainParticipantFactory::delete_participant;

%include "fastdds/dds/domain/DomainParticipantFactory.hpp"
