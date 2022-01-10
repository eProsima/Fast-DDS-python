%{
#include "fastdds/dds/subscriber/DataReaderListener.hpp"
%}

// generate directors for the virtual methods in the listener
%feature("director") eprosima::fastdds::dds::DataReaderListener;

%include "fastdds/dds/subscriber/DataReaderListener.hpp"
