# Python binding for Fast DDS

<a href="http://www.eprosima.com"><img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSd0PDlVz1U_7MgdTe0FRIWD0Jc9_YH-gGi0ZpLkr-qgCI6ZEoJZ5GBqQ" align="left" hspace="8" vspace="2" width="100" height="100" ></a>

[![License](https://img.shields.io/github/license/eProsima/Fast-DDS-python.svg)](https://opensource.org/licenses/Apache-2.0)
[![Releases](https://img.shields.io/github/v/release/eProsima/Fast-DDS-python?sort=semver)](https://github.com/eProsima/Fast-DDS-python/releases)
[![Issues](https://img.shields.io/github/issues/eProsima/Fast-DDS-python.svg)](https://github.com/eProsima/Fast-DDS-python/issues)
[![Forks](https://img.shields.io/github/forks/eProsima/Fast-DDS-python.svg)](https://github.com/eProsima/Fast-DDS-python/network/members)
[![Stars](https://img.shields.io/github/stars/eProsima/Fast-DDS-python.svg)](https://github.com/eProsima/Fast-DDS-python/stargazers)
[![Fast DDS Python Ubuntu CI (nightly)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-ubuntu-ci.yml/badge.svg)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-ubuntu-ci.yml)
[![Fast DDS Python Windows CI (nightly)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-windows-ci.yml/badge.svg)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-windows-ci.yml)

<!-- TODO(eduponz): Remove this before releasing v3.0.0 -->
> [!WARNING]
> In preparation for v2.0.0 (bindings for Fast DDS v3.0.0), Fast DDS Python's master branch is undergoing major changes entailing **API breaks**.
> Until Fast DDS Python v2.0.0 is released, it is strongly advisable to use the latest stable version, [v1.4.1](https://github.com/eProsima/Fast-DDS-python/tree/v1.4.1).

*eProsima Fast DDS Python* is a Python binding for the [*eProsima Fast DDS*](https://github.com/eProsima/Fast-DDS) C++ library.
This is a work in progress, but ultimately the goal is having the complete *Fast DDS* API available in Python.
Two packages are available in this repository: the proper Python binding, `fastdds_python`, and the examples, `fastdds_python_examples`.

## Installation guide

This tutorial shows how to build *Fast DDS Python* using [colcon](https://colcon.readthedocs.io), a command line tool to build sets of software packages.
To do so, `colcon` and `vcstool` need to be installed:

```bash
pip install -U colcon-common-extensions vcstool
```

### Dependencies

*Fast DDS Python* depends on [Fast DDS](https://github.com/eProsima/Fast-DDS) and [Fast CDR](https://github.com/eProsima/Fast-CDR).
For simplicity, this tutorial will build these dependencies alongside the binding itself.
More advanced users can build or link to this packages separately.

Install *Fast DDS* dependencies running:

```bash
sudo apt update
sudo apt install -y \
    libasio-dev \
    libtinyxml2-dev
```

Additionally, *Fast DDS Python* also depends on [SWIG 4.0](http://www.swig.org/) and python3-dev. Install these dependencies running:
```bash
sudo apt update
sudo apt install -y \
    swig \
    libpython3-dev
```

### Build and install

```bash
# Change directory to the location where the colcon workspace will be created
cd <path_to_ws>
# Create workspace directory
mkdir -p fastdds_python_ws/src
cd fastdds_python_ws
# Get workspace setup file
wget https://raw.githubusercontent.com/eProsima/Fast-DDS-python/main/fastdds_python.repos
# Download repositories
vcs import src < fastdds_python.repos
# Build the workspace
colcon build
```

Please, refer to [colcon documentation](https://colcon.readthedocs.io/en/released/reference/verb/build.html) for more information, such as building only one of the packages.

## Python example

Fast DDS documentation includes a first publisher-subscriber application using Python.
Please refer to [this section](https://fast-dds.docs.eprosima.com/en/latest/fastdds/getting_started/simple_python_app/simple_python_app.html#) for more information.
