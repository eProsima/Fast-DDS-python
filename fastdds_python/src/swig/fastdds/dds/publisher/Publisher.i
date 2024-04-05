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
    /**
     * Modifies the PublisherListener, sets the mask to StatusMask::all()
     *
     * @param listener new value for the PublisherListener
     * @return RETCODE_OK
     */
    ReturnCode_t set_listener(
            PublisherListener* listener)
    {
        eprosima::fastdds::dds::PublisherListener* old_listener =
            const_cast<eprosima::fastdds::dds::PublisherListener*>(self->get_listener());

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
     * Modifies the PublisherListener.
     *
     * @param listener new value for the PublisherListener
     * @param mask StatusMask that holds statuses the listener responds to
     * @return RETCODE_OK
     */
    ReturnCode_t set_listener(
            PublisherListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::PublisherListener* old_listener =
            const_cast<eprosima::fastdds::dds::PublisherListener*>(self->get_listener());

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
     * This operation creates a DataWriter. The returned DataWriter will be attached and belongs to the Publisher.
     *
     * @param topic Topic the DataWriter will be listening
     * @param qos QoS of the DataWriter.
     * @param listener Pointer to the listener (default: nullptr).
     * @param mask StatusMask that holds statuses the listener responds to (default: all).
     * @return Pointer to the created DataWriter. nullptr if failed.
     */
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

    /**
     * This operation creates a DataWriter. The returned DataWriter will be attached and belongs to the Publisher.
     *
     * @param topic Topic the DataWriter will be listening
     * @param profile_name DataWriter profile name.
     * @param listener Pointer to the listener (default: nullptr).
     * @param mask StatusMask that holds statuses the listener responds to (default: all).
     * @return Pointer to the created DataWriter. nullptr if failed.
     */
    DataWriter* create_datawriter_with_profile(
            Topic* topic,
            const std::string& profile_name,
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

        return self->create_datawriter_with_profile(topic, profile_name, listener, mask);
    }

    /**
     * This operation deletes a DataWriter that belongs to the Publisher.
     *
     * The delete_datawriter operation must be called on the same Publisher object used to create the DataWriter.
     * If delete_datawriter is called on a different Publisher, the operation will have no effect and it will
     * return false.
     *
     * The deletion of the DataWriter will automatically unregister all instances.
     * Depending on the settings of the WRITER_DATA_LIFECYCLE QosPolicy, the deletion of the DataWriter
     * may also dispose all instances.
     *
     * @param writer DataWriter to delete
     * @return RETCODE_PRECONDITION_NOT_MET if it does not belong to this Publisher, RETCODE_OK if it is correctly deleted and
     * RETCODE_ERROR otherwise.
     */
    ReturnCode_t delete_datawriter(
            const DataWriter* writer)
    {
        eprosima::fastdds::dds::DataWriterListener* listener =
            const_cast<eprosima::fastdds::dds::DataWriterListener*>(writer->get_listener());
        eprosima::fastdds::dds::ReturnCode_t ret = self->delete_datawriter(writer);

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
%ignore eprosima::fastdds::dds::Publisher::create_datawriter_with_profile;
%ignore eprosima::fastdds::dds::Publisher::delete_datawriter;

%include "fastdds/dds/publisher/Publisher.hpp"
