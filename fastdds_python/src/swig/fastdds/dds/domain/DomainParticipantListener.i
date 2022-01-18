%{
#include "fastdds/dds/domain/DomainParticipantListener.hpp"
%}

// generate directors for the virtual methods in the listener
%feature("director") eprosima::fastdds::dds::DomainParticipantListener;

%include "fastdds/dds/domain/DomainParticipantListener.hpp"
