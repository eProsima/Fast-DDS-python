#ifndef __FOO_H__
#define __FOO_H__

namespace foo {
class Foo
{
public:
    Foo();
    virtual ~Foo() = default;
    int get_v() const;
    void set_v(int value);
    virtual void print() const = 0;

protected:
    int v;
};

} // namespace foo
#endif // __FOO_H__