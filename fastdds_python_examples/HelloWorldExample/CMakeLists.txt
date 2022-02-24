
# Using minimum CMake version 3.13 to prevent issues with the SWIG include
# directories propagation happening with CMake 3.12 and prior

cmake_minimum_required(VERSION 3.13)

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

find_package(fastcdr REQUIRED)
find_package(fastrtps REQUIRED)


set(${PROJECT_NAME}_FILES
    HelloWorld.cxx
    HelloWorldPubSubTypes.cxx
    )

include_directories()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#Create library for C++ types
add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_FILES})
target_link_libraries(${PROJECT_NAME} PUBLIC fastcdr fastrtps)

###############################################################################
# Python bindings for type

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
set(CMAKE_SWIG_FLAGS "")

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
set(PYTHON_INCLUDE_PATH ${Python3_INCLUDE_DIRS})
set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
set(PYTHON_LIBRARIES ${Python3_LIBRARY})

include_directories(${PYTHON_INCLUDE_PATH})

set(${PROJECT_NAME}_MODULE
    HelloWorldWrapper
    )

set(${PROJECT_NAME}_MODULE_FILES
    ${PROJECT_NAME}.i
    )

SET_SOURCE_FILES_PROPERTIES(
    ${${PROJECT_NAME}_MODULE_FILES}
    PROPERTIES CPLUSPLUS ON
    USE_TARGET_INCLUDE_DIRECTORIES TRUE
    )

include_directories(
    ${PROJECT_SOURCE_DIR}
    )

SWIG_ADD_LIBRARY(${${PROJECT_NAME}_MODULE}
    TYPE SHARED
    LANGUAGE python
    SOURCES ${${PROJECT_NAME}_MODULE_FILES})

SWIG_LINK_LIBRARIES(${${PROJECT_NAME}_MODULE}
    ${PYTHON_LIBRARIES}
    fastrtps
    ${PROJECT_NAME}
    )

# Find the installation path
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "from distutils import sysconfig; print(sysconfig.get_python_lib(plat_specific=True, prefix='${CMAKE_INSTALL_PREFIX}'))"
    OUTPUT_VARIABLE _ABS_PYTHON_MODULE_PATH
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )

get_filename_component (_ABS_PYTHON_MODULE_PATH ${_ABS_PYTHON_MODULE_PATH} ABSOLUTE)
file (RELATIVE_PATH _REL_PYTHON_MODULE_PATH ${CMAKE_INSTALL_PREFIX} ${_ABS_PYTHON_MODULE_PATH})
SET (PYTHON_MODULE_PATH
    ${_REL_PYTHON_MODULE_PATH}
    )

# Install
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin/
    LIBRARY DESTINATION lib/
    ARCHIVE DESTINATION lib/
    )
install(TARGETS ${${PROJECT_NAME}_MODULE} DESTINATION ${PYTHON_MODULE_PATH})
get_property(support_files TARGET ${${PROJECT_NAME}_MODULE} PROPERTY SWIG_SUPPORT_FILES)
install(FILES ${support_files} DESTINATION ${PYTHON_MODULE_PATH})

