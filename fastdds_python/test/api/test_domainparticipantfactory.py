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
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))

    # Overload 2
    listener = fastdds.DomainParticipantListener()
    participant = factory.create_participant(
            0, fastdds.PARTICIPANT_QOS_DEFAULT, listener)
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        participant = factory.create_participant(
                0, fastdds.PARTICIPANT_QOS_DEFAULT, listener, status_mask_1)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(status_mask_1 == participant.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               factory.delete_participant(participant))
        participant = factory.create_participant(
                0, fastdds.PARTICIPANT_QOS_DEFAULT, listener, status_mask_2)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(status_mask_1 == participant.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               factory.delete_participant(participant))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), None)
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), listener)
    test(fastdds.StatusMask.none(), fastdds.StatusMask_none(), listener)
    test(fastdds.StatusMask.data_available(),
         fastdds.StatusMask_data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(),
         fastdds.StatusMask_data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(),
         fastdds.StatusMask_inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(),
         fastdds.StatusMask_liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(),
         fastdds.StatusMask_liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(),
         fastdds.StatusMask_offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(),
         fastdds.StatusMask_offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(),
         fastdds.StatusMask_publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(),
         fastdds.StatusMask_requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(),
         fastdds.StatusMask_requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(),
         fastdds.StatusMask_sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(),
         fastdds.StatusMask_sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(),
         fastdds.StatusMask_subscription_matched(), listener)

    m = fastdds.StatusMask_data_available() << \
        fastdds.StatusMask_data_on_readers() << \
        fastdds.StatusMask_inconsistent_topic() << \
        fastdds.StatusMask_liveliness_changed() << \
        fastdds.StatusMask_liveliness_lost() << \
        fastdds.StatusMask_offered_deadline_missed() << \
        fastdds.StatusMask_offered_incompatible_qos() << \
        fastdds.StatusMask_publication_matched() << \
        fastdds.StatusMask_requested_deadline_missed() << \
        fastdds.StatusMask_requested_incompatible_qos() << \
        fastdds.StatusMask_sample_lost() << \
        fastdds.StatusMask_sample_rejected() << \
        fastdds.StatusMask_subscription_matched()

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
         m,
         listener)


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

    # Overload 1
    participant = factory.create_participant_with_profile(
            'test_participant_profile')
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(3 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
    participant = factory.create_participant_with_profile(
            0, 'test_participant_profile')
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(0 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
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
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))
    participant = factory.create_participant_with_profile(
            0, 'test_participant_profile', listener)
    assert(participant is not None)
    assert(participant.is_enabled())
    assert(0 == participant.get_domain_id())
    qos = participant.get_qos()
    assert('test_name' == qos.name())
    assert(fastdds.StatusMask.all() == participant.get_status_mask())
    assert(fastdds.ReturnCode_t.RETCODE_OK ==
           factory.delete_participant(participant))

    def test(status_mask_1, status_mask_2, listnr=None):
        """
        Test the entity creation using the two types of StatusMasks.
        """
        participant = factory.create_participant_with_profile(
                'test_participant_profile', listener, status_mask_1)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(3 == participant.get_domain_id())
        qos = participant.get_qos()
        assert('test_name' == qos.name())
        assert(status_mask_1 == participant.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               factory.delete_participant(participant))
        participant = factory.create_participant_with_profile(
                0, 'test_participant_profile', listener, status_mask_1)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(0 == participant.get_domain_id())
        qos = participant.get_qos()
        assert('test_name' == qos.name())
        assert(status_mask_1 == participant.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               factory.delete_participant(participant))
        participant = factory.create_participant_with_profile(
                'test_participant_profile', listener, status_mask_2)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(3 == participant.get_domain_id())
        qos = participant.get_qos()
        assert('test_name' == qos.name())
        assert(status_mask_1 == participant.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               factory.delete_participant(participant))
        participant = factory.create_participant_with_profile(
                0, 'test_participant_profile', listener, status_mask_2)
        assert(participant is not None)
        assert(participant.is_enabled())
        assert(0 == participant.get_domain_id())
        qos = participant.get_qos()
        assert('test_name' == qos.name())
        assert(status_mask_1 == participant.get_status_mask())
        assert(fastdds.ReturnCode_t.RETCODE_OK ==
               factory.delete_participant(participant))

    # Overload 3: Different status masks
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), None)
    test(fastdds.StatusMask.all(), fastdds.StatusMask_all(), listener)
    test(fastdds.StatusMask.none(), fastdds.StatusMask_none(), listener)
    test(fastdds.StatusMask.data_available(),
         fastdds.StatusMask_data_available(), listener)
    test(fastdds.StatusMask.data_on_readers(),
         fastdds.StatusMask_data_on_readers(), listener)
    test(fastdds.StatusMask.inconsistent_topic(),
         fastdds.StatusMask_inconsistent_topic(), listener)
    test(fastdds.StatusMask.liveliness_changed(),
         fastdds.StatusMask_liveliness_changed(), listener)
    test(fastdds.StatusMask.liveliness_lost(),
         fastdds.StatusMask_liveliness_lost(), listener)
    test(fastdds.StatusMask.offered_deadline_missed(),
         fastdds.StatusMask_offered_deadline_missed(), listener)
    test(fastdds.StatusMask.offered_incompatible_qos(),
         fastdds.StatusMask_offered_incompatible_qos(), listener)
    test(fastdds.StatusMask.publication_matched(),
         fastdds.StatusMask_publication_matched(), listener)
    test(fastdds.StatusMask.requested_deadline_missed(),
         fastdds.StatusMask_requested_deadline_missed(), listener)
    test(fastdds.StatusMask.requested_incompatible_qos(),
         fastdds.StatusMask_requested_incompatible_qos(), listener)
    test(fastdds.StatusMask.sample_lost(),
         fastdds.StatusMask_sample_lost(), listener)
    test(fastdds.StatusMask.sample_rejected(),
         fastdds.StatusMask_sample_rejected(), listener)
    test(fastdds.StatusMask.subscription_matched(),
         fastdds.StatusMask_subscription_matched(), listener)

    m = fastdds.StatusMask_data_available() << \
        fastdds.StatusMask_data_on_readers() << \
        fastdds.StatusMask_inconsistent_topic() << \
        fastdds.StatusMask_liveliness_changed() << \
        fastdds.StatusMask_liveliness_lost() << \
        fastdds.StatusMask_offered_deadline_missed() << \
        fastdds.StatusMask_offered_incompatible_qos() << \
        fastdds.StatusMask_publication_matched() << \
        fastdds.StatusMask_requested_deadline_missed() << \
        fastdds.StatusMask_requested_incompatible_qos() << \
        fastdds.StatusMask_sample_lost() << \
        fastdds.StatusMask_sample_rejected() << \
        fastdds.StatusMask_subscription_matched()

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
         m,
         listener)
