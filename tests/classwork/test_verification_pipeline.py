from unittest import TestCase

from mockito import verify, mock, when

from classwork import Classwork, Assignment, VerificationPipeline
from classwork.verification_stage import VerificationStageFailed, VerificationStageStatus, VerificationStageEvent


class TestVerificationPipeline(TestCase):
    A_STAGE_NAME = 'build'
    VERIFICATION_STAGE_STARTED = VerificationStageStatus.STARTED
    VERIFICATION_STAGE_SUCCEEDED = VerificationStageStatus.SUCCEEDED
    VERIFICATION_STAGE_FAILED = VerificationStageStatus.FAILED

    assignment = Assignment('org-name', 'assignment-name')
    classwork = Classwork(assignment)

    verification_stage_started_event = VerificationStageEvent(A_STAGE_NAME, classwork.name, VERIFICATION_STAGE_STARTED)
    verification_stage_succeeded_event = VerificationStageEvent(A_STAGE_NAME, classwork.name,
                                                                VERIFICATION_STAGE_SUCCEEDED)
    verification_stage_failed_event = VerificationStageEvent(A_STAGE_NAME, classwork.name, VERIFICATION_STAGE_FAILED)

    def setUp(self):
        self.failed_verification_stage = self.__setup_failed_verification_stage()

        self.first_verification_stage = self.__setup_succeeded_verification_stage()
        self.second_verification_stage = self.__setup_succeeded_verification_stage()

        self.event_store = mock()

    def test_each_verification_stage_is_executed_for_the_classwork(self):
        some_verification_stages = [self.first_verification_stage, self.second_verification_stage]
        pipeline = VerificationPipeline(self.event_store, some_verification_stages)

        pipeline.verify(self.classwork)

        for stage in some_verification_stages:
            verify(stage, inorder=True).execute(self.classwork)

    def test_store_verification_stage_started_event(self):
        pipeline = VerificationPipeline(self.event_store, [self.first_verification_stage])

        pipeline.verify(self.classwork)

        verify(self.event_store).store(self.verification_stage_started_event)

    def test_store_verification_stage_succeeded_event(self):
        pipeline = VerificationPipeline(self.event_store, [self.first_verification_stage])

        pipeline.verify(self.classwork)

        verify(self.event_store).store(self.verification_stage_succeeded_event)

    def test_second_verification_stage_is_not_executed_given_first_verification_stage_failed(self):
        verification_stages = [self.failed_verification_stage, self.second_verification_stage]
        pipeline = VerificationPipeline(self.event_store, verification_stages)

        pipeline.verify(self.classwork)

        verify(self.second_verification_stage, times=0).execute(self.classwork)

    def test_store_verification_staged_failed_event_given_verification_stage_failed(self):
        pipeline = VerificationPipeline(self.event_store, [self.failed_verification_stage])

        pipeline.verify(self.classwork)

        verify(self.event_store).store(self.verification_stage_failed_event)

    def __setup_succeeded_verification_stage(self):
        stage = mock({'name': self.A_STAGE_NAME})
        return stage

    def __setup_failed_verification_stage(self):
        stage = mock({'name': self.A_STAGE_NAME})
        when(stage).execute(self.classwork).thenRaise(VerificationStageFailed(stage))
        return stage
