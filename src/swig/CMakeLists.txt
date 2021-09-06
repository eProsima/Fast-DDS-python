
###############################################################################
# Compile python wrapper with SWIG
###############################################################################

message(STATUS "Configuring FastDDS wrapper for Python...")

set(${PROJECT_NAME}_FILES
    fastdds_wrapper.i
    )

SET_SOURCE_FILES_PROPERTIES(
    ${${PROJECT_NAME}_FILES}
    PROPERTIES CPLUSPLUS ON
    USE_TARGET_INCLUDE_DIRECTORIES TRUE
    )

INCLUDE_DIRECTORIES()

SWIG_ADD_LIBRARY(${PROJECT_NAME} 
    TYPE SHARED
    LANGUAGE python 
    SOURCES ${${PROJECT_NAME}_FILES}
    )

SWIG_LINK_LIBRARIES(${PROJECT_NAME}
    ${PYTHON_LIBRARIES}
    fastrtps
    )

