cmake_minimum_required(VERSION 2.8.12)

if(NOT CMAKE_VERSION VERSION_LESS 3.0)
    cmake_policy(SET CMP0048 NEW)
endif()

# SWIG: use standard target name.
if(POLICY CMP0078)
  cmake_policy(SET CMP0078 NEW)
endif()

# SWIG: use SWIG_MODULE_NAME property.
if(POLICY CMP0086)
  cmake_policy(SET CMP0086 NEW)
endif()

project(FastDdsPythonWrapper)

###############################################################################
# Dependencies
###############################################################################

FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})
SET(CMAKE_SWIG_FLAGS "")

FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

if(NOT fastrtps_FOUND)
    find_package(fastrtps REQUIRED)
endif()

###############################################################################
# Compile python wrapper with SWIG
###############################################################################

message(STATUS "Configuring FastDDS wrapper for Python...")

#file(GLOB_RECURSE SWIG_INTERFACE_FILES
#    ${PROJECT_SOURCE_DIR}/src/swig/**/*.i)

set(SWIG_INTERFACE_FILES
    ${PROJECT_SOURCE_DIR}/src/swig/fastdds_wrapper.i
    #${PROJECT_SOURCE_DIR}/src/swig/hello_world_type.i
    )

set(DATA_TYPE_FILES
    ${PROJECT_SOURCE_DIR}/src/cpp/types/HelloWorld.cxx
    ${PROJECT_SOURCE_DIR}/src/cpp/types/HelloWorldTopicDataType.cxx
    ${PROJECT_SOURCE_DIR}/src/cpp/types/Foo.cxx
    ${PROJECT_SOURCE_DIR}/src/cpp/types/Bar.cxx
    )

SET_SOURCE_FILES_PROPERTIES(
    ${SWIG_INTERFACE_FILES}
    ${DATA_TYPE_FILES}
    PROPERTIES CPLUSPLUS ON
    USE_TARGET_INCLUDE_DIRECTORIES TRUE
    )

INCLUDE_DIRECTORIES(
    ${PROJECT_SOURCE_DIR}/src/swig
    ${PROJECT_SOURCE_DIR}/src/cpp
    )

SWIG_ADD_LIBRARY(FastDdsPythonWrapper 
    TYPE SHARED
    LANGUAGE python 
    SOURCES ${SWIG_INTERFACE_FILES} ${DATA_TYPE_FILES})
SWIG_LINK_LIBRARIES(FastDdsPythonWrapper ${PYTHON_LIBRARIES} fastrtps)

