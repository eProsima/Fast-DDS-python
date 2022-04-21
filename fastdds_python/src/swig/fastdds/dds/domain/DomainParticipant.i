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
    ReturnCode_t set_listener(
            DomainParticipantListener* listener)
    {
        eprosima::fastdds::dds::DomainParticipantListener* old_listener =
            const_cast<eprosima::fastdds::dds::DomainParticipantListener*>(self->get_listener());

        eprosima::fastrtps::types::ReturnCode_t ret = self->set_listener(listener);

        if ( (eprosima::fastrtps::types::ReturnCode_t::RETCODE_OK == ret) && (listener != old_listener) )
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

    ReturnCode_t set_listener(
            DomainParticipantListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::DomainParticipantListener* old_listener =
            const_cast<eprosima::fastdds::dds::DomainParticipantListener*>(self->get_listener());

        eprosima::fastrtps::types::ReturnCode_t ret = self->set_listener(listener, mask);

        if ( (eprosima::fastrtps::types::ReturnCode_t::RETCODE_OK == ret) && (listener != old_listener) )
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

    ReturnCode_t delete_publisher(
            const Publisher* publisher)
    {
        eprosima::fastdds::dds::PublisherListener* listener =
            const_cast<eprosima::fastdds::dds::PublisherListener*>(publisher->get_listener());
        eprosima::fastrtps::types::ReturnCode_t ret = self->delete_publisher(publisher);

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

    ReturnCode_t delete_subscriber(
            const Subscriber* subscriber)
    {
        eprosima::fastdds::dds::SubscriberListener* listener =
            const_cast<eprosima::fastdds::dds::SubscriberListener*>(subscriber->get_listener());
        eprosima::fastrtps::types::ReturnCode_t ret = self->delete_subscriber(subscriber);

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
%ignore eprosima::fastdds::dds::DomainParticipant::create_subscriber;
%ignore eprosima::fastdds::dds::DomainParticipant::delete_publisher;
%ignore eprosima::fastdds::dds::DomainParticipant::delete_subscriber;

%include "fastdds/dds/domain/DomainParticipant.hpp"
