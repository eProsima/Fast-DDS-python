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
#include "fastrtps/utils/collections/ResourceLimitedVector.hpp"
%}

%include "exception.i"

// Operator[] is ignored by SWIG because it does not map correctly to target languages
// mostly because of its dual getter/setter nature
// We can ignore them and extend to make the getter and setter methods explicit and break the overload
%ignore eprosima::fastrtps::ResourceLimitedVector::operator[];

// These methods return references.
// This is usually supported by SWIG, however, this being a template, and the returns being typedefs,
// it seems that SWIG handles them differently and compilation fails
// when trying to create a pointer to a reference and/or calling new for a reference
// We rewrite them in terms of pointer results
%ignore eprosima::fastrtps::ResourceLimitedVector::at;
%ignore eprosima::fastrtps::ResourceLimitedVector::front;
%ignore eprosima::fastrtps::ResourceLimitedVector::back;
%ignore eprosima::fastrtps::ResourceLimitedVector::push_back;

// Initializer lists are note supported in SWIG. Ignore the method
%ignore eprosima::fastrtps::ResourceLimitedVector::assign(std::initializer_list<value_type>);

// Casting to the inner 'collection_type' makes no sense in the target language
// and SWIG does not support it in any case
%ignore eprosima::fastrtps::ResourceLimitedVector::operator const collection_type&;

%exception eprosima::fastdds::ResourceLimitedVector::__getitem__
{
    try
    {
        $action
    }
    catch(std::out_of_range)
    {
        SWIG_exception(SWIG_IndexError, "Index out of bounds");
    }
}


%extend eprosima::fastrtps::ResourceLimitedVector {

    size_t __len__() const
    {
        return self->size();
    }

    value_type __getitem__(int i)
    {
        if (self->size() <= i)
        {
            throw std::out_of_range("Index out of bounds");
        }
        return (*self)[i];
    }

    pointer getitem(size_type n) {
        return &($self->operator[](n));
    }

    void setitem(size_type n, value_type v) {
        $self->operator[](n) = v;
    }

    void append(value_type v) {
        $self->push_back(v);
    }
}

%include "fastrtps/utils/collections/ResourceLimitedVector.hpp"

%define resource_limited_vector_template(name_, value_type_)
%inline %{
    class name_ ## StopIterator {};
    class name_ ## Iterator
    {
    public:
        name_ ## Iterator(
                typename eprosima::fastrtps::ResourceLimitedVector<value_type_>::iterator _cur,
                typename eprosima::fastrtps::ResourceLimitedVector<value_type_>::iterator _end)
            : cur(_cur)
            , end(_end)
        {
        }

        name_ ## Iterator* __iter__()
        {
            return this;
        }
        typename eprosima::fastrtps::ResourceLimitedVector<value_type_>::iterator cur;
        typename eprosima::fastrtps::ResourceLimitedVector<value_type_>::iterator end;
    };
%}

%exception name_ ## Iterator::__next__ {
    try
    {
        $action // calls %extend function __next__() below
    }
    catch (name_ ## StopIterator)
    {
        PyErr_SetString(PyExc_StopIteration, "End of iterator");
        return nullptr;
    }
}

%extend name_ ## Iterator
{
    value_type_ __next__()
    {
        if ($self->cur != $self->end)
        {
            // dereference the iterator and return reference to the object,
            // after that it increments the iterator
            return *$self->cur++;
        }
        throw name_ ## StopIterator();
    }
}

%template(name_) eprosima::fastrtps::ResourceLimitedVector<value_type_>;

%extend eprosima::fastrtps::ResourceLimitedVector<value_type_>
{
    name_ ## Iterator __iter__()
    {
        // return a constructed Iterator object
        return name_ ## Iterator($self->begin(), $self->end());
    }
}
%enddef
