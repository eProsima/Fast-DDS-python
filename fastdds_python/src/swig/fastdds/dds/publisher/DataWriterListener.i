%{
#include "fastdds/dds/publisher/DataWriterListener.hpp"
%}

// generate directors for the virtual methods in the listener
%feature("director") eprosima::fastdds::dds::DataWriterListener;

%include "fastdds/dds/publisher/DataWriterListener.hpp"
