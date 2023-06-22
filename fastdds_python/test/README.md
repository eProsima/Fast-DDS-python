# How to re-generate data types for python

1.  Navigate to `fastdds_python/fastdds_python/test/types`
2.  Run Fast DDS Gen script

    ```bash
    fastddsgen -python -replace test_complete.idl test_modules.idl
    ```
