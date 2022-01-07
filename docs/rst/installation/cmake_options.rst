.. include:: ../exports/roles.include

.. _cmake_options:

CMake options
=============

*eProsima Fast DDS Python Bindings* provides several CMake options for build configuration of the library.

.. list-table::
    :header-rows: 1

    *   - Option
        - Description
        - Possible values
        - Default
    *   - :class:`BUILD_DOCUMENTATION`
        - Build the library documentation. Set to ``ON`` if |br|
          :class:`BUILD_DOCUMENTATION_TESTS` is set to ``ON``.
        - ``ON`` ``OFF``
        - ``OFF``
    *   - :class:`BUILD_LIBRARY_TESTS`
        - Build the library tests.
        - ``ON`` ``OFF``
        - ``OFF``
    *   - :class:`BUILD_DOCUMENTATION_TESTS`
        - Build the library documentation tests. Setting this |br|
          ``ON`` will set :class:`BUILD_DOCUMENTATION` to ``ON``.
        - ``ON`` ``OFF``
        - ``OFF``
    *   - :class:`BUILD_TESTS`
        - Build the library and documentation tests. Setting this |br|
          ``ON`` will set :class:`BUILD_LIBRARY_TESTS` and |br|
          :class:`BUILD_DOCUMENTATION_TESTS` to ``ON``.
        - ``ON`` ``OFF``
        - ``OFF``
