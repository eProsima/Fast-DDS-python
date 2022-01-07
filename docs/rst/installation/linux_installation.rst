.. _linux_installation:

Linux installation from sources
===============================

The instructions for installing the *eProsima Fast DDS Python Bindings* from sources are provided in this page.
It is organized as follows:

.. contents::
    :local:
    :backlinks: none
    :depth: 2

.. _fastdds_python_linux:

Fast DDS Python Bindings installation
"""""""""""""""""""""""""""""""""""""

This section describes the instructions for installing *eProsima Fast DDS Python Bindings* in a Linux environment from
sources.
First of all, the :ref:`requirements_source_linux` and :ref:`dependencies_source_linux` detailed below need to be met.
Afterwards, the user can choose whether to follow either the :ref:`colcon <colcon_installation_linux>` or the
:ref:`CMake <cmake_installation_linux>` installation instructions.

.. _requirements_source_linux:

Requirements
------------

The installation of *eProsima Fast DDS Python Bindings* in a Linux environment from sources requires the following
tools to be installed in the system:

* :ref:`cmake_gcc_pip3_wget_git_source_linux`
* :ref:`gtest_source_linux` [optional]

.. _cmake_gcc_pip3_wget_git_source_linux:

CMake, g++, pip3, wget and git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These packages provide the tools required to install *eProsima Fast DDS Python Bindings* and its dependencies from
command line.
Install CMake_, `g++ <https://gcc.gnu.org/>`_, pip3_, wget_ and git_ using the package manager of the appropriate
Linux distribution.
For example, on Ubuntu use the command:

.. code-block:: bash

    sudo apt install cmake g++ python3-pip wget git

.. _gtest_source_linux:

Gtest
^^^^^

Gtest is a unit testing library for C++.
By default, *eProsima Fast DDS Python Bindings* does not compile tests.
It is possible to activate them with the opportune
`CMake configuration options <https://cmake.org/cmake/help/v3.6/manual/cmake.1.html#options>`_ when calling colcon_ or
CMake_.
For more details, please refer to the :ref:`cmake_options` section.
For a detailed description of the Gtest installation process, please refer to the
Gtest_ Installation Guide.

.. _dependencies_source_linux:

Dependencies
------------

*eProsima Fast DDS Python Bindings* has the following dependencies in a Linux environment:

* :ref:`fastDDS_source_linux`
* :ref:`swig_pythondev_source_linux`
* :ref:`documentation_dependencies_source_linux` [Optional]

.. _fastDDS_source_linux:

eProsima Fast DDS
^^^^^^^^^^^^^^^^^

Please, refer to the
`eProsima Fast DDS <https://fast-dds.docs.eprosima.com/en/latest/installation/binaries/binaries_linux.html#linux-binaries>`_
installation documentation to learn the installing procedure.

SWIG and Python development tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SWIG_ (Simplified Wrapper and Interface Generator) is a software development tool for building scripting language
interfaces to C and C++ programs.
Python development tools must also be installed.
Please, install these dependencies using the package manager of the appropriate Linux distribution.
For example, on Ubuntu use the command:

.. code-block:: bash

    sudo apt install swig libpython3-dev

Documentation dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^

In case that the documentation and its tests are also installed (please refer to :ref:`cmake_options` to see how to
enable it), some python3 dependencies are required: Doxygen_, Sphinx_, Breathe_ and doc8_.
This guide uses a Python virtual environment to install such dependencies, thus avoiding polluting the user's
installation except Doxygen that it is installed using the distribution package manager.

.. code-block:: bash

    DOXYGEN!

    python3 -m venv fastdds-python-docs-venv
    source fastdds-python-docs-venv/bin/activate
    wget https://raw.githubusercontent.com/eProsima/Fast-DDS-python/master/docs/requirements.txt
    pip3 install -r requirements.txt


.. _colcon_installation_linux:

Colcon installation
-------------------

colcon_ is a command line tool based on CMake_ aimed at building sets of software packages.
This section explains how to use it to compile *eProsima Fast DDS Python Bindings* and its other eProsima dependencies.

#. Install the ROS 2 development tools (colcon_ and vcstool_) by executing the following command:

    .. code-block:: bash

        pip3 install -U colcon-common-extensions vcstool
    
    .. note::

        If this fails due to an Environment Error, add the :code:`--user` flag to the :code:`pip3` installation command.

