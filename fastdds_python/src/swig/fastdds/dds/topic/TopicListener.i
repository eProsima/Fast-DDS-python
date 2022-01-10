%{
#include "fastdds/dds/topic/TopicListener.hpp"
%}

// generate directors for the virtual methods in the listener
%feature("director") eprosima::fastdds::dds::TopicListener;

%include "fastdds/dds/topic/TopicListener.hpp"
