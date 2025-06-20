// Copyright 2016 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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

/*!
 * @file calculator.i
 * This header file contains the SWIG interface of the described types in the IDL file.
 *
 * This file was generated by the tool fastddsgen (version: 4.1.0).
 */

%module(threads="1",directors="1",moduleimport="if __import__('os').name == 'nt': import win32api; win32api.LoadLibrary('calculator.dll')\nif __package__ or '.' in __name__:\n    from . import _calculatorWrapper\nelse:\n    import _calculatorWrapper") calculator

// We have enabled threads because the RPC server directors will call the target language environment
// from the C++ server threads, but we don't want the calls from the target language to release their
// locks (e.g. Python GIL) when calling the C++ methods.
// See a very nice explanation at https://github.com/swig/swig/issues/927#issuecomment-289279243
%feature("nothreadallow");

// If using windows in debug, it would try to use python_d, which would not be found.
%begin %{
/*
 * From: https://github.com/swig/swig/issues/2638
 * When a module uses a type in a module that is defined in a different module,
 * a false positive memory leak is detected.
 * The following line silences this warning.
 */
#define SWIG_PYTHON_SILENT_MEMLEAK
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
#include <exception>
%}

// SWIG helper modules
%include "exception.i"
%include "stdint.i"
%include "std_array.i"
%include "std_map.i"
%include "std_pair.i"
%include "std_shared_ptr.i"
%include "std_string.i"
%include "std_vector.i"
%include "typemaps.i"

// Assignemt operators are ignored, as there is no such thing in Python.
// Trying to export them issues a warning
%ignore *::operator=;

// Macro declarations
// Any macro used on the Fast DDS header files will give an error if it is not redefined here
#define FASTDDS_EXPORTED_API
#define eProsima_user_DllExport


%{
#include "calculator.hpp"
#include "calculatorClient.hpp"
#include "calculatorServer.hpp"
#include "calculatorServerImpl.hpp"

#include <fastdds/dds/core/LoanableSequence.hpp>
%}

%include <fastcdr/config.h>
%import(module="fastdds") "fastcdr/xcdr/optional.hpp"
%import(module="fastdds") "fastcdr/cdr/fixed_size_string.hpp"
%import(module="fastdds") "fastdds/dds/core/LoanableCollection.hpp"
%import(module="fastdds") "fastdds/dds/core/LoanableTypedCollection.hpp"
%import(module="fastdds") "fastdds/dds/core/LoanableSequence.hpp"

%import(module="fastdds") "fastdds/dds/rpc/exceptions/RpcException.hpp"
%import(module="fastdds") "fastdds/dds/rpc/exceptions/RpcOperationError.hpp"
%import(module="fastdds") "fastdds/dds/rpc/interfaces/RpcServer.hpp"

%exception {
    try
    {
        $action
    }
    catch (const eprosima::fastdds::dds::rpc::RpcException& ex)
    {
        SWIG_exception(SWIG_RuntimeError, ex.what());
    }
    catch (const std::exception& ex)
    {
        SWIG_exception(SWIG_RuntimeError, ex.what());
    }
    catch (...)
    {
        SWIG_exception(SWIG_RuntimeError,"Unknown exception");
    }
}

%import(module="fastdds") "fastdds/dds/rpc/interfaces/RpcServerWriter.hpp"
%ignore eprosima::fastdds::dds::rpc::RpcClientReader::read(T&);
%ignore eprosima::fastdds::dds::rpc::RpcClientReader::read(T&,eprosima::fastdds::dds::Duration_t&);
%import(module="fastdds") "fastdds/dds/rpc/interfaces/RpcClientReader.hpp"
%extend eprosima::fastdds::dds::rpc::RpcClientReader {
    std::pair<bool, T> read(
        const eprosima::fastdds::dds::Duration_t& timeout = eprosima::fastdds::dds::c_TimeInfinite)
    {
        std::pair<bool, T> ret_val{};
        if (eprosima::fastdds::dds::c_TimeInfinite == timeout)
        {
            ret_val.first = self->read(ret_val.second);
        }
        else
        {
            ret_val.first = self->read(ret_val.second, timeout);
        }
        return ret_val;
    }
}

%shared_ptr(eprosima::fastdds::dds::rpc::RpcClientReader<int32_t>);
%template(int32_t_client_reader_result) std::pair<bool, int32_t>;
%template(int32_t_client_reader) eprosima::fastdds::dds::rpc::RpcClientReader<int32_t>;

%template(int32_t_server_writer) eprosima::fastdds::dds::rpc::RpcServerWriter<int32_t>;

// Code for std::future taken from https://github.com/swig/swig/issues/1828#issuecomment-648449092
namespace eprosima::fastdds::dds::rpc
{
template <class R>
class RpcFuture {
 public:
    RpcFuture() noexcept;
    RpcFuture(RpcFuture &&) noexcept;
    RpcFuture(const RpcFuture& rhs) = delete;
    ~RpcFuture();
    RpcFuture& operator=(const RpcFuture& rhs) = delete;
    RpcFuture& operator=(RpcFuture&&) noexcept;

    // retrieving the value
    R get();

