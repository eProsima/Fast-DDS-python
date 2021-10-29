%{
#include "fastdds/rtps/common/Locator.h"
%}

// Ignore overloaded constructor that have no effect on target language
%ignore eprosima::fastrtps::rtps::Locator_t::Locator_t(Locator_t &&);

%include "fastdds/rtps/common/Locator.h"
