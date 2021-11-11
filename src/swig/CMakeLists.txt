
###############################################################################
# Compile python wrapper with SWIG
###############################################################################

message(STATUS "Configuring FastDDS wrapper for Python...")

find_package (PythonInterp REQUIRED)

set(${PROJECT_NAME}_MODULE
    fastdds_wrapper
    )

set(${PROJECT_NAME}_FILES
    ${${PROJECT_NAME}_MODULE}.i
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

# Find the installation path
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "from distutils import sysconfig; print(sysconfig.get_python_lib(plat_specific=True, prefix='${CMAKE_INSTALL_PREFIX}' ) )"
    OUTPUT_VARIABLE _ABS_PYTHON_MODULE_PATH
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )
get_filename_component (_ABS_PYTHON_MODULE_PATH ${_ABS_PYTHON_MODULE_PATH} ABSOLUTE)
file (RELATIVE_PATH _REL_PYTHON_MODULE_PATH ${CMAKE_INSTALL_PREFIX} ${_ABS_PYTHON_MODULE_PATH})
SET (PYTHON_MODULE_PATH
    ${_REL_PYTHON_MODULE_PATH}
    )

# Install
INSTALL ( FILES ${CMAKE_CURRENT_BINARY_DIR}/_${PROJECT_NAME}.so DESTINATION ${PYTHON_MODULE_PATH} )
INSTALL ( FILES ${CMAKE_CURRENT_BINARY_DIR}/${${PROJECT_NAME}_MODULE}.py DESTINATION ${PYTHON_MODULE_PATH} )
