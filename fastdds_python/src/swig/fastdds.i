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

%module(directors="1", threads="1", moduleimport="if __import__('os').name == 'nt': import win32api; win32api.LoadLibrary('$<TARGET_FILE_NAME:fastdds>')\nif __package__ or '.' in __name__:\n    from . import _fastdds_python\nelse:\n    import _fastdds_python") fastdds

// Handle exceptions on python callbacks and send them back to C++ so that they can be catched
// Also, add some meaningful description of the error
%feature("director:except") {
  if ($error != NULL) {
    PyObject *exc, *val, *tb;
    PyErr_Fetch(&exc, &val, &tb);
    PyErr_NormalizeException(&exc, &val, &tb);
    std::string err_msg("In method '$symname': ");

    PyObject* exc_str = PyObject_GetAttrString(exc, "__name__");
    err_msg += PyUnicode_AsUTF8(exc_str);
    Py_XDECREF(exc_str);

    if (val != NULL)
    {
      PyObject* val_str = PyObject_Str(val);
      err_msg += ": ";
      err_msg += PyUnicode_AsUTF8(val_str);
      Py_XDECREF(val_str);
    }

    Py_XDECREF(exc);
    Py_XDECREF(val);
    Py_XDECREF(tb);

    Swig::DirectorMethodException::raise(err_msg.c_str());
  }
}

// If using windows in debug, it would try to use python_d, which would not be found.
%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
#include <exception>
%}

%exception {
    try { $action }
    catch (Swig::DirectorException &e) { SWIG_fail; }
}

// SWIG helper modules
%include "stdint.i"
%include "std_list.i"
%include "std_string.i"
%include "std_shared_ptr.i"
%include "std_vector.i"
%include "typemaps.i"

%{
#include "fastdds/config.hpp"

bool has_statistics()
{
#ifdef FASTDDS_STATISTICS
  return true;
#else
  return false;
#endif
}
%}

bool has_statistics();

// Some operators are ignored, as there is no such thing in Python.
// Trying to export them issues a warning
%ignore *::operator=;
%ignore *::operator++;
%ignore *::operator!;

// This ensures that the returned string references can be used with the string API
// Otherwise, they will be wrapped objects without API
%typemap(out) std::string& {
  $result = SWIG_From_std_string(*$1);
}

// Keywords that are not fully supported in SWIG
// and make not difference in python anyways
#define final

// Macro delcarations
// Any macro used on the Fast DDS header files will give an error if it is not redefined here
#define eProsima_user_DllExport
#define FASTDDS_EXPORTED_API
#define FASTDDS_DEPRECATED_UNTIL(major, entity_name, msg)
#define FASTDDS_TODO_BEFORE(major, minor, msg)

// Defined template for std::vector<std::string>
%template(StringVector) std::vector<std::string>;

// Predeclaration of namespaces and/or classes not exported to the target language,
// but that are part of the Fast DDS public API
// SWIG will make an empty wrapper around these, but still needs to know they exists
// or the wrapper will fail compilation
namespace eprosima {
namespace fastdds {
namespace dds{
namespace builtin {

    // Just declaring the namespace

} // namespace builtin

namespace xtypes {

    // Just declaring the namespace

} // namespace xtypes
} // namespace dds
} // namespace fastdds
} // namespace eprosima

// Definition of the API exported to the binding.
// The order of appearance in this list matters.
// For example, base classes **MUST** be included before its derived classes.
// Failing to do so will issue a warning, but will not stop the compilation.
// However, the resulting derived class will **not** be considered as inheriting from the base class

#ifndef FASTDDS_DOCS_BUILD
%include <fastcdr/config.h>
%include "fastcdr/xcdr/optional.i"
%include "fastcdr/cdr/fixed_size_string.i"
#endif

%include "fastdds/LibrarySettings.i"
%include "fastdds/rtps/common/VendorId_t.i"
%include "fastdds/rtps/common/Types.i"
%include "fastdds/rtps/common/Time_t.i"
%include "fastdds/rtps/common/Locator.i"
%include "fastdds/rtps/common/LocatorList.i"
%include "fastdds/rtps/common/BinaryProperty.i"
%include "fastdds/rtps/common/Property.i"
%include "fastdds/rtps/common/EntityId_t.i"
%include "fastdds/rtps/common/GuidPrefix_t.i"
%include "fastdds/rtps/common/Guid.i"
%include "fastdds/rtps/common/PortParameters.i"
%include "fastdds/rtps/common/InstanceHandle.i"
%include "fastdds/utils/collections/ResourceLimitedContainerConfig.i"
%include "fastdds/utils/collections/ResourceLimitedVector.i"
%include "fastdds/rtps/attributes/ResourceManagement.i"
%include "fastdds/rtps/attributes/RTPSParticipantAllocationAttributes.i"
%include "fastdds/rtps/attributes/ThreadSettings.i"
%include "fastdds/rtps/flowcontrol/FlowControllerSchedulerPolicy.i"
%include "fastdds/rtps/flowcontrol/FlowControllerDescriptor.i"
%include "fastdds/rtps/attributes/BuiltinTransports.i"
%include "fastdds/rtps/attributes/PropertyPolicy.i"
%include "fastdds/rtps/attributes/RTPSParticipantAttributes.i"
%include "fastdds/rtps/attributes/ReaderAttributes.i"
%include "fastdds/rtps/attributes/WriterAttributes.i"
%include "fastdds/rtps/common/RemoteLocators.i"
%include "fastdds/rtps/common/SequenceNumber.i"
%include "fastdds/rtps/common/SampleIdentity.i"
%include "fastdds/rtps/common/WriteParams.i"
%include "fastdds/rtps/builtin/data/ContentFilterProperty.i"
%include "fastdds/rtps/reader/ReaderDiscoveryInfo.i"
%include "fastdds/rtps/writer/WriterDiscoveryInfo.i"
%include "fastdds/rtps/participant/ParticipantDiscoveryInfo.i"

