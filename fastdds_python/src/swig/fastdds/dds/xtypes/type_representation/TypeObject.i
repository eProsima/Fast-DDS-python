// Copyright 2024 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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
#include "fastdds/dds/xtypes/type_representation/detail/dds_xtypes_typeobject.hpp"
%}

%ignore eprosima::fastdds::dds::xtypes::TypeObjectHashId;
%ignore eprosima::fastdds::dds::xtypes::StringSTypeDefn;
%ignore eprosima::fastdds::dds::xtypes::StringLTypeDefn;
%ignore eprosima::fastdds::dds::xtypes::PlainCollectionHeader;
%ignore eprosima::fastdds::dds::xtypes::PlainSequenceSElemDefn;
%ignore eprosima::fastdds::dds::xtypes::PlainSequenceLElemDefn;
%ignore eprosima::fastdds::dds::xtypes::PlainArraySElemDefn;
%ignore eprosima::fastdds::dds::xtypes::PlainArrayLElemDefn;
%ignore eprosima::fastdds::dds::xtypes::PlainMapSTypeDefn;
%ignore eprosima::fastdds::dds::xtypes::PlainMapLTypeDefn;
%ignore eprosima::fastdds::dds::xtypes::StronglyConnectedComponentId;
%ignore eprosima::fastdds::dds::xtypes::ExtendedTypeDefn;
%ignore eprosima::fastdds::dds::xtypes::TypeIdentifier;
%ignore eprosima::fastdds::dds::xtypes::ExtendedAnnotationParameterValue;
%ignore eprosima::fastdds::dds::xtypes::AnnotationParameterValue;
%ignore eprosima::fastdds::dds::xtypes::AppliedAnnotationParameter;
%ignore eprosima::fastdds::dds::xtypes::AppliedAnnotation;
%ignore eprosima::fastdds::dds::xtypes::AppliedVerbatimAnnotation;
%ignore eprosima::fastdds::dds::xtypes::AppliedBuiltinMemberAnnotations;
%ignore eprosima::fastdds::dds::xtypes::CommonStructMember;
%ignore eprosima::fastdds::dds::xtypes::CompleteMemberDetail;
%ignore eprosima::fastdds::dds::xtypes::MinimalMemberDetail;
%ignore eprosima::fastdds::dds::xtypes::CompleteStructMember;
%ignore eprosima::fastdds::dds::xtypes::MinimalStructMember;
%ignore eprosima::fastdds::dds::xtypes::AppliedBuiltinTypeAnnotations;
%ignore eprosima::fastdds::dds::xtypes::MinimalTypeDetail;
%ignore eprosima::fastdds::dds::xtypes::CompleteTypeDetail;
%ignore eprosima::fastdds::dds::xtypes::CompleteStructHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalStructHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteStructType;
%ignore eprosima::fastdds::dds::xtypes::MinimalStructType;
%ignore eprosima::fastdds::dds::xtypes::CommonUnionMember;
%ignore eprosima::fastdds::dds::xtypes::CompleteUnionMember;
%ignore eprosima::fastdds::dds::xtypes::MinimalUnionMember;
%ignore eprosima::fastdds::dds::xtypes::CommonDiscriminatorMember;
%ignore eprosima::fastdds::dds::xtypes::CompleteDiscriminatorMember;
%ignore eprosima::fastdds::dds::xtypes::MinimalDiscriminatorMember;
%ignore eprosima::fastdds::dds::xtypes::CompleteUnionHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalUnionHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteUnionType;
%ignore eprosima::fastdds::dds::xtypes::MinimalUnionType;
%ignore eprosima::fastdds::dds::xtypes::CommonAnnotationParameter;
%ignore eprosima::fastdds::dds::xtypes::CompleteAnnotationParameter;
%ignore eprosima::fastdds::dds::xtypes::MinimalAnnotationParameter;
%ignore eprosima::fastdds::dds::xtypes::CompleteAnnotationHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalAnnotationHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteAnnotationType;
%ignore eprosima::fastdds::dds::xtypes::MinimalAnnotationType;
%ignore eprosima::fastdds::dds::xtypes::CommonAliasBody;
%ignore eprosima::fastdds::dds::xtypes::CompleteAliasBody;
%ignore eprosima::fastdds::dds::xtypes::MinimalAliasBody;
%ignore eprosima::fastdds::dds::xtypes::CompleteAliasHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalAliasHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteAliasType;
%ignore eprosima::fastdds::dds::xtypes::MinimalAliasType;
%ignore eprosima::fastdds::dds::xtypes::CompleteElementDetail;
%ignore eprosima::fastdds::dds::xtypes::CommonCollectionElement;
%ignore eprosima::fastdds::dds::xtypes::CompleteCollectionElement;
%ignore eprosima::fastdds::dds::xtypes::MinimalCollectionElement;
%ignore eprosima::fastdds::dds::xtypes::CommonCollectionHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteCollectionHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalCollectionHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteSequenceType;
%ignore eprosima::fastdds::dds::xtypes::MinimalSequenceType;
%ignore eprosima::fastdds::dds::xtypes::CommonArrayHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteArrayHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalArrayHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteArrayType;
%ignore eprosima::fastdds::dds::xtypes::MinimalArrayType;
%ignore eprosima::fastdds::dds::xtypes::CompleteMapType;
%ignore eprosima::fastdds::dds::xtypes::MinimalMapType;
%ignore eprosima::fastdds::dds::xtypes::CommonEnumeratedLiteral;
%ignore eprosima::fastdds::dds::xtypes::CompleteEnumeratedLiteral;
%ignore eprosima::fastdds::dds::xtypes::MinimalEnumeratedLiteral;
%ignore eprosima::fastdds::dds::xtypes::CommonEnumeratedHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteEnumeratedHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalEnumeratedHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteEnumeratedType;
%ignore eprosima::fastdds::dds::xtypes::MinimalEnumeratedType;
%ignore eprosima::fastdds::dds::xtypes::CommonBitflag;
%ignore eprosima::fastdds::dds::xtypes::CompleteBitflag;
%ignore eprosima::fastdds::dds::xtypes::MinimalBitflag;
%ignore eprosima::fastdds::dds::xtypes::CommonBitmaskHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteBitmaskType;
%ignore eprosima::fastdds::dds::xtypes::MinimalBitmaskType;
%ignore eprosima::fastdds::dds::xtypes::CommonBitfield;
%ignore eprosima::fastdds::dds::xtypes::CompleteBitfield;
%ignore eprosima::fastdds::dds::xtypes::MinimalBitfield;
%ignore eprosima::fastdds::dds::xtypes::CompleteBitsetHeader;
%ignore eprosima::fastdds::dds::xtypes::MinimalBitsetHeader;
%ignore eprosima::fastdds::dds::xtypes::CompleteBitsetType;
%ignore eprosima::fastdds::dds::xtypes::MinimalBitsetType;
%ignore eprosima::fastdds::dds::xtypes::CompleteExtendedType;
%ignore eprosima::fastdds::dds::xtypes::CompleteTypeObject;
%ignore eprosima::fastdds::dds::xtypes::MinimalExtendedType;
%ignore eprosima::fastdds::dds::xtypes::MinimalTypeObject;
%ignore eprosima::fastdds::dds::xtypes::TypeObject;
%ignore eprosima::fastdds::dds::xtypes::TypeIdentifierTypeObjectPair;
%ignore eprosima::fastdds::dds::xtypes::TypeIdentifierPair;
%ignore eprosima::fastdds::dds::xtypes::TypeIdentfierWithSize;
%ignore eprosima::fastdds::dds::xtypes::TypeIdentifierWithDependencies;
%ignore eprosima::fastdds::dds::xtypes::TypeInformation::TypeInformation(TypeInformation&&);
%ignore eprosima::fastdds::dds::xtypes::TypeInformation::minimal;
%ignore eprosima::fastdds::dds::xtypes::TypeInformation::complete;

%include "fastdds/dds/xtypes/type_representation/detail/dds_xtypes_typeobject.hpp"
