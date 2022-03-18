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
#include "fastdds/dds/publisher/Publisher.hpp"
%}

%extend eprosima::fastdds::dds::Publisher
{
    ReturnCode_t set_listener(
            PublisherListener* listener)
    {
        eprosima::fastdds::dds::PublisherListener* old_listener =
            const_cast<eprosima::fastdds::dds::PublisherListener*>(self->get_listener());

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
            PublisherListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::PublisherListener* old_listener =
            const_cast<eprosima::fastdds::dds::PublisherListener*>(self->get_listener());

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

    DataWriter* create_datawriter(
            Topic* topic,
            const DataWriterQos& writer_qos,
            DataWriterListener* listener = nullptr,
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

        return self->create_datawriter(topic, writer_qos, listener, mask);
    }

    ReturnCode_t delete_datawriter(
            const DataWriter* writer)
    {
        eprosima::fastdds::dds::DataWriterListener* listener =
            const_cast<eprosima::fastdds::dds::DataWriterListener*>(writer->get_listener());
        eprosima::fastrtps::types::ReturnCode_t ret = self->delete_datawriter(writer);

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

%ignore eprosima::fastdds::dds::Publisher::Publisher;
%ignore eprosima::fastdds::dds::Publisher::~Publisher;
%ignore eprosima::fastdds::dds::Publisher::set_listener;
%ignore eprosima::fastdds::dds::Publisher::create_datawriter;
%ignore eprosima::fastdds::dds::Publisher::delete_datawriter;

%include "fastdds/dds/publisher/Publisher.hpp"
