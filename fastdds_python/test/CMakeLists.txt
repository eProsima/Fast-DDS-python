# Compile types
add_subdirectory(types)

add_test(NAME api_tests COMMAND ${Python3_EXECUTABLE} -m pytest -vrP test_domainparticipant.py WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/api)
