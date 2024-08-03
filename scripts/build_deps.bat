
@REM  Foo nathan
git clone --branch v0.7-3 https://github.com/foonathan/memory.git
mkdir memory\build
pushd memory\build
cmake .. -DCMAKE_BUILD_TYPE=Release -DFOONATHAN_MEMORY_BUILD_EXAMPLES=OFF -DFOONATHAN_MEMORY_BUILD_TESTS=OFF -G Ninja
ninja install
popd

@REM Fast CDR
git clone --branch 2.2.3 https://github.com/eProsima/Fast-CDR.git
mkdir Fast-CDR\build
pushd Fast-CDR\build
cmake .. -DCMAKE_BUILD_TYPE=Release -G Ninja
ninja install
popd

@REM Fast RTPS
git clone --branch v2.14.3 https://github.com/eProsima/Fast-DDS.git
mkdir Fast-DDS\build
pushd Fast-DDS\build
cmake .. -DCMAKE_BUILD_TYPE=Release -G Ninja
ninja install
popd