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
#include "fastdds/rtps/common/GuidPrefix_t.hpp"

// Define a hash method in global scope for GuidPrefix_t types
// This is necessary if we want other classes to hash an internal GuidPrefix_t
long hash(const eprosima::fastrtps::rtps::GuidPrefix_t& prefix)
{
    long ret = 0;
    for (unsigned int i = 0; i < eprosima::fastrtps::rtps::GuidPrefix_t::size; ++i)
    {
        ret = (ret * 31) ^ prefix.value[i];
    }
    return ret;
}
%}

%typemap(in) eprosima::fastrtps::rtps::octet[eprosima::fastrtps::rtps::GuidPrefix_t::size](eprosima::fastrtps::rtps::octet temp[eprosima::fastrtps::rtps::GuidPrefix_t::size])
{
    if (PyTuple_Check($input))
    {
        if (!PyArg_ParseTuple($input, "BBBBBBBBBBBB",
                    temp, temp+1, temp+2, temp+3, temp+4, temp+5, temp+6, temp+7, temp+8, temp+9, temp+10, temp+11))
        {
            PyErr_SetString(PyExc_TypeError, "tuple must have 12 elements");
            SWIG_fail;
        }
        $1 = &temp[0];
    }
    else
    {
        PyErr_SetString(PyExc_TypeError, "expected a tuple.");
        SWIG_fail;
    }
}

%typemap(out) eprosima::fastrtps::rtps::octet[eprosima::fastrtps::rtps::GuidPrefix_t::size]
{
    PyObject* python_tuple = PyTuple_New(eprosima::fastrtps::rtps::GuidPrefix_t::size);

    if (python_tuple)
    {
        for(size_t count = 0; count < eprosima::fastrtps::rtps::GuidPrefix_t::size; ++count)
        {
            PyTuple_SetItem(python_tuple, count, PyInt_FromLong($1[count]));
        }
    }

    $result = python_tuple;
}

%ignore eprosima::fastrtps::rtps::operator <<(std::ostream&, const GuidPrefix_t&);
%ignore eprosima::fastrtps::rtps::operator >>(std::istream&, GuidPrefix_t&);

%include "fastdds/rtps/common/GuidPrefix_t.hpp"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::GuidPrefix_t {
    std::string __str__() const
    {
        std::ostringstream out;
        out << *$self;
        return out.str();
    }

    // Define the hash method using the global one
    long __hash__() const
    {
        return hash(*$self);
    }
}

