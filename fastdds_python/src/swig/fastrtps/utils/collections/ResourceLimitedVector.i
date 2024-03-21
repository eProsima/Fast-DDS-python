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
#include "fastdds/utils/collections/ResourceLimitedVector.hpp"
%}

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

// Initializer lists are note supported in SWIG. Ignore the method
%ignore eprosima::fastrtps::ResourceLimitedVector::assign(std::initializer_list<value_type>);

// Casting to the inner 'collection_type' makes no sense in the target language
// and SWIG does not support it in any case
%ignore eprosima::fastrtps::ResourceLimitedVector::operator const collection_type&;


%extend eprosima::fastrtps::ResourceLimitedVector {
    pointer at(size_type pos)
    {
        return &($self->at(pos));
    }
    pointer front()
    {
        return &($self->front());
    }
    pointer back()
    {
        return &($self->back());
    }

    pointer getitem(size_type n) {
        return &($self->operator[](n));
    }

    void setitem(size_type n, const_pointer v) {
        $self->operator[](n) = *v;
    }
}

%include "fastdds/utils/collections/ResourceLimitedVector.hpp"