#. Create a :code:`Fast-DDS-python` directory and download the `repos` file that will be used to install
   *eProsima Fast DDS Python Bindings* and its other eProsima dependencies:

    .. code-block:: bash

        mkdir -p ~/Fast-DDS-python/src
        cd ~/Fast-DDS-python
        wget https://raw.githubusercontent.com/eProsima/Fast-DDS-python/main/fastdds_python.repos
        vcs import src < fastdds_python.repos

#. Build the packages:

    .. code-block:: bash

        colcon build

.. note::

    Being based on CMake_, it is possible to pass the CMake configuration options to the :code:`colcon build` command.
    For more information on the specific syntax, please refer to the
    `CMake specific arguments <https://colcon.readthedocs.io/en/released/reference/verb/build.html#cmake-specific-arguments>`_
    to set the configuration.

.. _run_app_colcon_source_linux:

Run an application
^^^^^^^^^^^^^^^^^^

The *Fast DDS* functionality is contained in the :code:`fastdds` module so, besides importing this module in the Python
script, the colcon overlay built in the previous section must be sourced.
There are two possibilities:

* Every time a new shell is opened, prepare the environment locally by running the command:

    .. code-block:: bash
    
        source ~/Fast-DDS-python/install/setup.bash

* Add the sourcing of the colcon overlay permanently to the :code:`PATH`, by running:

    .. code-block:: bash

        echo 'source ~/Fast-DDS-python/install/setup.bash' >> ~/.bashrc

.. _cmake_installation_linux:

CMake installation
------------------

This section explains how to compile *eProsima Fast DDS Python Bindings* with CMake_, either
:ref:`locally <local_installation_source_linux>` or :ref:`globally <global_installation_source_linux>`.

.. _local_installation_source_linux:

Local installation
^^^^^^^^^^^^^^^^^^

#. Follow the 
   `eProsima Fast DDS local installation guide <https://fast-dds.docs.eprosima.com/en/latest/installation/sources_linux.html#local-installation>`_
   to install *eProsima Fast DDS* and its dependencies.

#. Install *eProsima Fast DDS Python Bindings*:

    .. code-block:: bash
    
        cd ~/Fast-DDS
        git clone https://github.com/eProsima/Fast-DDS-python.git
        mkdir Fast-DDS-python/build
        cd Fast-DDS-python/build
        cmake .. -DCMAKE_INSTALL_PREFIX=~/Fast-DDS/install -DCMAKE_PREFIX_PATH=~/Fast-DDS/install
        cmake --build . --target install

.. note::

    By default, *eProsima Fast DDS Python Bindings* does not compile tests.
    However, they can be activated by downloading and installing Gtest_,
    and enabling :ref:`the corresponding CMake option <cmake_options>`.

.. _global_installation_source_linux:

Global installation
^^^^^^^^^^^^^^^^^^^

#. Follow the
   `eProsima Fast DDS global installation guide <https://fast-dds.docs.eprosima.com/en/latest/installation/sources_linux.html#global-installation>`_
   to install *eProsima Fast DDS* and its dependencies:

#. Install *eProsima Fast DDS Python Bindings*:

    .. code-block:: bash
    
        cd ~/Fast-DDS
        git clone https://github.com/eProsima/Fast-DDS-python.git
        mkdir Fast-DDS-python/build
        cd Fast-DDS-python/build
        cmake ..
        sudo cmake --build . --target install

.. _run_app_cmake_source_linux:

Run an application
^^^^^^^^^^^^^^^^^^

The *Fast DDS* functionality is contained in the :code:`fastdds` module so, besides importing this module in the Python
script, the library must be found.
Consequently, prepare the environment setting the installation folder, which in case of a system-wide installation is
:code:`/usr/local/lib/` (if installed locally, adjust for the correct install directory).
There are two possibilities:

* Prepare the environment locally by running the command:

    .. code-block:: bash
    
        export LD_LIBRARY_PATH=/usr/local/lib/

* Add it permanently to the :code:`PATH` by running:

    .. code-block:: bash

        echo 'export LD_LIBRARY_PATH=/usr/local/lib/' >> ~/.bashrc

.. External links

.. _colcon: https://colcon.readthedocs.io/en/released/
.. _CMake: https://cmake.org
.. _pip3: https://docs.python.org/3/installing/index.html
.. _wget: https://www.gnu.org/software/wget/
.. _git: https://git-scm.com/
.. _Gtest: https://github.com/google/googletest
.. _vcstool: https://pypi.org/project/vcstool/
.. _SWIG: http://www.swig.org/
.. _Doxygen: https://www.doxygen.nl/index.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _Breathe: https://breathe.readthedocs.io/en/latest/
.. _doc8: https://github.com/PyCQA/doc8
