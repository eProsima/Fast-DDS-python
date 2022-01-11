# Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###############################################################################
# Test subdirectories
###############################################################################

add_subdirectory(types)


configure_file(${CMAKE_CURRENT_SOURCE_DIR}/PubSubReader.py
${CMAKE_CURRENT_BINARY_DIR}/PubSubReader.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/PubSubWriter.py
${CMAKE_CURRENT_BINARY_DIR}/PubSubWriter.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/blackbox_common.py
${CMAKE_CURRENT_BINARY_DIR}/blackbox_common.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/test_blackbox_qos_values.py
${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_qos_values.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/test_blackbox_pubsub_basic.py
${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_pubsub_basic.py COPYONLY)

add_test (NAME blackbox_qos_values
  COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_qos_values.py)

add_test (NAME blackbox_pubsub_basic
  COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_pubsub_basic.py)
