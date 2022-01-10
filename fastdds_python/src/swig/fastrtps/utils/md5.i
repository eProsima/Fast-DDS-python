// SWIG helper modules
%include "std_string.i"

%{
#include "fastrtps/utils/md5.h"
%}

%ignore md5(const std::string);

%include "fastrtps/utils/md5.h"
