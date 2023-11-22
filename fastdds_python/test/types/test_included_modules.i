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
 * @file test_included_modules.i
 * This header file contains the SWIG interface of the described types in the IDL file.
 *
 * This file was generated by the tool fastddsgen.
 */

%module test_included_modules

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
#include "test_included_modules.hpp"

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

%traits_penumn(enum eprosima::test2::Color2);
%traits_penumn(enum eprosima::test2::Material2);


////////////////////////////////////////////////////////
// Binding for class eprosima::test2::StructType2
////////////////////////////////////////////////////////

// Ignore overloaded methods that have no application on Python
// Otherwise they will issue a warning
%ignore eprosima::test2::StructType2::StructType2(eprosima::test2::StructType2&&);

// Overloaded getter methods shadow each other and are equivalent in python
// Avoid a warning ignoring all but one
%ignore eprosima::test2::StructType2::char_field(char&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::char_field();
%rename("%s") eprosima::test2::StructType2::char_field() const;



%ignore eprosima::test2::StructType2::uint8_field(uint8_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::uint8_field();
%rename("%s") eprosima::test2::StructType2::uint8_field() const;



%ignore eprosima::test2::StructType2::int16_field(int16_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::int16_field();
%rename("%s") eprosima::test2::StructType2::int16_field() const;



%ignore eprosima::test2::StructType2::uint16_field(uint16_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::uint16_field();
%rename("%s") eprosima::test2::StructType2::uint16_field() const;



%ignore eprosima::test2::StructType2::int32_field(int32_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::int32_field();
%rename("%s") eprosima::test2::StructType2::int32_field() const;



%ignore eprosima::test2::StructType2::uint32_field(uint32_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::uint32_field();
%rename("%s") eprosima::test2::StructType2::uint32_field() const;



%ignore eprosima::test2::StructType2::int64_field(int64_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::int64_field();
%rename("%s") eprosima::test2::StructType2::int64_field() const;



%ignore eprosima::test2::StructType2::uint64_field(uint64_t&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::uint64_field();
%rename("%s") eprosima::test2::StructType2::uint64_field() const;



%ignore eprosima::test2::StructType2::float_field(float&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::float_field();
%rename("%s") eprosima::test2::StructType2::float_field() const;



%ignore eprosima::test2::StructType2::double_field(double&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::double_field();
%rename("%s") eprosima::test2::StructType2::double_field() const;



%ignore eprosima::test2::StructType2::bool_field(bool&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::bool_field();
%rename("%s") eprosima::test2::StructType2::bool_field() const;



%ignore eprosima::test2::StructType2::string_field(std::string&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::string_field();
%rename("%s") eprosima::test2::StructType2::string_field() const;



%ignore eprosima::test2::StructType2::enum_field(eprosima::test2::Color2&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::enum_field();
%rename("%s") eprosima::test2::StructType2::enum_field() const;



%ignore eprosima::test2::StructType2::enum2_field(eprosima::test2::Material2&&);


// Overloaded getter methods shadow each other and are equivalent in python
// Const accesors produced constant enums instead of arrays/dictionaries when used
// We ignore them to prevent this
%ignore eprosima::test2::StructType2::enum2_field();
%rename("%s") eprosima::test2::StructType2::enum2_field() const;



%template(_StructType2Seq) eprosima::fastdds::dds::LoanableTypedCollection<eprosima::test2::StructType2, std::false_type>;
%template(StructType2Seq) eprosima::fastdds::dds::LoanableSequence<eprosima::test2::StructType2, std::false_type>;
%extend eprosima::fastdds::dds::LoanableSequence<eprosima::test2::StructType2, std::false_type>
{
    size_t __len__() const
    {
        return self->length();
    }

    const eprosima::test2::StructType2& __getitem__(size_t i) const
    {
        return (*self)[i];
    }
}


// Include the class interfaces
%include "test_included_modules.hpp"

// Include the corresponding TopicDataType
%include "test_included_modulesPubSubTypes.i"

