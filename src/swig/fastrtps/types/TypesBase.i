%{
#include "fastrtps/types/TypesBase.h"
#include <sstream>
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(OctetSeq) std::vector<eprosima::fastrtps::rtps::octet>;

// Although explicitly deleted, SWIG still tries to create this method
%ignore eprosima::fastrtps::types::ReturnCode_t::operator bool;

// Ignore overloaded constructors
%ignore eprosima::fastrtps::types::MemberFlag::MemberFlag(MemberFlag &&);
%ignore eprosima::fastrtps::types::TypeFlag::TypeFlag(TypeFlag &&);

%include "fastrtps/types/TypesBase.h"

%extend eprosima::fastrtps::types::ReturnCode_t {
    std::string __str__() const
    {
        std::ostringstream out;
        out << (*$self)();
        return out.str();
    }
    
    bool operator==(eprosima::fastrtps::types::ReturnCode_t::ReturnCodeValue value) const
    {
        return *$self == value;
    }

    bool operator!=(eprosima::fastrtps::types::ReturnCode_t::ReturnCodeValue value) const
    {
        return *$self != value;
    }
}