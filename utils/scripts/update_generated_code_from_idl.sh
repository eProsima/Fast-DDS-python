#!/usr/bin/env bash

red='\E[1;31m'
yellow='\E[1;33m'
textreset='\E[1;0m'

current_dir=$(git rev-parse --show-toplevel)

if [[ ! "$(pwd -P)" -ef "${current_dir}" ]]; then
    echo -e "${red}This script must be executed in the repository root directory.${textreset}"
    exit -1
fi

if [[ -z "$(which fastddsgen)" ]]; then
    echo "Cannot find fastddsgen. Please, include it in PATH environment variable"
    exit -1
fi

ret_value=0

cd ./fastdds_python/test/types
echo -e "Processing ${yellow}test_complete.idl test_modules.idl${textreset}"
echo "Running: fastddsgen -replace -python test_complete.idl test_modules.idl"
fastddsgen -replace -python test_complete.idl test_modules.idl
if [[ $? != 0 ]]; then
    ret_value=-1
fi
cd -

if [[ $ret_value != -1 ]]; then
    cd "./fastdds_python_examples/HelloWorldExample"

echo -e "Processing ${yellow}HelloWorld.idl${textreset}"
    echo "Running: fastddsgen -replace -python HelloWorld.idl"
    fastddsgen -replace -python HelloWorld.idl
fi

if [[ $? != 0 ]]; then
    ret_value=-1
fi
cd -

exit ${ret_value}
