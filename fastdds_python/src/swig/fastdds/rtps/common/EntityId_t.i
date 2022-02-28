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
#include "fastdds/rtps/common/EntityId_t.hpp"

// Define a hash method in global scope for EntityId_t types
// This is necessary if we want other classes to hash an internal EntityId_t
long hash(const eprosima::fastrtps::rtps::EntityId_t& id)
{
    long ret = 0;
    for (unsigned int i = 0; i < eprosima::fastrtps::rtps::EntityId_t::size; ++i)
    {
        ret = (ret * 31) ^ id.value[i];
    }
    return ret;
}
%}

// Overloaded constructor ignored
%ignore eprosima::fastrtps::rtps::EntityId_t::EntityId_t(EntityId_t &&);
%ignore eprosima::fastrtps::rtps::operator <<(std::ostream&, const EntityId_t&);
%ignore eprosima::fastrtps::rtps::operator >>(std::istream&, EntityId_t&);

// Operators declared outside the class conflict with those declared for other types
%ignore eprosima::fastrtps::rtps::operator==;
%ignore eprosima::fastrtps::rtps::operator!=;

// Declare hash so that we do not get a warning
// This will make an empty class on the target, but the user should not need this anyway.
namespace std {
    template <typename T>
    struct hash;
}

%typemap(in) eprosima::fastrtps::rtps::octet[eprosima::fastrtps::rtps::EntityId_t::size](eprosima::fastrtps::rtps::octet temp[eprosima::fastrtps::rtps::EntityId_t::size])
{
    if (PyTuple_Check($input))
    {
        if (!PyArg_ParseTuple($input, "BBBB",
                    temp, temp+1, temp+2, temp+3))
        {
            PyErr_SetString(PyExc_TypeError, "tuple must have 4 elements");
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

%typemap(out) eprosima::fastrtps::rtps::octet[eprosima::fastrtps::rtps::EntityId_t::size]
{
    PyObject* python_tuple = PyTuple_New(eprosima::fastrtps::rtps::EntityId_t::size);

    if (python_tuple)
    {
        for(size_t count = 0; count < eprosima::fastrtps::rtps::EntityId_t::size; ++count)
        {
            PyTuple_SetItem(python_tuple, count, PyInt_FromLong($1[count]));
        }
    }

    $result = python_tuple;
}

%include "fastdds/rtps/common/EntityId_t.hpp"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::EntityId_t {
    bool operator==(const eprosima::fastrtps::rtps::EntityId_t& other) const
    {
        return *$self == other;
    }

    bool operator==(uint32_t other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::EntityId_t& other) const
    {
        return *$self != other;
    }

    // Define the hash method using the global one
    std::string __str__() const
    {
        std::ostringstream out;
        out << *$self;
        return out.str();
    }

    long __hash__() const
    {
        return hash(*$self);
    }
}
