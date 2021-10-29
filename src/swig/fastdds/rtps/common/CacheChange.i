%{
#include "fastdds/rtps/common/CacheChange.h"
%}

// Ignore problematic classes that are not part of the user API
%ignore eprosima::fastrtps::rtps::CacheChangeWriterInfo_t;
%ignore eprosima::fastrtps::rtps::CacheChangeReaderInfo_t;

%include "fastdds/rtps/common/CacheChange.h"
