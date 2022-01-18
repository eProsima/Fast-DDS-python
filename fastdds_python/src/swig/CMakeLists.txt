
###############################################################################
# Compile python wrapper with SWIG
###############################################################################

message(STATUS "Configuring FastDDS wrapper for Python...")

find_package (PythonInterp REQUIRED)

set(${PROJECT_NAME}_MODULE
    fastdds
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
install(TARGETS ${PROJECT_NAME} DESTINATION ${PYTHON_MODULE_PATH})
get_property(support_files TARGET ${PROJECT_NAME} PROPERTY SWIG_SUPPORT_FILES)
install(FILES ${support_files} DESTINATION ${PYTHON_MODULE_PATH})