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
#include "fastdds/dds/publisher/DataWriter.hpp"
%}


// Deprecated function are ignored
%ignore eprosima::fastdds::dds::DataWriter::write_w_timestamp(void*, const InstanceHandle_t&,
            const fastrtps::rtps::Time_t&);
%ignore eprosima::fastdds::dds::DataWriter::register_instance_w_timestamp(void*,
            const fastrtps::rtps::Time_t&);
%ignore eprosima::fastdds::dds::DataWriter::unregister_instance_w_timestamp(void*, const InstanceHandle_t&,
            const fastrtps::rtps::Time_t&);
%ignore eprosima::fastdds::dds::DataWriter::get_matched_subscriptions(
            std::vector<InstanceHandle_t*>&) const;

// Unsupported function on Python are ignored
%ignore loan_sample(void*&, LoanInitializationKind);
%ignore discard_loan(void*&);


// Tell SWIG to convert parameter size_t* removed in an output parameter
%apply size_t* OUTPUT { size_t* removed }
// Ignore C++ clear_history because we need to overload it in Python.
%extend eprosima::fastdds::dds::DataWriter
{
    // TODO Document with %feature("autodoc")
    eprosima::fastdds::dds::ReturnCode_t clear_history(size_t* removed)
    {
        eprosima::fastdds::dds::ReturnCode_t ret = self->clear_history(removed);
        return ret;
    }

    ReturnCode_t set_listener(
            DataWriterListener* listener)
    {
        eprosima::fastdds::dds::DataWriterListener* old_listener =
            const_cast<eprosima::fastdds::dds::DataWriterListener*>(self->get_listener());

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

    ReturnCode_t set_listener(
            DataWriterListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::DataWriterListener* old_listener =
            const_cast<eprosima::fastdds::dds::DataWriterListener*>(self->get_listener());

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
}

%ignore eprosima::fastdds::dds::DataWriter::set_listener;
%ignore eprosima::fastdds::dds::DataWriter::clear_history(size_t*);

// Template for std::vector<DataWriter*>
%template(DataWriterVector) std::vector<eprosima::fastdds::dds::DataWriter*>;

%include "fastdds/dds/publisher/DataWriter.hpp"

%clear size_t* removed;