    // functions to check state
    bool valid() const noexcept;
    void wait() const;

/*
    template <class Rep, class Period>
    future_status wait_for(const chrono::duration<Rep, Period>& rel_time) const;
    template <class Clock, class Duration>
    future_status wait_until(const chrono::time_point<Clock, Duration>& abs_time) const;
*/
};

}

%shared_ptr(eprosima::fastdds::dds::rpc::RpcFuture<calculator_base::detail::BasicCalculator_representation_limits_Out>);
%template(calculator_base_detail_BasicCalculator_representation_limits_Out_rpc_future) eprosima::fastdds::dds::rpc::RpcFuture<calculator_base::detail::BasicCalculator_representation_limits_Out>;

%typemap(out, optimal="1") eprosima::fastdds::dds::rpc::RpcFuture<calculator_base::detail::BasicCalculator_representation_limits_Out> {
  std::shared_ptr<$1_ltype> *smartresult = new std::shared_ptr<$1_ltype>(new $1_ltype($1));
  $result = SWIG_NewPointerObj(SWIG_as_voidptr(smartresult), $descriptor(std::shared_ptr< eprosima::fastdds::dds::rpc::RpcFuture<calculator_base::detail::BasicCalculator_representation_limits_Out>> *), SWIG_POINTER_OWN);
}

%shared_ptr(eprosima::fastdds::dds::rpc::RpcFuture<int32_t>);
%template(int32_t_rpc_future) eprosima::fastdds::dds::rpc::RpcFuture<int32_t>;

%typemap(out, optimal="1") eprosima::fastdds::dds::rpc::RpcFuture<int32_t> {
  std::shared_ptr<$1_ltype> *smartresult = new std::shared_ptr<$1_ltype>(new $1_ltype($1));
  $result = SWIG_NewPointerObj(SWIG_as_voidptr(smartresult), $descriptor(std::shared_ptr< eprosima::fastdds::dds::rpc::RpcFuture<int32_t>> *), SWIG_POINTER_OWN);
}

%import(module="fastdds") "fastdds/dds/rpc/interfaces/RpcClientWriter.hpp"
%import(module="fastdds") "fastdds/dds/rpc/interfaces/RpcStatusCode.hpp"

%ignore eprosima::fastdds::dds::rpc::RpcServerReader::read(T&);
%ignore eprosima::fastdds::dds::rpc::RpcServerReader::read(T&,eprosima::fastdds::dds::Duration_t&);
%import(module="fastdds") "fastdds/dds/rpc/interfaces/RpcServerReader.hpp"
%extend eprosima::fastdds::dds::rpc::RpcServerReader {
    std::pair<bool, T> read(
        const eprosima::fastdds::dds::Duration_t& timeout = eprosima::fastdds::dds::c_TimeInfinite)
    {
        std::pair<bool, T> ret_val{};
        if (eprosima::fastdds::dds::c_TimeInfinite == timeout)
        {
            ret_val.first = self->read(ret_val.second);
        }
        else
        {
            ret_val.first = self->read(ret_val.second, timeout);
        }
        return ret_val;
    }
}

%template(int32_t_server_reader_result) std::pair<bool, int32_t>;
%template(int32_t_server_reader) eprosima::fastdds::dds::rpc::RpcServerReader<int32_t>;

%shared_ptr(eprosima::fastdds::dds::rpc::RpcClientWriter<int32_t>);
%template(int32_t_rpc_client_writer) eprosima::fastdds::dds::rpc::RpcClientWriter<int32_t>;
%typemap(in,numinputs=0) std::shared_ptr<eprosima::fastdds::dds::rpc::RpcClientWriter<int32_t>>& %{
    $1 = new std::shared_ptr<eprosima::fastdds::dds::rpc::RpcClientWriter<int32_t>>();
%}
%typemap(argout) std::shared_ptr<eprosima::fastdds::dds::rpc::RpcClientWriter<int32_t>>& (PyObject* tmp) %{
    tmp = SWIG_NewPointerObj($1, $1_descriptor, SWIG_POINTER_OWN);
    $result = SWIG_Python_AppendOutput($result, tmp);
%}

%exception;

%define %traits_penumn(Type...)
  %fragment(SWIG_Traits_frag(Type),"header",
        fragment="StdTraits") {
namespace swig {
  template <> struct traits< Type > {
    typedef value_category category;
    static const char* type_name() { return  #Type; }
  };
}
}
%enddef



%shared_ptr(calculator_base::Adder);



%shared_ptr(calculator_base::Subtractor);



%shared_ptr(calculator_base::BasicCalculator);
%shared_ptr(calculator_base::BasicCalculatorServer_IServerImplementation);
%shared_ptr(calculator_base::BasicCalculatorServerImplementation);
%feature("director") calculator_base::BasicCalculatorServerImplementation;



%shared_ptr(Calculator);
%shared_ptr(CalculatorServer_IServerImplementation);
%shared_ptr(CalculatorServerImplementation);
%feature("director") CalculatorServerImplementation;


// Include the class interfaces
%include "calculator.hpp"
%include "calculatorClient.hpp"
%include "calculatorServer.hpp"
%include "calculatorServerImpl.hpp"

// Include the corresponding TopicDataType
%include "calculatorPubSubTypes.i"

