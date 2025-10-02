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
#include <stdexcept>
#include <vector>

#include "fastdds/rtps/common/InstanceHandle.hpp"

// Define a hash method in global scope for InstanceHandle_t types
// This is necessary if we want other classes to hash an internal InstanceHandle_t
long hash(const eprosima::fastdds::rtps::InstanceHandle_t& handle)
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
%rename(get_guid) eprosima::fastdds::rtps::InstanceHandle_t::operator const GUID_t&;

%ignore eprosima::fastdds::rtps::InstanceHandleValue_t::operator [] const;
%ignore eprosima::fastdds::rtps::InstanceHandleValue_t::operator [];
%ignore eprosima::fastdds::rtps::operator <<(std::ostream&, const InstanceHandle_t&);
%ignore eprosima::fastdds::rtps::operator >>(std::istream&, InstanceHandle_t&);
%ignore eprosima::fastdds::rtps::InstanceHandleValue_t::operator const octet* () const;
%ignore eprosima::fastdds::rtps::InstanceHandleValue_t::operator octet* ();

%extend eprosima::fastdds::rtps::InstanceHandleValue_t {

    // Constructor from sequence of 16 bytes (tupla/lista/bytes/bytearray)
    InstanceHandleValue_t(PyObject* seq) {
        eprosima::fastdds::rtps::InstanceHandleValue_t* self = new eprosima::fastdds::rtps::InstanceHandleValue_t();
        SWIG_PYTHON_THREAD_BEGIN_BLOCK;

        // Fast-path: bytes
        if (PyBytes_Check(seq)) {
            if (PyBytes_GET_SIZE(seq) == 16)
            {
                const char* b = PyBytes_AS_STRING(seq);
                for (int i = 0; i < 16; ++i) (*self)[i] = (uint8_t)(unsigned char)b[i];
            }
            else
            {
                delete self;
                self = nullptr;
                PyErr_SetString(PyExc_ValueError, "Expected 16 bytes");
            }
        }
        // Fast-path: bytearray
        else if (PyByteArray_Check(seq))
        {
            if (PyByteArray_GET_SIZE(seq) == 16)
            {
                const char* b = PyByteArray_AS_STRING(seq);
                for (int i = 0; i < 16; ++i) (*self)[i] = (uint8_t)(unsigned char)b[i];
            }
            else
            {
                delete self;
                self = nullptr;
                PyErr_SetString(PyExc_ValueError, "Expected 16 bytes");
            }
        }
        else
        {
            // Generic fallback: iterable from 16 ints 0..255
            PyObject* it = PyObject_GetIter(seq);
            size_t count {0};
            if (it)
            {
                PyObject* item {nullptr};
                while ((item = PyIter_Next(it)))
                {
                    long val = PyLong_AsLong(item);
                    Py_DECREF(item);
                    if (val == -1 && PyErr_Occurred())
                    {
                        delete self;
                        self = nullptr;
                        PyErr_SetString(PyExc_TypeError, "Sequence must contain integers");
                        break;
                    }
                    else if (val < 0 || val > 255)
                    {
                        delete self;
                        self = nullptr;
                        PyErr_SetString(PyExc_ValueError, "Each value must be in 0..255");
                        break;
                    }

                    (*self)[count] = static_cast<uint8_t>(val);
                    ++count;
                }
                Py_DECREF(it);
                if (count != 16)
                {
                    delete self;
                    self = nullptr;
                    PyErr_SetString(PyExc_ValueError, "Expected 16 elements");
                }
            }
            else
            {
                delete self;
                self = nullptr;
                PyErr_SetString(PyExc_TypeError, "Expected a sequence of 16 integers (0..255) or 16-byte object");
            }
        }

        SWIG_PYTHON_THREAD_END_BLOCK;

        return self;
    }

    size_t __len__() const { return 16; }

    uint8_t __getitem__(size_t i) const {
        if (i >= 16) throw std::out_of_range("index out of range");
        return $self->operator[](i);
    }

    void __setitem__(size_t i, uint8_t v) {
        if (i >= 16) throw std::out_of_range("index out of range");
        $self->operator[](i) = v;
    }
}

%ignore eprosima::fastdds::rtps::InstanceHandle_t::value;

// Declare the comparison operators as internal to the class
%extend eprosima::fastdds::rtps::InstanceHandle_t {

    bool operator==(const eprosima::fastdds::rtps::InstanceHandle_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastdds::rtps::InstanceHandle_t& other) const
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

    // Setter from sequence (tuple/list/bytes/bytearray)
    void from_sequence(PyObject* seq) {
        // Reutiliza el constructor para validar y copiar
        eprosima::fastdds::rtps::InstanceHandleValue_t* tmp = new_eprosima_fastdds_rtps_InstanceHandleValue_t(seq);
        for (int i = 0; i < 16; ++i) $self->value[i] = (*tmp)[i];
        delete tmp; // evitar fuga
    }

    // Getter: return a tuple of 16 ints (0..255)
    PyObject* to_sequence() const {
        SWIG_PYTHON_THREAD_BEGIN_BLOCK;

        PyObject* python_tuple = PyTuple_New(16);

        if (python_tuple)
        {
            for(size_t count = 0; count < 16; ++count)
            {
                PyTuple_SetItem(python_tuple, count, PyInt_FromLong($self->value[count]));
            }
        }

        SWIG_PYTHON_THREAD_END_BLOCK;

        return python_tuple;
    }
}

// Template for std::vector<InstanceHandle_t>
%template(InstanceHandleVector) std::vector<eprosima::fastdds::rtps::InstanceHandle_t>;
%typemap(doctype) std::vector<eprosima::fastdds::rtps::InstanceHandle_t>"InstanceHandleVector";

%include "fastdds/rtps/common/InstanceHandle.hpp"

%pythoncode %{
def _ihv_get_value(self):
    return self.to_sequence()

def _ihv_set_value(self, seq):
    self.from_sequence(seq)

InstanceHandle_t.value = property(_ihv_get_value, _ihv_set_value,
                                       doc="16-byte value as list/tuple/bytes/bytearray")
%}
