# Copyright 2022 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import TestTypes
from os import getpid

def get_port() :
    port = getpid()
    if (5000 > port) :
        port += 5000

    print("Generating port {}".format(port))
    return port

global_port = get_port()
enable_datasharing = False
use_pull_mode = False
use_udpv4 = True


#****** Auxiliary print functions  ******#
def default_receive_print(data) :
    if isinstance(data, TestTypes.HelloWorld):
        print("Received HelloWorld {}".format(data.message()))
    if isinstance(data, TestTypes.Data64kb):
        print("Received Data64kb {}".format(data.data()[0]))

def default_send_print(data) :
    if isinstance(data, TestTypes.HelloWorld):
        print("Sent HelloWorld {}".format(data.index()))
    if isinstance(data, TestTypes.Data64kb):
        print("Sent Data64kb {}".format(data.data()[0]))

#****** Auxiliary data generators *******#
def default_helloworld_data_generator(max = 0) :
    if (max == 0) :
        max = 10

    ret = []
    index = 1
    while(index <= max) :
        msg = TestTypes.HelloWorld()
        msg.index(index)
        msg.message("HelloWorld {}".format(index))
        ret.append(msg)
        index += 1

    return ret

data64kb_length = 63996
def default_data64kb_data_generator(max = 0) :
    if (max == 0) :
        max = 10

    ret = []
    index = 1
    while(index <= max) :
        msg = TestTypes.Data64kb()
        msg.data().resize(data64kb_length)
        msg.data()[0] = index
        i = 1
        while(i < data64kb_length) :
            msg.data()[i] = (index + i) % 255
            i += 1
        ret.append(msg)
        index += 1

    return ret
