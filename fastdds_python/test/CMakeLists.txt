# Compile types
add_subdirectory(types)

add_test(NAME api_tests COMMAND ${Python3_EXECUTABLE} -m pytest -vrP WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/api)

function(populate_path target out_var)
   
    set(WIN_PATH "")
    get_target_property(LINK_LIBRARIES_ ${target} LINK_LIBRARIES)
    if(NOT "${LINK_LIBRARIES_}" STREQUAL "LINK_LIBRARIES_-NOTFOUND")
        foreach(LIBRARY_LINKED ${LINK_LIBRARIES_})
            if(TARGET ${LIBRARY_LINKED})
                # Check if is a real target or a target interface
                get_target_property(type ${LIBRARY_LINKED} TYPE)
                if(NOT type STREQUAL "INTERFACE_LIBRARY")
                    # we cannot use generator expressions because we must turn the string
                    # to cmake path (unix) format in order to make them python friendly
                    get_target_property(TARGET_PATH ${LIBRARY_LINKED} LOCATION)
                    get_filename_component(TARGET_PATH "${TARGET_PATH}" DIRECTORY)
                    set(${WIN_PATH} "${TARGET_PATH};${WIN_PATH}")
                    # recursive call
                    populate_path(${LIBRARY_LINKED} WIN_PATH)
                endif()
                unset(type)
            endif()
        endforeach()
        set(${out_var} "${WIN_PATH};${out_var}" PARENT_SCOPE)
    endif()

endfunction()

if(WIN32)

    # get the python path value
    set(PYTHON_PATH "")
    get_target_property(PYTHON_PATH fastdds_python LOCATION)
    get_filename_component(PYTHON_PATH "${PYTHON_PATH}" DIRECTORY)

    # get the path value
    set(WIN_PATH "")
    populate_path(fastdds_python WIN_PATH)
    string(REPLACE "\\" "/" WIN_PATH "${WIN_PATH}")
    string(REPLACE ";" "\\;" WIN_PATH "${WIN_PATH};$ENV{PATH}")

    # set the environment variables
    set_tests_properties(api_tests PROPERTIES
        ENVIRONMENT "PATH=${PYTHON_PATH}\\;${WIN_PATH};PYTHONPATH=${PYTHON_PATH}")

    unset(WIN_PATH)
    unset(PYTHON_PATH)

endif()
