# Python binding for Fast DDS

<a href="http://www.eprosima.com"><img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSd0PDlVz1U_7MgdTe0FRIWD0Jc9_YH-gGi0ZpLkr-qgCI6ZEoJZ5GBqQ" align="left" hspace="8" vspace="2" width="100" height="100" ></a>

[![License](https://img.shields.io/github/license/eProsima/Fast-DDS-python.svg)](https://opensource.org/licenses/Apache-2.0)
[![Releases](https://img.shields.io/github/v/release/eProsima/Fast-DDS-python?sort=semver)](https://github.com/eProsima/Fast-DDS-python/releases)
[![Issues](https://img.shields.io/github/issues/eProsima/Fast-DDS-python.svg)](https://github.com/eProsima/Fast-DDS-python/issues)
[![Forks](https://img.shields.io/github/forks/eProsima/Fast-DDS-python.svg)](https://github.com/eProsima/Fast-DDS-python/network/members)
[![Stars](https://img.shields.io/github/stars/eProsima/Fast-DDS-python.svg)](https://github.com/eProsima/Fast-DDS-python/stargazers)
[![Fast DDS Python Ubuntu CI (nightly)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-ubuntu-ci.yml/badge.svg)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-ubuntu-ci.yml)
[![Fast DDS Python Windows CI (nightly)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-windows-ci.yml/badge.svg)](https://github.com/eProsima/Fast-DDS-Python/actions/workflows/nightly-windows-ci.yml)

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

Additionally, *Fast DDS Python* also depends on [SWIG](http://www.swig.org/) and python3-dev. Install these dependencies running:
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

## Limitations

This project is on the very early stages of development, and there are many features not available yet. These include, but are not restricted to:

* QoS modification is not supported on python. It is possible to create a QoS object with the default constructor
  or retrieve it with the `get_qos` methods of the entities, but it is not possible to modify the QoS values.
  If you need to use non-default QoS, please use XML configuration files.

## Python example

The *Fast DDS* functionality is contained in the `fastdds` module, so you will need to include that module in your script. You will also need to create the python binding for your data type and include its module. This example will guide you through these steps in a simple example.

### Generate a data type

Create an IDL file with the description of your data type and save it as `HelloWorld.idl`:

```
struct HelloWorld
{
	unsigned long index;
	string message;
};
```

Use [*Fast DDS gen*](https://fast-dds.docs.eprosima.com/en/latest/fastddsgen/usage/usage.html) to generate the necessary files from this IDL. If you installed *Fast DDS Python* using the `fastdds_python.repos` file, you will find *Fast DDS Gen* in the `src` file. Do not forget to use the `-python` option to create the files needed for the python binding:

```bash
fastddsgen -python HelloWorld.idl
```

Now use the generated CMakeFile to compile the data type and create the python binding:

```bash
mkdir HelloWorld_build
cd HelloWorld_build
cmake ..
cmake --build .
```

This will create a `HelloWorld.py` file with a `HelloWorld` module that you will need to add to your script.

### Creating the DataWriter

Import the `fastdds` and the `HelloWorld` modules and follow the usual steps to create a DataWriter:

```python
import fastdds
import HelloWorld

domain = 5;
factory = fastdds.DomainParticipantFactory.get_instance()
participant_qos = fastdds.DomainParticipantQos()
factory.get_default_participant_qos(participant_qos)
participant = factory.create_participant(domain, participant_qos)

topic_data_type = HelloWorld.HelloWorldPubSubType()
topic_data_type.setName("HelloWorldDataType")
type_support = fastdds.TypeSupport(topic_data_type)
participant.register_type(type_support)

topic_qos = fastdds.TopicQos()
participant.get_default_topic_qos(topic_qos)
topic = self.participant.create_topic("myTopic", topic_data_type.getName(), topic_qos)

publisher_qos = fastdds.PublisherQos()
participant.get_default_publisher_qos(publisher_qos)
publisher = participant.create_publisher(publisher_qos)

writer_qos = fastdds.DataWriterQos()
publisher.get_default_datawriter_qos(writer_qos)
writer = self.publisher.create_datawriter(topic, writer_qos)
```

### Publishing a sample

You can publish a sample the same way you would do it in C++:

```python
data = HelloWorld.HelloWorld()
data.message("Hello World")
data.index(0)
writer.write(data)
```

### Creating the DataReader

Import the `fastdds` and the `HelloWorld` modules and follow the usual steps to create a DataReader:

```python
import fastdds
import HelloWorld

domain = 5;
factory = fastdds.DomainParticipantFactory.get_instance()
participant_qos = fastdds.DomainParticipantQos()
factory.get_default_participant_qos(participant_qos)
participant = factory.create_participant(domain, participant_qos)

topic_data_type = HelloWorld.HelloWorldPubSubType()
topic_data_type.setName("HelloWorldDataType")
type_support = fastdds.TypeSupport(topic_data_type)
participant.register_type(type_support)

topic_qos = fastdds.TopicQos()
participant.get_default_topic_qos(topic_qos)
topic = participant.create_topic("myTopic", topic_data_type.getName(), topic_qos)

subscriber_qos = fastdds.SubscriberQos()
participant.get_default_subscriber_qos(subscriber_qos)
subscriber = participant.create_subscriber(subscriber_qos)

reader_qos = fastdds.DataReaderQos()
subscriber.get_default_datareader_qos(reader_qos)
reader = subscriber.create_datareader(topic, reader_qos)
```

### Reading a sample

You can read a sample the same way you would do it in C++:

```python
info = fastdds.SampleInfo()
data = HelloWorld.HelloWorld()
reader.take_next_sample(data, info)

print("Received {message} : {index}".format(message=data.message(), index=data.index()))
```
