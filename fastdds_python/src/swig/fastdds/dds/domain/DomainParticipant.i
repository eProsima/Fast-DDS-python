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
#include "fastdds/dds/domain/DomainParticipant.hpp"
%}

%extend eprosima::fastdds::dds::DomainParticipant
{
    /**
     * Modifies the DomainParticipantListener, sets the mask to StatusMask::all()
     *
     * @param listener new value for the DomainParticipantListener
     * @return RETCODE_OK
     */
    ReturnCode_t set_listener(
            DomainParticipantListener* listener)
    {
        eprosima::fastdds::dds::DomainParticipantListener* old_listener =
            const_cast<eprosima::fastdds::dds::DomainParticipantListener*>(self->get_listener());

        eprosima::fastdds::dds::ReturnCode_t ret = self->set_listener(listener);

        if ( (eprosima::fastdds::dds::RETCODE_OK == ret) && (listener != old_listener) )
        {

            SWIG_PYTHON_THREAD_BEGIN_BLOCK;
            if (nullptr != listener)
            {
                Swig::Director* director = SWIG_DIRECTOR_CAST(listener);

                if (nullptr != director)
                {
                    Py_INCREF(director->swig_get_self());
                }
            }
            if (nullptr != old_listener)
            {
                Swig::Director* director = SWIG_DIRECTOR_CAST(old_listener);

                if (nullptr != director)
                {
                    Py_DECREF(director->swig_get_self());
                }
            }
            SWIG_PYTHON_THREAD_END_BLOCK;

        }

        return ret;
    }

    /**
     * Modifies the DomainParticipantListener.
     *
     * @param listener new value for the DomainParticipantListener
     * @param mask StatusMask that holds statuses the listener responds to
     * @return RETCODE_OK
     */
    ReturnCode_t set_listener(
            DomainParticipantListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::DomainParticipantListener* old_listener =
            const_cast<eprosima::fastdds::dds::DomainParticipantListener*>(self->get_listener());

        eprosima::fastdds::dds::ReturnCode_t ret = self->set_listener(listener, mask);

        if ( (eprosima::fastdds::dds::RETCODE_OK == ret) && (listener != old_listener) )
        {

            SWIG_PYTHON_THREAD_BEGIN_BLOCK;
            if (nullptr != listener)
            {
                Swig::Director* director = SWIG_DIRECTOR_CAST(listener);

                if (nullptr != director)
                {
                    Py_INCREF(director->swig_get_self());
                }
            }
            if (nullptr != old_listener)
            {
                Swig::Director* director = SWIG_DIRECTOR_CAST(old_listener);

                if (nullptr != director)
                {
                    Py_DECREF(director->swig_get_self());
                }
            }
            SWIG_PYTHON_THREAD_END_BLOCK;

        }

        return ret;
    }

    /**
     * Create a Publisher in this Participant.
     *
     * @param qos QoS of the Publisher.
     * @param listener Pointer to the listener (default: nullptr)
     * @param mask StatusMask that holds statuses the listener responds to (default: all)
     * @return Pointer to the created Publisher.
     */
    Publisher* create_publisher(
            const PublisherQos& qos,
            PublisherListener* listener = nullptr,
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

        return self->create_publisher(qos, listener, mask);
    }

    /**
     * Create a Publisher in this Participant.
     *
     * @param profile_name Publisher profile name.
     * @param listener Pointer to the listener (default: nullptr)
     * @param mask StatusMask that holds statuses the listener responds to (default: all)
     * @return Pointer to the created Publisher.
     */
    Publisher* create_publisher_with_profile(
            const std::string& profile_name,
            PublisherListener* listener = nullptr,
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

        return self->create_publisher_with_profile(profile_name, listener, mask);
    }

    /**
     * Deletes an existing Publisher.
     *
     * @param publisher to be deleted.
     * @return RETCODE_PRECONDITION_NOT_MET if the publisher does not belong to this participant or if it has active DataWriters,
     * RETCODE_OK if it is correctly deleted and RETCODE_ERROR otherwise.
     */
    ReturnCode_t delete_publisher(
            const Publisher* publisher)
    {
        eprosima::fastdds::dds::PublisherListener* listener =
            const_cast<eprosima::fastdds::dds::PublisherListener*>(publisher->get_listener());
        eprosima::fastdds::dds::ReturnCode_t ret = self->delete_publisher(publisher);

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

    /**
     * Create a Subscriber in this Participant.
     *
     * @param qos QoS of the Subscriber.
     * @param listener Pointer to the listener (default: nullptr)
     * @param mask StatusMask that holds statuses the listener responds to (default: all)
     * @return Pointer to the created Subscriber.
     */
    Subscriber* create_subscriber(
            const SubscriberQos& qos,
            SubscriberListener* listener = nullptr,
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

        return self->create_subscriber(qos, listener, mask);
    }

    /**
     * Create a Subscriber in this Participant.
     *
     * @param profile_name Subscriber profile name.
     * @param listener Pointer to the listener (default: nullptr)
     * @param mask StatusMask that holds statuses the listener responds to (default: all)
     * @return Pointer to the created Subscriber.
     */
    FASTDDS_EXPORTED_API Subscriber* create_subscriber_with_profile(
            const std::string& profile_name,
            SubscriberListener* listener = nullptr,
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

        return self->create_subscriber_with_profile(profile_name, listener, mask);
    }

    /**
     * Deletes an existing Subscriber.
     *
     * @param subscriber to be deleted.
     * @return RETCODE_PRECONDITION_NOT_MET if the subscriber does not belong to this participant or if it has active DataReaders,
     * RETCODE_OK if it is correctly deleted and RETCODE_ERROR otherwise.
     */
    ReturnCode_t delete_subscriber(
            const Subscriber* subscriber)
    {
        eprosima::fastdds::dds::SubscriberListener* listener =
            const_cast<eprosima::fastdds::dds::SubscriberListener*>(subscriber->get_listener());
        eprosima::fastdds::dds::ReturnCode_t ret = self->delete_subscriber(subscriber);

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

%ignore eprosima::fastdds::dds::DomainParticipant::has_active_entities;
%ignore eprosima::fastdds::dds::DomainParticipant::DomainParticipant;
%ignore eprosima::fastdds::dds::DomainParticipant::~DomainParticipant;
%ignore eprosima::fastdds::dds::DomainParticipant::set_listener;
%ignore eprosima::fastdds::dds::DomainParticipant::create_publisher;
%ignore eprosima::fastdds::dds::DomainParticipant::create_publisher_with_profile;
%ignore eprosima::fastdds::dds::DomainParticipant::create_subscriber;
%ignore eprosima::fastdds::dds::DomainParticipant::delete_publisher;
%ignore eprosima::fastdds::dds::DomainParticipant::delete_subscriber;
%ignore eprosima::fastdds::dds::DomainParticipant::create_subscriber_with_profile;

// Template for std::vector<DomainParticipant*>
%template(DomainParticipantVector) std::vector<eprosima::fastdds::dds::DomainParticipant*>;
%typemap(doctype) std::vector<eprosima::fastdds::dds::DomainParticipant*> "DomainParticipantVector";

%include "fastdds/dds/domain/DomainParticipant.hpp"
