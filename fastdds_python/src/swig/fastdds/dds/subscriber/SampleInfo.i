%{
#include "fastdds/dds/subscriber/SampleInfo.hpp"
%}

%ignore eprosima::fastdds::dds::READ;
%ignore eprosima::fastdds::dds::NOT_READ;
%ignore eprosima::fastdds::dds::NEW;
%ignore eprosima::fastdds::dds::NOT_NEW;
%ignore eprosima::fastdds::dds::ALIVE;
%ignore eprosima::fastdds::dds::NOT_ALIVE_DISPOSED;
%ignore eprosima::fastdds::dds::NOT_ALIVE_NO_WRITERS;

%include "fastdds/dds/subscriber/SampleInfo.hpp"
