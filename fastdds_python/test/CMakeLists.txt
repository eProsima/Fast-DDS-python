# Compile types
add_subdirectory(types)

# this test checks if the swig generated fastdds.py can be imported (windows platform has issues)
add_test(NAME import_test COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/import_test.py)

add_test(NAME api_tests COMMAND ${Python3_EXECUTABLE} -m pytest WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/api)

if(WIN32)
        # Environment variables must be separated with ; thus we must escape \\; to split directories
        # Note that $<TARGET_FILE_DIR:...> returns a path with / as path separator. win32api python module
        # cannot yet handle \ (guess it doesn't escape them after reading the environment)
        set(MYPATH "PATH=$<TARGET_FILE_DIR:Python3::Module>;$<TARGET_FILE_DIR:fastrtps>")
        set(MYPATH "${MYPATH};$<TARGET_FILE_DIR:fastcdr>;$<TARGET_FILE_DIR:fastdds_python>")
        set(MYPATH "${MYPATH};$<TARGET_FILE_DIR:test_complete>")
        set(MYPATH "${MYPATH};$<TARGET_FILE_DIR:foonathan_memory>;$ENV{PATH}")
        string(REPLACE ";" "\\;" MYPATH "${MYPATH}") # cannot modify the generator expressions but how are joined

        set(MYPYTHONPATH "PYTHONPATH=$<TARGET_FILE_DIR:fastdds_python>;$<TARGET_PROPERTY:fastdds_python,BINARY_DIR>")
        set(MYPYTHONPATH "${MYPYTHONPATH};$<TARGET_FILE_DIR:test_complete>;$<TARGET_PROPERTY:test_complete,BINARY_DIR>")
        string(REPLACE ";" "\\;" MYPYTHONPATH "${MYPYTHONPATH}")

        # set the environment variables
        set_tests_properties(import_test api_tests PROPERTIES ENVIRONMENT "${MYPATH};${MYPYTHONPATH}")

        unset(MYPATH)
        unset(MYPYTHONPATH)
endif()
