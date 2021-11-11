// This class contains a 'const char*' member that may leak on destruction
// However, converting it to a 'shar*' does not
// SWIG is very special)
%typemap(out) char const *flow_controller_name = char *;
%typemap(memberin) char const *flow_controller_name = char *;

%{
#include "fastdds/rtps/attributes/WriterAttributes.h"
%}

%include "fastdds/rtps/attributes/WriterAttributes.h"

// Undo the mapping for future classes
%typemap(out) char const *flow_controller_name;
%typemap(memberin) char const *flow_controller_name;