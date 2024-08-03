#!/bin/bash

# Script to install required software in manylinux2014 container

set -eu

# Install tinyxml2 and asio
# yum install -y tinyxml2-devel asio-devel
INSTALL_FOLDER=`pwd`/install
echo "Installing to ${INSTALL_FOLDER}"

# Foo nathan
git clone --branch v0.7-3 https://github.com/foonathan/memory.git
mkdir memory/build
pushd memory/build
cmake .. --install-prefix ${INSTALL_FOLDER} -DCMAKE_BUILD_TYPE=Release -DFOONATHAN_MEMORY_BUILD_EXAMPLES=OFF -DFOONATHAN_MEMORY_BUILD_TESTS=OFF
make install
popd

# Fast CDR:
git clone --branch 2.2.3 https://github.com/eProsima/Fast-CDR.git
mkdir Fast-CDR/build
pushd Fast-CDR/build
cmake .. --install-prefix ${INSTALL_FOLDER} -DCMAKE_BUILD_TYPE=Release
make install
popd

# Fast RTPS:
git clone --branch v2.14.3 https://github.com/eProsima/Fast-DDS.git
mkdir Fast-DDS/build
pushd Fast-DDS/build
cmake .. --install-prefix ${INSTALL_FOLDER} -DCMAKE_BUILD_TYPE=Release
make install
popd
