# Python binding for Fast DDS Statistics Backend

# HelloWorldExample

## Prerequisites

* Compile and install the Fast DDS python wrappers
* If colcon is used, source your installation environment

## Compile and install the example

Use colcon to build the example. You will need to source the installation environment afterwards.
```bash
colcon build
source install/setup.bash
```

## Execute the example

Open two terminals

On one terminal run the publisher:
```bash
python3 HelloWorldExample.py -p publisher
```

On the other one run the subscriber:
```bash
python3 HelloWorldExample.py -p subscriber
```
