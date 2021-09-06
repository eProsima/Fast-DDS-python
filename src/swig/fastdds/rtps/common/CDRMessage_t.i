%{
#include "fastdds/rtps/common/CDRMessage_t.h"
%}

// Overloaded constructor ignored
%ignore eprosima::fastrtps::rtps::CDRMessage_t::CDRMessage_t(CDRMessage_t &&);

%include "fastdds/rtps/common/CDRMessage_t.h"
