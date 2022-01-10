%{
#include "fastdds/dds/core/status/StatusMask.hpp"
%}

// This class is defined as a subclass of std::bitset<size_t(16)>
// However, SWIG choked parsing this, but could parse std::bitset<16>
// Furthermore, SWIG does not have any wrapper for std::bitset
//  - We create a workaround defining sizet(16)=16
//  - We ignore the warning about not knowing bitset.
// This will only affect in that the resulting class cannot be used in a polymorphic way, but we so not need it.
#define size_t(n) n
%warnfilter(401) eprosima::fastdds::dds::StatusMask;

%include "fastdds/dds/core/status/StatusMask.hpp"

#undef size_t(n)
