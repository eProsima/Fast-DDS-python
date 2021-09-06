%module topic_types


// SWIG helper modules
%include "std_string.i"
%include "typemaps.i"

// Assignemt operators are ignored, as there is no such thing in Python.
// Trying to export them issues a warning
%ignore *::operator=;

// Definition of internal types
typedef unsigned int uint32_t;

// Macro delcarations
// Any macro used on the Fast DDS header files will give an error if it is not redefined here
#define RTPS_DllAPI

class HelloWorld;
class HelloWorldTopicDataType;

namespace foo {

class Foo;

namespace bar {

class Bar;

} // namespace bar
} // namespace foo

%include "HelloWorld/HelloWorld.i"
%include "HelloWorld/HelloWorldTopicDataType.i"
%include "FooBar/Foo.i"
%include "FooBar/Bar.i"
