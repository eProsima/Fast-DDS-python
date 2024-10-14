import fastdds


def test_create_participant():
    """
    This test checks:
    - DomainParticipantFactory::create_participant
    - DomainParticipantFactory::delete_participant
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()

    # Overload 1
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT)
    assert(participant.is_enabled())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(participant is not None)
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))

    # Overload 2
    listener = fastdds.DomainParticipantListener()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT, listener)
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))

    def test(status_mask, listnr=None):
        """
        Test the entity creation using the type of StatusMask.
        """
        participant = factory.create_participant(
                0, fastdds.PARTICIPANT_QOS_DEFAULT, listnr, status_mask)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(status_mask == participant.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               factory.delete_participant(participant))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), None)
    test(fastdds.StatusMask.all(), listener)
    test(fastdds.StatusMask.none(), listener)
    test(fastdds.StatusMask.data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(), listener)

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched(),
         listener)

    # Overload 4
    extended_qos = fastdds.DomainParticipantExtendedQos()
    participant = factory.create_participant(
            extended_qos)
    assert(participant.is_enabled())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(participant is not None)
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))


def test_create_participant_with_profile():
    """
    This test checks:
    - DomainParticipantFactory::create_participant_with_profile
    - DomainParticipantFactory::delete_participant
    - Publisher::get_status_mask
    - StatusMask::operator ==
    - StatusMask::operator <<
    """
    factory = fastdds.DomainParticipantFactory.get_instance()

    # Failure
    participant = factory.create_participant_with_profile(
            'no_exists_profile')
    assert(participant is None)
    participant = factory.create_participant_with_profile(
            0, 'no_exists_profile')
    assert(participant is None)

    # Overload 1
    participant = factory.create_participant_with_profile(
            'test_participant_profile')
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(3 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))
    participant = factory.create_participant_with_profile(
            0, 'test_participant_profile')
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(0 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))

    # Overload 2
    listener = fastdds.DomainParticipantListener()
    participant = factory.create_participant_with_profile(
            'test_participant_profile', listener)
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(3 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))
    participant = factory.create_participant_with_profile(
            0, 'test_participant_profile', listener)
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(0 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.RETCODE_OK ==
           factory.delete_participant(participant))

    def test(status_mask, listnr=None):
        """
        Test the entity creation using the type of StatusMask.
        """
        participant = factory.create_participant_with_profile(
                'test_participant_profile', listnr, status_mask)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(3 == participant.get_domain_id())
        qos = participant.get_qos()
        assert('test_name' == qos.name())
        assert(status_mask == participant.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               factory.delete_participant(participant))
        participant = factory.create_participant_with_profile(
                0, 'test_participant_profile', listnr, status_mask)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(0 == participant.get_domain_id())
        qos = participant.get_qos()
        assert('test_name' == qos.name())
        assert(status_mask == participant.get_status_mask())
        assert(fastdds.RETCODE_OK ==
               factory.delete_participant(participant))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(),  None)
    test(fastdds.StatusMask.all(),  listener)
    test(fastdds.StatusMask.none(),  listener)
    test(fastdds.StatusMask.data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(), listener)

    test(fastdds.StatusMask.data_available() <<
         fastdds.StatusMask.data_on_readers() <<
         fastdds.StatusMask.inconsistent_topic() <<
         fastdds.StatusMask.liveliness_changed() <<
         fastdds.StatusMask.liveliness_lost() <<
         fastdds.StatusMask.offered_deadline_missed() <<
         fastdds.StatusMask.offered_incompatible_qos() <<
         fastdds.StatusMask.publication_matched() <<
         fastdds.StatusMask.requested_deadline_missed() <<
         fastdds.StatusMask.requested_incompatible_qos() <<
         fastdds.StatusMask.sample_lost() <<
         fastdds.StatusMask.sample_rejected() <<
         fastdds.StatusMask.subscription_matched(),
         listener)

def test_get_participant_qos_from_xml():

    with open("test_xml_profile.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    factory = fastdds.DomainParticipantFactory.get_instance()

    qos = fastdds.DomainParticipantQos()
    ret = factory.get_participant_qos_from_xml(
            xml_content, qos, 'test_participant_profile')
    assert(fastdds.RETCODE_OK == ret)

    qos_no_name = fastdds.DomainParticipantQos()
    ret = factory.get_participant_qos_from_xml(
            xml_content, qos_no_name)
    assert(fastdds.RETCODE_OK == ret)

    # Non matching name takes the first participant found (the only one)
    assert(qos == qos_no_name)

def test_get_default_participant_qos_from_xml():

    with open("test_xml_profile.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    factory = fastdds.DomainParticipantFactory.get_instance()

    default_qos = fastdds.DomainParticipantQos()
    ret = factory.get_default_participant_qos_from_xml(
            xml_content, default_qos)
    assert(fastdds.RETCODE_OK == ret)

    qos = fastdds.DomainParticipantQos()
    ret = factory.get_participant_qos_from_xml(
            xml_content, qos, 'test_participant_profile')
    assert(fastdds.RETCODE_OK == ret)

    assert(default_qos == qos)

def test_get_participant_extended_qos_from_xml():

    with open("test_xml_profile.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    factory = fastdds.DomainParticipantFactory.get_instance()

    qos = fastdds.DomainParticipantExtendedQos()
    ret = factory.get_participant_extended_qos_from_xml(
            xml_content, qos, 'test_participant_profile')
    assert(fastdds.RETCODE_OK == ret)

    qos_no_name = fastdds.DomainParticipantExtendedQos()
    ret = factory.get_participant_extended_qos_from_xml(
            xml_content, qos_no_name)
    assert(fastdds.RETCODE_OK == ret)

    # Non matching name takes the first participant found (the only one)
    assert(qos == qos_no_name)

def test_get_default_participant_extended_qos_from_xml():

    with open("test_xml_profile.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    factory = fastdds.DomainParticipantFactory.get_instance()

    default_qos = fastdds.DomainParticipantExtendedQos()
    ret = factory.get_default_participant_extended_qos_from_xml(
            xml_content, default_qos)
    assert(fastdds.RETCODE_OK == ret)

    qos = fastdds.DomainParticipantExtendedQos()
    ret = factory.get_participant_extended_qos_from_xml(
            xml_content, qos, 'test_participant_profile')
    assert(fastdds.RETCODE_OK == ret)

    assert(default_qos == qos)
