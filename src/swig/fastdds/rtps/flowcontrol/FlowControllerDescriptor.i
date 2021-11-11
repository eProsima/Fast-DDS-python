// This class contains a 'const char*' member that may leak on destruction
// However, converting it to a 'shar*' does not
// SWIG is very special)
%typemap(out) char const *name = char *;
%typemap(memberin) char const *name = char *;

%{
#include "fastdds/rtps/flowcontrol/FlowControllerDescriptor.hpp"
%}

%include "fastdds/rtps/flowcontrol/FlowControllerDescriptor.hpp"

// Undo the mapping for future classes
%typemap(out) char const *name;
%typemap(memberin) char const *name;