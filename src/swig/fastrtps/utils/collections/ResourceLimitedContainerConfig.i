%{
#include "fastrtps/utils/collections/ResourceLimitedContainerConfig.hpp"
%}

// SWIG does not support parsing this default argument:
//    size_t max = (std::numeric_limits<size_t>::max)()
// This issues a parsing error and stops SWIG
// We are forced to reimplement the interface here
// Due to the way SWIG creates the wrapper, the default values can be substituted by any value
// since the wrapper will not use them anywhere,
// they are used only to detect when arguments are optional

namespace eprosima {
namespace fastrtps {

struct ResourceLimitedContainerConfig
{

    ResourceLimitedContainerConfig(
            size_t ini = 0,
            size_t max = 0,
            size_t inc = 1u)
        : initial(ini)
        , maximum(max)
        , increment(inc);
    inline static ResourceLimitedContainerConfig fixed_size_configuration(
            size_t size);

    inline static ResourceLimitedContainerConfig dynamic_allocation_configuration(
            size_t increment = 1u);

    size_t initial;
    size_t maximum;
    size_t increment;

};

inline bool operator == (
        const ResourceLimitedContainerConfig& lhs,
        const ResourceLimitedContainerConfig& rhs);

}  // namespace fastrtps
}  // namespace eprosima

//%include "fastrtps/utils/collections/ResourceLimitedContainerConfig.hpp"

// This class has a global comparison operator that will be ignored by general rules.
// Extend it with an internal operator
%extend eprosima::fastrtps::ResourceLimitedContainerConfig {
    bool operator ==(
                const eprosima::fastrtps::ResourceLimitedContainerConfig& b) const
        {
            return ($self->initial == b.initial) &&
                ($self->maximum == b.maximum) &&
                ($self->increment == b.increment);
        }
}
