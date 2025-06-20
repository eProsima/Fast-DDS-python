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
 * @file calculatorClient.hpp
 * Client implementation for interfaces
 *
 * This file was generated by the tool fastddsgen (version: 4.1.0).
 */

#ifndef FAST_DDS_GENERATED__CALCULATOR_CLIENT_HPP
#define FAST_DDS_GENERATED__CALCULATOR_CLIENT_HPP

#include <memory>

#include <fastdds/dds/domain/DomainParticipant.hpp>
#include <fastdds/dds/domain/qos/RequesterQos.hpp>

#include "calculator.hpp"

namespace calculator_base {

extern eProsima_user_DllExport std::shared_ptr<BasicCalculator> create_BasicCalculatorClient(
        eprosima::fastdds::dds::DomainParticipant& part,
        const char* service_name,
        const eprosima::fastdds::dds::RequesterQos& qos);


} // namespace calculator_base

extern eProsima_user_DllExport std::shared_ptr<Calculator> create_CalculatorClient(
        eprosima::fastdds::dds::DomainParticipant& part,
        const char* service_name,
        const eprosima::fastdds::dds::RequesterQos& qos);


#endif  // FAST_DDS_GENERATED__CALCULATOR_CLIENT_HPP
