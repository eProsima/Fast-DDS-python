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
