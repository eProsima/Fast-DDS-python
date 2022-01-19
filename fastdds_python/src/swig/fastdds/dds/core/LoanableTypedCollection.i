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
#include "fastdds/dds/core/LoanableTypedCollection.hpp"
%}

// Operator[] is ignored by SWIG because it does not map correctly to target languages
// mostly because of its dual getter/setter nature
// We can ignore them and extend to make the getter and setter methods explicit and break the overload
%ignore eprosima::fastdds::dds::LoanableTypedCollection::operator[];

%include "fastdds/dds/core/LoanableTypedCollection.hpp"

%extend eprosima::fastdds::dds::LoanableTypedCollection {
  T getitem(size_type n) {
      return $self->operator[](n);
  }

  void setitem(size_type n, const T& v) {
      $self->operator[](n) = v;
  }
}
