%{
#include "fastrtps/utils/fixed_size_string.hpp"
%}

// Ignore method that causes warnings on SWIG
%ignore eprosima::fastrtps::fixed_string::operator const char*() const;

%include "fastrtps/utils/fixed_size_string.hpp"

%template(fixed_string_255) eprosima::fastrtps::fixed_string<255>;

%extend eprosima::fastrtps::fixed_string {

    std::string __str__() const
    {
        return $self->to_string();
    }
}

