#!/usr/bin/env bash

idl_files=(
    './fastdds_python/test/types/test_modules.idl'
    './fastdds_python/test/types/test_complete.idl'
    './fastdds_python/test/types/test_included_modules.idl'
    './fastdds_python_examples/HelloWorldExample/HelloWorld.idl'
)

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

for idl_file in "${idl_files[@]}"; do
    idl_dir=$(dirname "${idl_file}")
    file_from_gen=$(basename "${idl_file}")

    echo -e "Processing ${yellow}${idl_file}${textreset}"

    cd "${idl_dir}"

    echo "Running: fastddsgen -cdr both -replace -flat-output-dir -python ${file_from_gen}"
    fastddsgen -cdr both -replace -flat-output-dir -python ${file_from_gen}

    if [[ $? != 0 ]]; then
        ret_value=-1
    fi

    cd -
done

exit ${ret_value}
