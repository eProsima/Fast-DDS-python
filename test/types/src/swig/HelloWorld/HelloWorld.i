%{
#include "HelloWorld/HelloWorld.h"
%}

// Ignore overloaded methods that have no application on Python
// Otherwise they will issue a warning
%ignore HelloWorld::HelloWorld(HelloWorld&&);

// field getter-setter methods do not map correctly to target languages
// We better ignore it and extend to make the getter and setter methods explicit and break the overload
%ignore HelloWorld::index;
%ignore HelloWorld::message;

%include "HelloWorld/HelloWorld.h"

%extend HelloWorld {
  uint32_t get_index() const {
      return $self->index();
  }

  void set_index(const uint32_t& v) {
      $self->index(v);
  }

  const std::string& get_message() const {
      return $self->message();
  }

  void set_message(const std::string& v) {
      $self->message(v);
  }
}
