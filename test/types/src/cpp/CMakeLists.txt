
###############################################################################
# Compile topic types
###############################################################################

message(STATUS "Configuring Topic data types...")

cmake_minimum_required(VERSION 2.8.12)

if(NOT CMAKE_VERSION VERSION_LESS 3.0)
    cmake_policy(SET CMP0048 NEW)
endif()

project(TopicDataTypes)

# Find requirements
if(NOT fastcdr_FOUND)
    find_package(fastcdr REQUIRED)
endif()

if(NOT fastrtps_FOUND)
    find_package(fastrtps REQUIRED)
endif()


set(${PROJECT_NAME}_FILES
    HelloWorld/HelloWorld.cxx
    HelloWorld/HelloWorldTopicDataType.cxx
    FooBar/Foo.cxx
    FooBar/Bar.cxx
    )

INCLUDE_DIRECTORIES()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#Create library
add_library(${PROJECT_NAME} ${${PROJECT_NAME}_FILES})

target_link_libraries(${PROJECT_NAME} PUBLIC fastcdr fastrtps)

