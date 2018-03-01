from unittest import TestCase

from mockito import mock, when, verify

from challenge.challenge import Challenge
from verification.challenge_verifier import ChallengeVerifier


class TestChallengeVerifier(TestCase):
    the_challenge = Challenge('an-ord', 'a-name')

    submission_repository = mock()
    verification_pipeline = mock()

    def setUp(self):
        verification_pipeline_factory = mock()
        when(verification_pipeline_factory).create().thenReturn(self.verification_pipeline)

        self.challenge_verifier = ChallengeVerifier(self.submission_repository, verification_pipeline_factory)

    def test_verification_pipeline_should_verify_each_submission(self):
        submissions = self.__given_submissions()

        self.challenge_verifier.verify_submissions(self.the_challenge)

        for submission in submissions:
            verify(self.verification_pipeline).verify(submission)

    def __given_submissions(self):
        submissions = [mock(), mock()]
        when(self.submission_repository).find_by_challenge(self.the_challenge).thenReturn(submissions)
        return submissions
