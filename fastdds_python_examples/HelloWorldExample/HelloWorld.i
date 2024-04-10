// Copyright 2016 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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

/*!
 * @file HelloWorld.i
 * This header file contains the SWIG interface of the described types in the IDL file.
 *
 * This file was generated by the tool fastddsgen.
 */

%module HelloWorld

// SWIG helper modules
%include "stdint.i"
%include "std_array.i"
%include "std_map.i"
%include "std_string.i"
%include "std_vector.i"
%include "typemaps.i"

// Assignemt operators are ignored, as there is no such thing in Python.
// Trying to export them issues a warning
%ignore *::operator=;

// Macro declarations
// Any macro used on the Fast DDS header files will give an error if it is not redefined here
#define FASTDDS_EXPORTED_API
#define eProsima_user_DllExport


%{
#include "HelloWorld.hpp"

#include <fastdds/dds/core/LoanableSequence.hpp>
%}

%include <fastcdr/config.h>
#if FASTCDR_VERSION_MAJOR > 1
%import(module="fastdds") "fastcdr/xcdr/optional.hpp"
#endif
%import(module="fastdds") "fastdds/dds/core/LoanableCollection.hpp"
%import(module="fastdds") "fastdds/dds/core/LoanableTypedCollection.hpp"
%import(module="fastdds") "fastdds/dds/core/LoanableSequence.hpp"

%define %traits_penumn(Type...)
  %fragment(SWIG_Traits_frag(Type),"header",
        fragment="StdTraits") {
namespace swig {
  template <> struct traits< Type > {
    typedef value_category category;
    static const char* type_name() { return  #Type; }
  };
}
}
%enddef

////////////////////////////////////////////////////////
// Binding for class HelloWorld
////////////////////////////////////////////////////////

// Ignore overloaded methods that have no application on Python
// Otherwise they will issue a warning
%ignore HelloWorld::HelloWorld(HelloWorld&&);

// Overloaded getter methods shadow each other and are equivalent in python
// Avoid a warning ignoring all but one
%ignore HelloWorld::index(uint32_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore HelloWorld::index();
%rename("%s") HelloWorld::index() const;



%ignore HelloWorld::message(std::string&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore HelloWorld::message();
%rename("%s") HelloWorld::message() const;



%template(_HelloWorldSeq) eprosima::fastdds::dds::LoanableTypedCollection<HelloWorld, std::false_type>;
%template(HelloWorldSeq) eprosima::fastdds::dds::LoanableSequence<HelloWorld, std::false_type>;
%extend eprosima::fastdds::dds::LoanableSequence<HelloWorld, std::false_type>
{
    size_t __len__() const
    {
        return self->length();
    }

    const HelloWorld& __getitem__(size_t i) const
    {
        return (*self)[i];
    }
}


// Include the class interfaces
%include "HelloWorld.hpp"

// Include the corresponding TopicDataType
%include "HelloWorldPubSubTypes.i"
