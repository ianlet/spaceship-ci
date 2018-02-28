from unittest import TestCase

from mockito import verify, mock, when

from classwork import Classwork, Assignment, VerificationPipeline
from classwork.verification_stage import VerificationStageFailed


class TestVerificationPipeline(TestCase):
    assignment = Assignment('org-name', 'assignment_name')
    classwork = Classwork(assignment)

    def setUp(self):
        self.failed_verification_stage = self.__setup_failed_verification_stage()

        self.first_verification_stage = self.__setup_succeeded_verification_stage()
        self.second_verification_stage = self.__setup_succeeded_verification_stage()

    def test_each_verification_stage_is_executed_for_the_classwork(self):
        some_verification_stages = [self.first_verification_stage, self.second_verification_stage]
        pipeline = VerificationPipeline(some_verification_stages)

        pipeline.verify(self.classwork)

        for stage in some_verification_stages:
            verify(stage, inorder=True).execute(self.classwork)

    def test_second_verification_stage_is_not_executed_given_first_verification_stage_failed(self):
        verification_stages = [self.failed_verification_stage, self.second_verification_stage]
        pipeline = VerificationPipeline(verification_stages)

        pipeline.verify(self.classwork)

        verify(self.second_verification_stage, times=0).execute(self.classwork)

    def __setup_succeeded_verification_stage(self):
        return mock()

    def __setup_failed_verification_stage(self):
        stage = mock()
        when(stage).execute(self.classwork).thenRaise(VerificationStageFailed())
        return stage
