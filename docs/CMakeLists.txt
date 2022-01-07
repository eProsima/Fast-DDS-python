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
# Build Doxygen documentation
####################################################################################################

file(GLOB_RECURSE HPP_FILES "${PROJECT_SOURCE_DIR}/include/**/*.h*")
set(PROJECT_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set(PROJECT_SOURCE_DOCS_DIR ${PROJECT_SOURCE_DIR}/docs)
set(PROJECT_BINARY_DOCS_DIR ${PROJECT_BINARY_DIR}/docs)
set(DOCS_OUTPUT_HTML_DIR ${PROJECT_BINARY_DOCS_DIR}/html)

find_package(Doxygen REQUIRED)
# Doxygen related variables
set(DOXYGEN_INPUT_DIR "${PROJECT_INCLUDE_DIR}")
set(DOXYGEN_OUTPUT_DIR "${PROJECT_BINARY_DOCS_DIR}/doxygen")
set(DOXYGEN_OUTPUT_XML_DIR "${DOXYGEN_OUTPUT_DIR}/xml")
set(DOXYGEN_OUTPUT_HTML_DIR "${DOXYGEN_OUTPUT_DIR}/html")
set(DOXYGEN_INDEX_FILE "${DOXYGEN_OUTPUT_XML_DIR}/index.xml")
set(DOXYFILE_IN "${CMAKE_CURRENT_SOURCE_DIR}/doxygen-config.in")
set(DOXYFILE_OUT ${PROJECT_BINARY_DOCS_DIR}/doxygen-config)

# Create doxygen directories
add_custom_target(doc-dirs
    COMMAND ${CMAKE_COMMAND} -E make_directory ${PROJECT_BINARY_DOCS_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOCS_OUTPUT_HTML_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOXYGEN_OUTPUT_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOXYGEN_OUTPUT_XML_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${DOXYGEN_OUTPUT_HTML_DIR}
    COMMENT "Creating documentation directories" VERBATIM)

# Configure doxygen
configure_file(${DOXYFILE_IN} ${DOXYFILE_OUT} @ONLY)

# Doxygen command
add_custom_command(OUTPUT ${DOXYGEN_INDEX_FILE}
    COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYFILE_OUT}
    DEPENDS ${HPP_FILES}
    MAIN_DEPENDENCY ${DOXYFILE_OUT} ${DOXYFILE_IN}
    COMMENT "Generating doxygen documentation")

# Generate API reference
add_custom_target(doxygen ALL
    DEPENDS ${DOXYGEN_INDEX_FILE}
    COMMENT "Generated API documentation with doxygen" VERBATIM)
add_dependencies(doxygen doc-dirs)

# Install doxygen generated XML files
install(DIRECTORY ${DOXYGEN_OUTPUT_XML_DIR}
    DESTINATION docs/${PROJECT_NAME}/doxygen
    COMPONENT fastdds-python-doxygen)
set(CPACK_COMPONENT_fastdds-python-doxygen_DISPLAY_NAME "Fast DDS Python Bindings doxygen")
set(CPACK_COMPONENT_fastdds-python-doxygen_DESCRIPTION
    "eProsima Fast DDS Python Bindings doxygen documentation")
set(CPACK_COMPONENTS_ALL ${CPACK_COMPONENTS_ALL} doxygen)

####################################################################################################
# Build Sphinx documentation
####################################################################################################
# Find sphinx
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/modules" ${CMAKE_MODULE_PATH})
find_package(Sphinx REQUIRED)

set(DOCS_BUILDER html)

# Generate the sphinx documentation
add_custom_target(Sphinx ALL
    COMMAND
    ${SPHINX_EXECUTABLE} -b ${DOCS_BUILDER}
    # Tell Breathe where to find the Doxygen output
    -D breathe_projects.fastdds_python=${DOXYGEN_OUTPUT_XML_DIR}
    $<$<STREQUAL:"${CMAKE_BUILD_TYPE}","Debug">:-Dtodo_include_todos=1>
    -d "${PROJECT_BINARY_DOCS_DIR}/doctrees"
    ${PROJECT_SOURCE_DOCS_DIR}
    ${DOCS_OUTPUT_HTML_DIR}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS doxygen
    COMMENT "Generating documentation with Sphinx")

# Install the generated docs
install(DIRECTORY ${DOCS_OUTPUT_HTML_DIR}
    DESTINATION docs/${PROJECT_NAME}/sphinx
    COMPONENT fastdds-python-sphinx
    PATTERN ".buildinfo" EXCLUDE)
set(CPACK_COMPONENT_fastdds-python-sphinx_DISPLAY_NAME "Fast DDS Python Bindings Sphinx")
set(CPACK_COMPONENT_fastdds-python-sphinx_DESCRIPTION
    "eProsima Fast DDS Python Bindings documentation in ${DOCS_BUILDER} format")
set(CPACK_COMPONENTS_ALL ${CPACK_COMPONENTS_ALL} ${DOCS_BUILDER})

# Add tests if required
if(BUILD_DOCUMENTATION_TESTS)
    message(STATUS "Adding documentation tests")
    add_subdirectory(test)
endif()
