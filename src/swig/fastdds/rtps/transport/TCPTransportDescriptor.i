%{
#include "fastdds/rtps/transport/TCPTransportDescriptor.h"
%}

// Flatten nested classes
%feature("flatnested", "1");

// Need to create a custom name for the flattened classes
// since other classes also define the same inner class
%rename (TCPTransportDescriptor_TLSConfig) eprosima::fastdds::rtps::TCPTransportDescriptor::TLSConfig;
%rename (TCPTransportDescriptor_TLSConfig_TLSOptions) eprosima::fastdds::rtps::TCPTransportDescriptor::TLSConfig::TLSOptions;
%rename (TCPTransportDescriptor_TLSConfig_TLSVerifyMode) eprosima::fastdds::rtps::TCPTransportDescriptor::TLSConfig::TLSVerifyMode;
%rename (TCPTransportDescriptor_TLSConfig_TLSHandShakeRole) eprosima::fastdds::rtps::TCPTransportDescriptor::TLSConfig::TLSHandShakeRole;

%include "fastdds/rtps/transport/TCPTransportDescriptor.h"

// Deactivate class flattening
%feature("flatnested", "0");
