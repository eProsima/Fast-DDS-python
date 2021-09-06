#include "Bar.h"
#include <iostream>

using namespace foo;
using namespace foo::bar;

Bar::Bar() : Foo() {}
void Bar::print() const { std::cout << "BAR: " << get_v() << std::endl; }