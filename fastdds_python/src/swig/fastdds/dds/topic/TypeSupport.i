%{
#include "fastdds/dds/topic/TypeSupport.hpp"
%}

// SWIG does not support templates in the generated binding,
// because not all output languages support them
// We must explicitly declare the specializations of the templates
%template(TopicDataTypeShrPtr) std::shared_ptr<eprosima::fastdds::dds::TopicDataType>;

// Ignore overloaded method that has no application in python
// Otherwise it will issue a warning
%ignore eprosima::fastdds::dds::TypeSupport::TypeSupport(TypeSupport &&);

// This constructor takes ownership of the TopicDataType pointer
// We need SWIG to be aware of it, so we ignore it here and redefine it later
%ignore eprosima::fastdds::dds::TypeSupport::TypeSupport(fastdds::dds::TopicDataType*);


%include "fastdds/dds/topic/TypeSupport.hpp"

// To make SWIG aware of the loss of the ownership, use the DISOWN typemap
// Do not worry about the heap allocation, SWIG recognizes the method as a constructor
// and successfully deallocates on destruction
%extend eprosima::fastdds::dds::TypeSupport {
    %apply SWIGTYPE *DISOWN { eprosima::fastdds::dds::TopicDataType* ptr };
    TypeSupport(eprosima::fastdds::dds::TopicDataType* ptr)
    {
        return new eprosima::fastdds::dds::TypeSupport(ptr);
    }
}
