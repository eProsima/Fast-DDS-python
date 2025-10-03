# until https://bugs.python.org/issue46276 is not fixed we can apply this
# workaround on windows
import os

if os.name == "nt":
    import win32api

    win32api.LoadLibrary("test_complete")

import fastdds
import pytest
import sys


def test_create_instance_handle_from_bytes():
    ih = fastdds.InstanceHandle_t()
    ih.value = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
    assert (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16) == ih.value


def test_create_instance_handle_from_bytearray():
    ih = fastdds.InstanceHandle_t()
    ih.value = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    assert (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16) == ih.value


def test_create_instance_handle_from_tuple():
    ih = fastdds.InstanceHandle_t()
    ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    assert (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16) == ih.value


def test_create_instance_handle_from_list():
    ih = fastdds.InstanceHandle_t()
    ih.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16) == ih.value


def test_create_instance_handle_from_bytes_with_less_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e"
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 bytes"


def test_create_instance_handle_from_bytes_with_more_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = (
            b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12"
        )
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 bytes"


def test_create_instance_handle_from_bytearray_with_less_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 bytes"


def test_create_instance_handle_from_bytearray_with_more_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = bytearray(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        )
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 bytes"


def test_create_instance_handle_from_tuple_with_less_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 elements"


def test_create_instance_handle_from_tuple_with_more_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 elements"


def test_create_instance_handle_from_list_with_less_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 elements"


def test_create_instance_handle_from_list_with_more_elements():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Expected 16 elements"


def test_create_instance_handle_from_bytearray_with_with_negative_number():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(ValueError) as exception:
        ih.value = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, -10, 11, 12, 13, 14, 15, 16])
    assert str(exception.value) == "byte must be in range(0, 256)"


def test_create_instance_handle_from_bytearray_with_large_number():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(ValueError) as exception:
        ih.value = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, 1000, 11, 12, 13, 14, 15, 16])
    assert str(exception.value) == "byte must be in range(0, 256)"


def test_create_instance_handle_from_tuple_with_negative_number():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, -10, 11, 12, 13, 14, -15, 16)
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Each value must be in 0..255"


def test_create_instance_handle_from_tuple_with_large_number():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 1000, 11, 12, 13, 14, 15, 16)
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Each value must be in 0..255"


def test_create_instance_handle_from_list_with_negative_number():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, -10, 11, 12, 13, 14, 15, 16]
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Each value must be in 0..255"


def test_create_instance_handle_from_list_with_large_number():
    ih = fastdds.InstanceHandle_t()
    with pytest.raises(SystemError) as exception:
        ih.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1000, 11, 12, 13, 14, 15, 16]
    repr = exception.getrepr()
    assert str(repr).split("\n")[0] == "ValueError: Each value must be in 0..255"
