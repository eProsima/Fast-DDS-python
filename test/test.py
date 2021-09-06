import fastdds_wrapper
import topic_types

class Reader:
  def __init__(self, domain):
    factory = fastdds_wrapper.DomainParticipantFactory.get_instance()
    self.participant_qos = fastdds_wrapper.DomainParticipantQos()
    factory.get_default_participant_qos(self.participant_qos)
    self.participant = factory.create_participant(5, self.participant_qos)

    self.topic_data_type = topic_types.HelloWorldTopicDataType()
    self.topic_data_type.setName("HelloWorldDataType")
    self.type_support = fastdds_wrapper.TypeSupport(self.topic_data_type)
    self.participant.register_type(self.type_support)

    self.topic_qos = fastdds_wrapper.TopicQos()
    self.participant.get_default_topic_qos(self.topic_qos)
    self.topic = self.participant.create_topic("myTopic", self.topic_data_type.getName(), self.topic_qos)

    self.subscriber_qos = fastdds_wrapper.SubscriberQos()
    self.participant.get_default_subscriber_qos(self.subscriber_qos)
    self.subscriber = self.participant.create_subscriber(self.subscriber_qos)

    self.reader_qos = fastdds_wrapper.DataReaderQos()
    self.subscriber.get_default_datareader_qos(self.reader_qos)
    self.reader = self.subscriber.create_datareader(self.topic, self.reader_qos)

  def read(self):
    info = fastdds_wrapper.SampleInfo()
    data = topic_types.HelloWorld()
    self.reader.take_next_sample(data, info)
    
    print("Received {message} : {index}".format(message=data.get_message(), index=data.get_index()))


class Writer:
  def __init__(self, domain):
    factory = fastdds_wrapper.DomainParticipantFactory.get_instance()
    self.participant_qos = fastdds_wrapper.DomainParticipantQos()
    factory.get_default_participant_qos(self.participant_qos)
    self.participant = factory.create_participant(5, self.participant_qos)

    self.topic_data_type = topic_types.HelloWorldTopicDataType()
    self.topic_data_type.setName("HelloWorldDataType")
    self.type_support = fastdds_wrapper.TypeSupport(self.topic_data_type)
    self.participant.register_type(self.type_support)

    self.topic_qos = fastdds_wrapper.TopicQos()
    self.participant.get_default_topic_qos(self.topic_qos)
    self.topic = self.participant.create_topic("myTopic", self.topic_data_type.getName(), self.topic_qos)

    self.publisher_qos = fastdds_wrapper.PublisherQos()
    self.participant.get_default_publisher_qos(self.publisher_qos)
    self.publisher = self.participant.create_publisher(self.publisher_qos)

    self.writer_qos = fastdds_wrapper.DataWriterQos()
    self.publisher.get_default_datawriter_qos(self.writer_qos)
    self.writer = self.publisher.create_datawriter(self.topic, self.writer_qos)
    
    self.index = 0

  def write(self):
    data = topic_types.HelloWorld()
    data.set_message("Hello World")
    data.set_index(self.index)
    self.writer.write(data)
    print("Sending {message} : {index}".format(message=data.get_message(), index=data.get_index()))
    self.index = self.index + 1

