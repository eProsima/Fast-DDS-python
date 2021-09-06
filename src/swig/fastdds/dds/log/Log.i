%{
#include "fastdds/dds/log/Log.hpp"
%}

// Ignore nested structs, as they are not supported by SWIG
%ignore eprosima::fastdds::dds::Log::Context;
%ignore eprosima::fastdds::dds::Log::Entry;

// Ignore also the public methods that need these structs as input
// as they will be unusable, since we cannot instantiate any object of the ignored classes
%ignore eprosima::fastdds::dds::Log::QueueLog;

%include "fastdds/dds/log/Log.hpp"
