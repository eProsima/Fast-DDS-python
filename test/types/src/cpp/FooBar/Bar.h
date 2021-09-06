#ifndef __BAR_H__
#define __BAR_H__

#include "Foo.h"

namespace foo {
namespace bar {

class Bar : public Foo
{
public:
    Bar();
    void print() const;
};

} // namespace bar
} // namespace foo

#endif // __BAR_H__