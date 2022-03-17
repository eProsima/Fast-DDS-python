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
#include "fastdds/dds/subscriber/Subscriber.hpp"
%}

%extend eprosima::fastdds::dds::Subscriber
{
    ReturnCode_t set_listener(
            SubscriberListener* listener)
    {
        eprosima::fastdds::dds::SubscriberListener* old_listener =
            const_cast<eprosima::fastdds::dds::SubscriberListener*>(self->get_listener());

        eprosima::fastrtps::types::ReturnCode_t ret = self->set_listener(listener);

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

        return ret;
    }

    ReturnCode_t set_listener(
            SubscriberListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::SubscriberListener* old_listener =
            const_cast<eprosima::fastdds::dds::SubscriberListener*>(self->get_listener());

        eprosima::fastrtps::types::ReturnCode_t ret = self->set_listener(listener, mask);

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

        return ret;
    }
}

%ignore eprosima::fastdds::dds::Subscriber::Subscriber;
%ignore eprosima::fastdds::dds::Subscriber::~Subscriber;
%ignore eprosima::fastdds::dds::Subscriber::set_listener;

%include "fastdds/dds/subscriber/Subscriber.hpp"
