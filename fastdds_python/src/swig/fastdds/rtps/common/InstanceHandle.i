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
#include "fastdds/rtps/common/InstanceHandle.h"

// Define a hash method in global scope for InstanceHandle_t types
// This is necessary if we want other classes to hash an internal InstanceHandle_t
long hash(const eprosima::fastrtps::rtps::InstanceHandle_t& handle)
{
    long ret = 0;
    for (unsigned int i = 0; i < 16; ++i)
    {
        ret = (ret * 31) ^ handle.value[i];
    }
    return ret;
}

%}

// SWIG does not support type conversion operators correctly unless converted to a normal method
%rename(get_guid) eprosima::fastrtps::rtps::InstanceHandle_t::operator const GUID_t&;

%ignore eprosima::fastrtps::rtps::InstanceHandleValue_t::operator [] const;
%ignore eprosima::fastrtps::rtps::operator <<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastrtps::rtps::operator >>(std::istream&, InstanceHandle_t&);
%rename(read_pointer_cast) eprosima::fastrtps::rtps::InstanceHandleValue_t::operator const octet* () const;
%rename(write_pointer_cast) eprosima::fastrtps::rtps::InstanceHandleValue_t::operator octet* ();

%typemap(in) eprosima::fastrtps::rtps::InstanceHandleValue_t*(eprosima::fastrtps::rtps::InstanceHandleValue_t temp)
{
    if (PyTuple_Check($input))
    {
        eprosima::fastrtps::rtps::octet* buf = temp;
        if (!PyArg_ParseTuple($input, "BBBBBBBBBBBBBBBB",
                    buf, buf+1, buf+2, buf+3, buf+4, buf+5, buf+6, buf+7, buf+8,
                    buf+9, buf+10, buf+11, buf+12, buf+13, buf+14, buf+15))
        {
            PyErr_SetString(PyExc_TypeError, "tuple must have 16 elements");
            SWIG_fail;
        }
        $1 = &temp;
    }
    else
    {
        PyErr_SetString(PyExc_TypeError, "expected a tuple.");
        SWIG_fail;
    }
}

%typemap(out) eprosima::fastrtps::rtps::InstanceHandleValue_t*
{
    constexpr size_t ih_size = std::tuple_size<eprosima::fastrtps::rtps::KeyHash_t>::value;
    PyObject* python_tuple = PyTuple_New(ih_size);

    if (python_tuple)
    {
        for(size_t count = 0; count < ih_size; ++count)
        {
            PyTuple_SetItem(python_tuple, count, PyInt_FromLong((*$1)[count]));
        }
    }

    $result = python_tuple;
}

// Template for std::vector<InstanceHandle_t>
%template(InstanceHandleVector) std::vector<eprosima::fastrtps::rtps::InstanceHandle_t>;
%typemap(doctype) std::vector<eprosima::fastrtps::rtps::InstanceHandle_t>"InstanceHandleVector";

%include "fastdds/rtps/common/InstanceHandle.h"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::InstanceHandle_t {

    bool operator==(const eprosima::fastrtps::rtps::InstanceHandle_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::InstanceHandle_t& other) const
    {
        return *$self != other;
    }

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
