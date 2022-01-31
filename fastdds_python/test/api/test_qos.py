import fastdds

def test_participant_qos():
    # DomainParticipantQos
    participant_qos = fastdds.DomainParticipantQos()

    # .name
    participant_qos.name("test name")
    assert("test name" == participant_qos.name())

    factory = fastdds.DomainParticipantFactory.get_instance()
    factory.set_default_participant_qos(participant_qos)

    default_participant_qos = fastdds.DomainParticipantQos()
    factory.get_default_participant_qos(default_participant_qos)

    print('adios {}'.format(participant_qos.name()))
    print('hola {}'.format(default_participant_qos.name()))

    assert("test name" == default_participant_qos.name())
