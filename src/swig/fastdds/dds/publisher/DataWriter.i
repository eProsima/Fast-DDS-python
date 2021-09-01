%{
#include "fastdds/dds/publisher/DataWriter.hpp"
%}


// Ignore unimplemented method (the wrapper will try to use it)
%ignore eprosima::fastdds::dds::DataWriter::dispose_w_timestamp;

%include "fastdds/dds/publisher/DataWriter.hpp"
