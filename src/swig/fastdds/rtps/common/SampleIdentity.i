%{
#include "fastdds/rtps/common/SampleIdentity.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::SampleIdentity::SampleIdentity(SampleIdentity &&);
%ignore eprosima::fastrtps::rtps::SampleIdentity::writer_guid(GUID_t &&);
%ignore eprosima::fastrtps::rtps::SampleIdentity::sequence_number(SequenceNumber_t &&);

%include "fastdds/rtps/common/SampleIdentity.h"
