###############################################################################
# Test subdirectories
###############################################################################

add_subdirectory(types)


configure_file(${CMAKE_CURRENT_SOURCE_DIR}/PubSubReader.py
${CMAKE_CURRENT_BINARY_DIR}/PubSubReader.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/PubSubWriter.py
${CMAKE_CURRENT_BINARY_DIR}/PubSubWriter.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/blackbox_common.py
${CMAKE_CURRENT_BINARY_DIR}/blackbox_common.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/test_blackbox_qos_values.py
${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_qos_values.py COPYONLY)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/test_blackbox_pubsub_basic.py
${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_pubsub_basic.py COPYONLY)

add_test (NAME blackbox_qos_values
  COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_qos_values.py)

add_test (NAME blackbox_pubsub_basic
  COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_BINARY_DIR}/test_blackbox_pubsub_basic.py)
