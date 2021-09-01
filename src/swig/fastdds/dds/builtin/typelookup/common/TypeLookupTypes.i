%{
#include "fastdds/dds/builtin/typelookup/common/TypeLookupTypes.hpp"
%}

// Avoid creating the default constructor for abstract types
%nodefaultctor eprosima::fastdds::dds::builtin::TypeLookup_RequestPubSubType;  // Pure virtual
%ignore eprosima::fastdds::dds::builtin::TypeLookup_RequestPubSubType::TypeLookup_RequestPubSubType;

%nodefaultctor eprosima::fastdds::dds::builtin::TypeLookup_ReplyPubSubType;  // Pure virtual
%ignore eprosima::fastdds::dds::builtin::TypeLookup_ReplyPubSubType::TypeLookup_ReplyPubSubType;

// Igonre overloaded methods that have no application on Python
// Otherwise they will issue a warning
%ignore eprosima::fastdds::dds::builtin::TypeLookup_getTypes_Result::TypeLookup_getTypes_Result(TypeLookup_getTypes_Result&&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_getTypes_Result::result(TypeLookup_getTypes_Out &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_getTypes_Result::_d() const;

%ignore eprosima::fastdds::dds::builtin::TypeLookup_getTypeDependencies_Result::TypeLookup_getTypeDependencies_Result(TypeLookup_getTypeDependencies_Result &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_getTypeDependencies_Result::result(TypeLookup_getTypeDependencies_Out &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_getTypeDependencies_Result::_d() const;

%ignore eprosima::fastdds::dds::builtin::TypeLookup_Call::TypeLookup_Call(TypeLookup_Call &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Call::result(TypeLookup_getTypeDependencies_Out &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Call::getTypes(TypeLookup_getTypes_In &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Call::getTypeDependencies(TypeLookup_getTypeDependencies_In &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Call::_d() const;

%ignore eprosima::fastdds::dds::builtin::TypeLookup_Return::TypeLookup_Return(TypeLookup_Return &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Return::getType(TypeLookup_getTypes_Result &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Return::getTypeDependencies(TypeLookup_getTypeDependencies_Result &&);
%ignore eprosima::fastdds::dds::builtin::TypeLookup_Return::_d() const;

%include "fastdds/dds/builtin/typelookup/common/TypeLookupTypes.hpp"
