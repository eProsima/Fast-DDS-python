// Copyright 2016 Proyectos y Sistemas de Mantenimiento SL (eProsima).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*!
 * @file HelloWorldTopicDataType.h
 * This header file contains the declaration of the serialization functions.
 */


#ifndef _HELLOWORLD_TOPICDATATYPE_H_
#define _HELLOWORLD_TOPICDATATYPE_H_

#include <fastdds/dds/topic/TopicDataType.hpp>

#include "HelloWorld.h"

class HelloWorldTopicDataType : public eprosima::fastdds::dds::TopicDataType {
public:
    typedef HelloWorld type;

    HelloWorldTopicDataType();

    virtual ~HelloWorldTopicDataType();

    bool serialize(
            void *data,
            eprosima::fastrtps::rtps::SerializedPayload_t *payload) override;

    bool deserialize(
            eprosima::fastrtps::rtps::SerializedPayload_t *payload,
            void *data) override;

    std::function<uint32_t()> getSerializedSizeProvider(
            void* data) override;

    bool getKey(
            void *data,
            eprosima::fastrtps::rtps::InstanceHandle_t *ihandle,
            bool force_md5 = false) override;

    virtual void* createData() override;

    virtual void deleteData(
            void * data) override;

    MD5 m_md5;
    unsigned char* m_keyBuffer;
};

#endif // _HELLOWORLD_TOPICDATATYPE_H_
