from unittest import TestCase

from mockito import verify, mock

from challenge.challenge import Challenge
from challenge.submission import Submission
from verification.preparation_stage import PreparationStage


class TestPreparationStage(TestCase):
    challenge = Challenge('org-name', 'challenge-name')
    submission = Submission('submission-01', 'submission-url', challenge)

    repository = mock()

    def setUp(self):
        self.preparation_stage = PreparationStage(self.repository)

    def test_clone_submission_repository(self):
        self.preparation_stage.execute(self.submission)

        verify(self.repository).clone(self.submission)
