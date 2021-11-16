%{
#include "fastdds/rtps/common/SequenceNumber.h"
%}

%include "fastdds/rtps/common/SequenceNumber.h"

// Declare the comparison operators as internal to the class
%extend eprosima::fastrtps::rtps::SequenceNumber_t {
    bool operator==(const eprosima::fastrtps::rtps::SequenceNumber_t& other) const
    {
        return *$self == other;
    }

    bool operator!=(const eprosima::fastrtps::rtps::SequenceNumber_t& other) const
    {
        return *$self != other;
    }

    bool operator<(const eprosima::fastrtps::rtps::SequenceNumber_t& other) const
    {
        return *$self < other;
    }

    bool operator>(const eprosima::fastrtps::rtps::SequenceNumber_t& other) const
    {
        return *$self > other;
    }

    bool operator<=(const eprosima::fastrtps::rtps::SequenceNumber_t& other) const
    {
        return *$self <= other;
    }

    bool operator>=(const eprosima::fastrtps::rtps::SequenceNumber_t& other) const
    {
        return *$self >= other;
    }

    std::string __str__() const
    {
        std::ostringstream out;
        out << *$self;
        return out.str();
    }
}
