%{
#include "fastdds/rtps/common/SampleIdentity.h"
%}

// Ignore overloaded constructor and methods that have no effect on target language
%ignore eprosima::fastrtps::rtps::SampleIdentity::SampleIdentity(SampleIdentity &&);
%ignore eprosima::fastrtps::rtps::SampleIdentity::writer_guid(GUID_t &&);
%ignore eprosima::fastrtps::rtps::SampleIdentity::sequence_number(SequenceNumber_t &&);

// Ignore private methods that cannot be wrapped
%ignore operator >>(std::istream& input, SampleIdentity& sid);
%ignore operator <<(std::ostream& output, const SampleIdentity& sid);

%include "fastdds/rtps/common/SampleIdentity.h"
