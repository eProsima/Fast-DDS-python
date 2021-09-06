%{
#include "fastrtps/types/TypesBase.h"
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
