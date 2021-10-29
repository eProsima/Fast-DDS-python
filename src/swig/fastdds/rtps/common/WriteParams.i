%{
#include "fastdds/rtps/common/WriteParams.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::WriteParams::WriteParams(WriteParams &&);
%ignore eprosima::fastrtps::rtps::WriteParams::sample_identity(SampleIdentity &&);
%ignore eprosima::fastrtps::rtps::WriteParams::related_sample_identity(SampleIdentity &&);

%include "fastdds/rtps/common/WriteParams.h"
