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

####################################################################################################
# Add tests
####################################################################################################

# Check docs style
find_program(DOC8 doc8 DOC "path to doc8 executable")
message(STATUS "doc8 found: ${DOC8}")
if(DOC8)
    add_test(
        NAME documentation.doc8
        COMMAND ${DOC8}
        --max-line-length 120 ${PROJECT_SOURCE_DOCS_DIR})
else()
    message(FATAL_ERROR "Could not find doc8")
endif()

# Check docs spelling
add_test(NAME documentation.spell_check
    COMMAND
    ${SPHINX_EXECUTABLE} -Q -W --keep-going
    -D breathe_projects.fastdds_statistics_backend=${DOXYGEN_OUTPUT_DIR}/xml
    -b spelling
    -d "${PROJECT_BINARY_DOCS_DIR}/doctrees"
    ${PROJECT_SOURCE_DOCS_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}/spelling)
