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
    /**
     * Modifies the SubscriberListener, sets the mask to StatusMask::all()
     *
     * @param listener new value for SubscriberListener
     * @return RETCODE_OK
     */
    ReturnCode_t set_listener(
            SubscriberListener* listener)
    {
        eprosima::fastdds::dds::SubscriberListener* old_listener =
            const_cast<eprosima::fastdds::dds::SubscriberListener*>(self->get_listener());

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

    /**
     * Modifies the SubscriberListener.
     *
     * @param listener new value for the SubscriberListener
     * @param mask StatusMask that holds statuses the listener responds to.
     * @return RETCODE_OK
     */
    ReturnCode_t set_listener(
            SubscriberListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::SubscriberListener* old_listener =
            const_cast<eprosima::fastdds::dds::SubscriberListener*>(self->get_listener());

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

    /**
     * This operation creates a DataReader. The returned DataReader will be attached and belong to the Subscriber.
     *
     * @param topic Topic the DataReader will be listening.
     * @param reader_qos QoS of the DataReader.
     * @param listener Pointer to the listener (default: nullptr)
     * @param mask StatusMask that holds statuses the listener responds to (default: all).
     * @return Pointer to the created DataReader. nullptr if failed.
     */
    DataReader* create_datareader(
            TopicDescription* topic,
            const DataReaderQos& reader_qos,
            DataReaderListener* listener = nullptr,
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

        return self->create_datareader(topic, reader_qos, listener, mask);
    }

    /**
     * This operation creates a DataReader. The returned DataReader will be attached and belongs to the Subscriber.
     *
     * @param topic Topic the DataReader will be listening.
     * @param profile_name DataReader profile name.
     * @param listener Pointer to the listener (default: nullptr)
     * @param mask StatusMask that holds statuses the listener responds to (default: all).
     * @return Pointer to the created DataReader. nullptr if failed.
     */
    RTPS_DllAPI DataReader* create_datareader_with_profile(
            TopicDescription* topic,
            const std::string& profile_name,
            DataReaderListener* listener = nullptr,
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

        return self->create_datareader_with_profile(topic, profile_name, listener, mask);
    }

    /**
     * This operation deletes a DataReader that belongs to the Subscriber.
     *
     * The delete_datareader operation must be called on the same Subscriber object used to create the DataReader.
     * If delete_datareader is called on a different Subscriber, the operation will have no effect and it will
     * return an error.
     *
     * @param reader DataReader to delete
     * @return RETCODE_PRECONDITION_NOT_MET if the datareader does not belong to this subscriber, RETCODE_OK if it is correctly
     * deleted and RETCODE_ERROR otherwise.
     */
    ReturnCode_t delete_datareader(
            const DataReader* reader)
    {
        eprosima::fastdds::dds::DataReaderListener* listener =
            const_cast<eprosima::fastdds::dds::DataReaderListener*>(reader->get_listener());
        eprosima::fastrtps::types::ReturnCode_t ret = self->delete_datareader(reader);

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

%ignore eprosima::fastdds::dds::Subscriber::Subscriber;
%ignore eprosima::fastdds::dds::Subscriber::~Subscriber;
%ignore eprosima::fastdds::dds::Subscriber::set_listener;
%ignore eprosima::fastdds::dds::Subscriber::create_datareader;
%ignore eprosima::fastdds::dds::Subscriber::delete_datareader;

%include "fastdds/dds/subscriber/Subscriber.hpp"
