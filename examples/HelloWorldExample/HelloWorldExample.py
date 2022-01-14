# Copyright 2021 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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
"""
Script to test Fast DDS python bindings
"""
import argparse
import signal
from threading import Condition

import fastdds
import HelloWorld

DESCRIPTION = """HelloWorld example for Fast DDS python bindings"""
USAGE = ('python3 HelloWorldExample.py -p publisher|subscriber [-d domainID -m machineID]')

# To capture ctrl+C
def signal_handler(sig, frame):
    print('Interrupted!')

class ReaderListener(fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()

    def on_data_available(self, reader):
        info = fastdds.SampleInfo()
        data = HelloWorld.HelloWorld()
        reader.take_next_sample(data, info)
    
        print("Received {message} : {index}".format(message=data.message(), index=data.index()))

    def on_subscription_matched(self, datareader, info) :
        if (0 < info.current_count_change) :
            print ("Subscriber matched publisher {}".format(info.last_publication_handle))
        else :
            print ("Subscriber unmatched publisher {}".format(info.last_publication_handle))

class WriterListener (fastdds.DataWriterListener) :
    def __init__(self, writer) :
        self._writer = writer
        super().__init__()

    def on_publication_matched(self, datawriter, info) :
        if (0 < info.current_count_change) :
            print ("Publisher matched subscriber {}".format(info.last_subscription_handle))
            self._writer._cvDiscovery.acquire()
            self._writer._matched_reader += 1
            self._writer._cvDiscovery.notify()
            self._writer._cvDiscovery.release()
        else :
            print ("Publisher unmatched subscriber {}".format(info.last_subscription_handle))
            self._writer._cvDiscovery.acquire()
            self._writer._matched_reader += 1
            self._writer._cvDiscovery.notify()
            self._writer._cvDiscovery.release()


class Reader():
  def __init__(self, domain):
    factory = fastdds.DomainParticipantFactory.get_instance()
    self.participant_qos = fastdds.DomainParticipantQos()
    factory.get_default_participant_qos(self.participant_qos)
    self.participant = factory.create_participant(domain, self.participant_qos)

    self.topic_data_type = HelloWorld.HelloWorldPubSubType()
    self.topic_data_type.setName("HelloWorldDataType")
    self.type_support = fastdds.TypeSupport(self.topic_data_type)
    self.participant.register_type(self.type_support)

    self.topic_qos = fastdds.TopicQos()
    self.participant.get_default_topic_qos(self.topic_qos)
    self.topic = self.participant.create_topic("myTopic", self.topic_data_type.getName(), self.topic_qos)

    self.subscriber_qos = fastdds.SubscriberQos()
    self.participant.get_default_subscriber_qos(self.subscriber_qos)
    self.subscriber = self.participant.create_subscriber(self.subscriber_qos)

    self.listener = ReaderListener()
    self.reader_qos = fastdds.DataReaderQos()
    self.subscriber.get_default_datareader_qos(self.reader_qos)
    self.reader = self.subscriber.create_datareader(self.topic, self.reader_qos, self.listener)

  def delete(self):
    factory = fastdds.DomainParticipantFactory.get_instance()
    self.participant.delete_contained_entities()
    factory.delete_participant(self.participant)

  def run(self):
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to stop')
    signal.pause()
    self.delete()

class Writer:
  def __init__(self, domain, machine):
    self.machine = machine
    self._matched_reader = 0
    self._cvDiscovery = Condition()

    factory = fastdds.DomainParticipantFactory.get_instance()
    self.participant_qos = fastdds.DomainParticipantQos()
    factory.get_default_participant_qos(self.participant_qos)
    self.participant = factory.create_participant(domain, self.participant_qos)

    self.topic_data_type = HelloWorld.HelloWorldPubSubType()
    self.topic_data_type.setName("HelloWorldDataType")
    self.type_support = fastdds.TypeSupport(self.topic_data_type)
    self.participant.register_type(self.type_support)

    self.topic_qos = fastdds.TopicQos()
    self.participant.get_default_topic_qos(self.topic_qos)
    self.topic = self.participant.create_topic("myTopic", self.topic_data_type.getName(), self.topic_qos)

    self.publisher_qos = fastdds.PublisherQos()
    self.participant.get_default_publisher_qos(self.publisher_qos)
    self.publisher = self.participant.create_publisher(self.publisher_qos)

    self.listener = WriterListener(self)
    self.writer_qos = fastdds.DataWriterQos()
    self.publisher.get_default_datawriter_qos(self.writer_qos)
    self.writer = self.publisher.create_datawriter(self.topic, self.writer_qos, self.listener)
    
    self.index = 0

  def write(self):
    data = HelloWorld.HelloWorld()
    if self.machine:
      data.message("Hello World " + self.machine)
    else:
      data.message("Hello World")
    data.index(self.index)
    self.writer.write(data)
    print("Sending {message} : {index}".format(message=data.message(), index=data.index()))
    self.index = self.index + 1

  def delete(self):
    factory = fastdds.DomainParticipantFactory.get_instance()
    self.participant.delete_contained_entities()
    factory.delete_participant(self.participant)

  def run(self):
    self.wait_discovery()
    for x in range(10) :
        self.write()
    self.delete()

  def wait_discovery(self) :
    self._cvDiscovery.acquire()
    print ("Writer is waiting discovery...")
    self._cvDiscovery.wait_for(lambda : self._matched_reader != 0)
    self._cvDiscovery.release()
    print("Writer discovery finished...")


def parse_options():
  """"
  Parse arguments.

  :return: Parsed arguments.
  """
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    add_help=True,
    description=(DESCRIPTION),
    usage=(USAGE)
  )
  required_args = parser.add_argument_group('required arguments')
  required_args.add_argument(
    '-d',
    '--domain',
    type=int,
    required=False,
    help='DomainID.'
  )
  required_args.add_argument(
    '-p',
    '--parameter',
    type=str,
    required=True,
    help='Whether the application is run as publisher or subscriber.'
  )
  required_args.add_argument(
    '-m',
    '--machine',
    type=str,
    required=False,
    help='Distinguish the machine publishing. Only applies if the application is run as publisher.'

  )
  return parser.parse_args()

if __name__ == '__main__':
  # Parse arguments
  args = parse_options()
  if not args.domain:
    args.domain = 0

  if args.parameter == 'publisher':
    print('Creating publisher.')
    writer = Writer(args.domain, args.machine)
    writer.run()
  elif args.parameter == 'subscriber':
    print('Creating subscriber.')
    reader = Reader(args.domain)
    reader.run()
  else:
    print('Error: Incorrect arguments.')
    print(USAGE)

  exit()
