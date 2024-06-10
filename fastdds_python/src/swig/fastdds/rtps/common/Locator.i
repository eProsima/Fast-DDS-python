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
#include "fastdds/rtps/common/Locator.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastdds::rtps::Locator_t::Locator_t(Locator_t&&);
%ignore eprosima::fastdds::rtps::operator <<(std::ostream&, const Locator_t&);
%ignore eprosima::fastdds::rtps::operator >>(std::istream&, Locator_t&);
%ignore eprosima::fastdds::rtps::operator ==(const Locator_t&, const Locator_t&);
%ignore eprosima::fastdds::rtps::operator !=(const Locator_t&, const Locator_t&);

%typemap(in) eprosima::fastdds::rtps::octet[16](eprosima::fastdds::rtps::octet temp[16])
{
    if (PyTuple_Check($input))
    {
        if (!PyArg_ParseTuple($input, "BBBBBBBBBBBBBBBB",
                    temp, temp+1, temp+2, temp+3, temp+4, temp+5, temp+6, temp+7, temp+8, temp+9, temp+10, temp+11,
                    temp+12, temp+13, temp+14, temp+15))
        {
            PyErr_SetString(PyExc_TypeError, "tuple must have 16 elements");
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

%typemap(out) eprosima::fastdds::rtps::octet[16]
{
    PyObject* python_tuple = PyTuple_New(16);

    if (python_tuple)
    {
        for(size_t count = 0; count < 16; ++count)
        {
            PyTuple_SetItem(python_tuple, count, PyInt_FromLong($1[count]));
        }
    }

    $result = python_tuple;
}

%include "fastdds/rtps/common/Locator.h"

%extend eprosima::fastdds::rtps::Locator_t
{
    bool operator==(const Locator_t& other_locator) const
    {
        return *self == other_locator;

    }

    bool operator!=(const Locator_t& other_locator) const
    {
        return *self == other_locator;

    }
}