%include "fastdds/dds/common/InstanceHandle.i"
%include "fastdds/dds/core/ReturnCode.i"
%include "fastdds/dds/core/status/StatusMask.i"
%include "fastdds/dds/core/policy/ParameterTypes.i"
%include "fastdds/dds/core/policy/QosPolicies.i"
%include "fastdds/dds/core/Time_t.i"
%include "fastdds/dds/topic/IContentFilter.i"
%include "fastdds/dds/topic/TopicDataType.i"
%include "fastdds/dds/topic/IContentFilterFactory.i"
%include "fastdds/dds/topic/TypeSupport.i"
%include "fastdds/dds/builtin/topic/BuiltinTopicKey.i"
%include "fastdds/dds/builtin/topic/ParticipantBuiltinTopicData.i"
%include "fastdds/dds/builtin/topic/SubscriptionBuiltinTopicData.i"
%include "fastdds/dds/builtin/topic/PublicationBuiltinTopicData.i"
%include "fastdds/dds/core/condition/Condition.i"
%include "fastdds/dds/core/Entity.i"
%include "fastdds/dds/core/condition/WaitSet.i"
%include "fastdds/dds/core/LoanableTypedCollection.i"
%include "fastdds/dds/core/StackAllocatedSequence.i"
%include "fastdds/dds/core/LoanableCollection.i"
%include "fastdds/dds/core/UserAllocatedSequence.i"
%include "fastdds/dds/core/LoanableSequence.i"
%include "fastdds/dds/core/LoanableArray.i"
%include "fastdds/dds/core/Types.i"
%include "fastdds/dds/core/policy/ReaderDataLifecycleQosPolicy.i"
%include "fastdds/dds/core/policy/ReaderResourceLimitsQos.i"
%include "fastdds/dds/core/policy/RTPSReliableReaderQos.i"
%include "fastdds/dds/core/policy/RTPSReliableWriterQos.i"
%include "fastdds/dds/core/policy/WriterDataLifecycleQosPolicy.i"
%include "fastdds/dds/core/status/LivelinessChangedStatus.i"
%include "fastdds/dds/core/status/MatchedStatus.i"
%include "fastdds/dds/core/status/SubscriptionMatchedStatus.i"
%include "fastdds/dds/core/status/BaseStatus.i"
%include "fastdds/dds/core/status/IncompatibleQosStatus.i"
%include "fastdds/dds/core/status/DeadlineMissedStatus.i"
%include "fastdds/dds/core/status/SampleRejectedStatus.i"
%include "fastdds/dds/core/status/PublicationMatchedStatus.i"
%include "fastdds/dds/topic/qos/TopicQos.i"
%include "fastdds/dds/topic/TopicDescription.i"
%include "fastdds/dds/topic/Topic.i"
%include "fastdds/dds/topic/ContentFilteredTopic.i"
%include "fastdds/dds/topic/TopicListener.i"
%include "fastdds/dds/subscriber/qos/ReaderQos.i"
%include "fastdds/dds/subscriber/qos/SubscriberQos.i"
%include "fastdds/dds/subscriber/qos/DataReaderQos.i"
%include "fastdds/dds/subscriber/DataReaderListener.i"
%include "fastdds/dds/subscriber/SubscriberListener.i"
%include "fastdds/dds/subscriber/ViewState.i"
%include "fastdds/dds/subscriber/SampleState.i"
%include "fastdds/dds/subscriber/InstanceState.i"
%include "fastdds/dds/subscriber/SampleInfo.i"
%include "fastdds/dds/subscriber/DataReader.i"
%include "fastdds/dds/subscriber/Subscriber.i"
%include "fastdds/dds/publisher/qos/PublisherQos.i"
%include "fastdds/dds/publisher/qos/WriterQos.i"
%include "fastdds/dds/publisher/qos/DataWriterQos.i"
%include "fastdds/dds/publisher/DataWriterListener.i"
%include "fastdds/dds/publisher/PublisherListener.i"
%include "fastdds/dds/publisher/DataWriter.i"
%include "fastdds/dds/publisher/Publisher.i"
%include "fastdds/dds/domain/DomainParticipantListener.i"
%include "fastdds/dds/domain/qos/DomainParticipantFactoryQos.i"
%include "fastdds/dds/domain/qos/DomainParticipantQos.i"
%include "fastdds/dds/domain/qos/DomainParticipantExtendedQos.i"
%include "fastdds/dds/domain/qos/ReplierQos.i"
%include "fastdds/dds/domain/qos/RequesterQos.i"
%include "fastdds/dds/domain/DomainParticipant.i"
%include "fastdds/dds/domain/DomainParticipantFactory.i"
%include "fastdds/dds/xtypes/type_representation/TypeObject.i"
