
cmake_minimum_required(VERSION 3.20)

# SWIG: use standard target name.
if(POLICY CMP0078)
  cmake_policy(SET CMP0078 NEW)
endif()

# SWIG: use SWIG_MODULE_NAME property.
if(POLICY CMP0086)
  cmake_policy(SET CMP0086 NEW)
endif()

###############################################################################
# Library for types defined in calculator IDL
###############################################################################

message(STATUS "Configuring python wrapper for types in calculator...")

###############################################################################
# Type library on C++

project(calculator)

find_package(fastcdr REQUIRED)
find_package(fastdds 3 REQUIRED)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#Create library for C++ types
add_library(${PROJECT_NAME} SHARED
        calculatorTypeObjectSupport.cxx
        calculatorPubSubTypes.cxx
        calculatorClient.cxx
        calculatorServer.cxx
        )
if(WIN32)
    target_compile_definitions(${PROJECT_NAME} PRIVATE EPROSIMA_USER_DLL_EXPORT)
endif(WIN32)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)
target_include_directories(${PROJECT_NAME} PUBLIC
    ${PROJECT_SOURCE_DIR}
    )
target_link_libraries(${PROJECT_NAME}
    PUBLIC
    fastcdr
    fastdds
    )

###############################################################################
# Python bindings for type

find_package(SWIG)
if (NOT SWIG_FOUND)
    # Trick to find swig4.1 in Ubuntu noble.
    find_program(SWIG_EXECUTABLE NAMES swig4.1 swig)
    find_package(SWIG REQUIRED)
endif()
include(${SWIG_USE_FILE})
set(CMAKE_SWIG_FLAGS "")

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
set(PYTHON_INCLUDE_PATH ${Python3_INCLUDE_DIRS})
set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
set(PYTHON_LIBRARIES ${Python3_LIBRARIES})

include_directories(${PYTHON_INCLUDE_PATH})

set(${PROJECT_NAME}_MODULE
    calculatorWrapper
    )

set(${PROJECT_NAME}_MODULE_FILES
    calculator.i
    )

SET_SOURCE_FILES_PROPERTIES(
    ${${PROJECT_NAME}_MODULE_FILES}
    PROPERTIES CPLUSPLUS ON
    USE_TARGET_INCLUDE_DIRECTORIES TRUE
    )

SWIG_ADD_LIBRARY(${${PROJECT_NAME}_MODULE}
    TYPE SHARED
    LANGUAGE python
    SOURCES ${${PROJECT_NAME}_MODULE_FILES})

set_property(TARGET ${${PROJECT_NAME}_MODULE} PROPERTY CXX_STANDARD 11)
if(UNIX AND CMAKE_SIZEOF_VOID_P EQUAL 8)
    set_property(TARGET ${${PROJECT_NAME}_MODULE} PROPERTY SWIG_COMPILE_DEFINITIONS SWIGWORDSIZE64)
endif()

target_link_libraries(${${PROJECT_NAME}_MODULE}
    Python3::Module
    fastdds
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
    ${_REL_PYTHON_MODULE_PATH}/${PROJECT_NAME}
    )

# Install
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin/
    LIBRARY DESTINATION lib/
    ARCHIVE DESTINATION lib/
    )
install(TARGETS ${${PROJECT_NAME}_MODULE} DESTINATION ${PYTHON_MODULE_PATH})
get_property(support_files TARGET ${${PROJECT_NAME}_MODULE} PROPERTY SWIG_SUPPORT_FILES)
install(FILES ${support_files} DESTINATION ${PYTHON_MODULE_PATH} RENAME __init__.py)

