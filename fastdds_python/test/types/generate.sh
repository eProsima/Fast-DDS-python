#!/bin/bash
if [[ -z "$(which fastddsgen)" ]]; then
    echo "Cannot find fastddsgen. Please, include it in PATH environment variable"
    exit -1
fi

fastddsgen -cdr both -python -replace test_complete.idl test_modules.idl
