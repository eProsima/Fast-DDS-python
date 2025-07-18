// Copyright 2025 Proyectos y Sistemas de Mantenimiento SL (eProsima).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

%{
#include "fastdds/dds/rpc/exceptions.hpp"
%}

// Base class should be included first
%include "fastdds/dds/rpc/exceptions/RpcException.hpp"
// Include first level inheritance
%include "fastdds/dds/rpc/exceptions/RpcBrokenPipeException.hpp"
%include "fastdds/dds/rpc/exceptions/RpcFeedCancelledException.hpp"
%include "fastdds/dds/rpc/exceptions/RpcOperationError.hpp"
%include "fastdds/dds/rpc/exceptions/RpcTimeoutException.hpp"
// This is the base class for second level inheritance
%include "fastdds/dds/rpc/RemoteExceptionCode_t.hpp"
%include "fastdds/dds/rpc/exceptions/RpcRemoteException.hpp"
// Include second level inheritance
%include "fastdds/dds/rpc/exceptions/RemoteInvalidArgumentError.hpp"
%include "fastdds/dds/rpc/exceptions/RemoteOutOfResourcesError.hpp"
%include "fastdds/dds/rpc/exceptions/RemoteUnknownExceptionError.hpp"
%include "fastdds/dds/rpc/exceptions/RemoteUnknownOperationError.hpp"
%include "fastdds/dds/rpc/exceptions/RemoteUnsupportedError.hpp"
