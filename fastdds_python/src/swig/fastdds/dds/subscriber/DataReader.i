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
#include "fastdds/dds/subscriber/DataReader.hpp"
%}

// Template for std::vector<DataReader*>
%template(DataReaderVector) std::vector<eprosima::fastdds::dds::DataReader*>;
%typemap(doctype) std::vector<eprosima::fastdds::dds::DataReader*> "DataReaderVector";

%template(SampleInfoSeq) eprosima::fastdds::dds::LoanableSequence<eprosima::fastdds::dds::SampleInfo>;
%typemap(doctype) eprosima::fastdds::dds::LoanableSequence<eprosima::fastdds::dds::SampleInfo> "SampleInfoSeq";
%extend eprosima::fastdds::dds::LoanableSequence<eprosima::fastdds::dds::SampleInfo>
{
    size_t __len__() const
    {
        return self->length();
    }

    const eprosima::fastdds::dds::SampleInfo& __getitem__(size_t i) const
    {
        return (*self)[i];
    }
}


%extend eprosima::fastdds::dds::DataReader
{
    ReturnCode_t set_listener(
            DataReaderListener* listener)
    {
        eprosima::fastdds::dds::DataReaderListener* old_listener =
            const_cast<eprosima::fastdds::dds::DataReaderListener*>(self->get_listener());

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
            DataReaderListener* listener,
            const StatusMask& mask)
    {
        eprosima::fastdds::dds::DataReaderListener* old_listener =
            const_cast<eprosima::fastdds::dds::DataReaderListener*>(self->get_listener());

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
}

%ignore eprosima::fastdds::dds::DataReader::set_listener;

%include "fastdds/dds/subscriber/DataReader.hpp"
