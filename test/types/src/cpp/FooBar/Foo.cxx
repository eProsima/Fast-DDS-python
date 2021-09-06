#include "Foo.h"

using namespace foo;

Foo::Foo() : v(0) {}
int Foo::get_v() const { return v; }
void Foo::set_v(int value) { v = value; }
