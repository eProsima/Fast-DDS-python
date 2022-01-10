%{
#include "fastdds/dds/topic/IContentFilter.hpp"
%}

// Flatten nested classes
%feature("flatnested", "1");

%include "fastdds/dds/topic/IContentFilter.hpp"

// Deactivate class flattening
%feature("flatnested", "0");
