%{
#include "fastdds/dds/subscriber/SubscriberListener.hpp"
%}

// generate directors for the virtual methods in the listener
%feature("director") eprosima::fastdds::dds::SubscriberListener;

%include "fastdds/dds/subscriber/SubscriberListener.hpp"
