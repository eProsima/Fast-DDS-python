
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

###############################################################################
# Library for types defined in HelloWorld IDL
###############################################################################

message(STATUS "Configuring python wrapper for types in HelloWorld...")

###############################################################################
# Type library on C++

project(HelloWorld)

FIND_PACKAGE(fastcdr REQUIRED)
FIND_PACKAGE(fastrtps REQUIRED)


set(${PROJECT_NAME}_FILES
    HelloWorld.cxx
    HelloWorldPubSubTypes.cxx
    )

INCLUDE_DIRECTORIES()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#Create library for C++ types
add_library(${PROJECT_NAME} ${${PROJECT_NAME}_FILES})
target_link_libraries(${PROJECT_NAME} PUBLIC fastcdr fastrtps)

###############################################################################
# Python bindings for type

project(HelloWorldWrapper)

FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})
SET(CMAKE_SWIG_FLAGS "")

FIND_PACKAGE(PythonLibs REQUIRED)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

FIND_PACKAGE(fastcdr REQUIRED)
FIND_PACKAGE(fastrtps REQUIRED)

set(${PROJECT_NAME}_FILES
    HelloWorld.i
    )

SET_SOURCE_FILES_PROPERTIES(
    ${${PROJECT_NAME}_FILES}
    PROPERTIES CPLUSPLUS ON
    USE_TARGET_INCLUDE_DIRECTORIES TRUE
    )

INCLUDE_DIRECTORIES(
    ${PROJECT_SOURCE_DIR}
    )

SWIG_ADD_LIBRARY(${PROJECT_NAME} 
    TYPE SHARED
    LANGUAGE python 
    SOURCES ${${PROJECT_NAME}_FILES})

SWIG_LINK_LIBRARIES(${PROJECT_NAME}
    ${PYTHON_LIBRARIES}
    fastrtps
    HelloWorld
    )

