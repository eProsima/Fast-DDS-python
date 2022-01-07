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

FIND_PACKAGE(PythonLibs REQUIRED)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

FIND_PACKAGE(fastrtps REQUIRED)

###############################################################################
# Project subdirectories
###############################################################################

add_subdirectory(src/swig)

###############################################################################
# Testing options
###############################################################################
option(BUILD_TESTS "Build Fast DDS Python Bindings and documentation tests" OFF)
option(BUILD_LIBRARY_TESTS "Build Fast DDS Python Bindings tests" OFF)
option(BUILD_DOCUMENTATION_TESTS "Build Fast DDS Python Bindings documentation tests" OFF)

if (BUILD_TESTS)
    set(BUILD_LIBRARY_TESTS ON)
    set(BUILD_DOCUMENTATION_TESTS ON)
endif()

if (BUILD_LIBRARY_TESTS OR BUILD_DOCUMENTATION_TESTS)
    # CTest needs to be included here, otherwise it is not possible to run the tests from the root
    # of the build directory
    enable_testing()
    include(CTest)
endif()

if (BUILD_LIBRARY_TESTS)
    add_subdirectory(test)
endif()

###############################################################################
# Documentation
###############################################################################
option(BUILD_DOCUMENTATION "Generate documentation" OFF)
if (BUILD_DOCUMENTATION OR BUILD_DOCUMENTATION_TESTS)
    set (BUILD_DOCUMENTATION ON)
    add_subdirectory(docs)
endif()
