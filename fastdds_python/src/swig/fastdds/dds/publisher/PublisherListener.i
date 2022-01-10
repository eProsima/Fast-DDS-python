%{
#include "fastdds/dds/publisher/PublisherListener.hpp"
%}

// generate directors for the virtual methods in the listener
%feature("director") eprosima::fastdds::dds::PublisherListener;

%include "fastdds/dds/publisher/PublisherListener.hpp"
