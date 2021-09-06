%{
#include "FooBar/Bar.h"
%}

%include "FooBar/Bar.h"


%{
    void print_foo (foo::Foo* f)
    {
        f->print();
        f->set_v(0);
    }
%}

void print_foo(foo::Foo* f);
