from unittest import TestCase

from mockito import mock, verify, when

from challenge.challenge import Challenge
from challenge.submission import Submission
from verification.build_stage import BuildStage


class TestBuildStage(TestCase):
    ORG_NAME = 'org-name'
    CHALLENGE_NAME = 'challenge-name'
    SUBMISSION_NAME = 'submission-01'
    SUBMISSION_URL = 'git@github.com:org/submission.git'
    BASE_PATH = 'tests'

    CONTAINER_COMMAND = ['./gradlew', 'build', '-x', 'test']

    challenge = Challenge(ORG_NAME, CHALLENGE_NAME)
    submission = Submission(SUBMISSION_NAME, SUBMISSION_URL, challenge)
    submission_path = f'{BASE_PATH}/{submission.path}'
    container_name = f'{submission.slug}--build'

    def setUp(self):
        self.executor = mock()

        self.stage = BuildStage(self.BASE_PATH, self.executor)

    def test_run_submission_container(self):
        container = mock()
        when(self.executor).create_container(self.submission.slug, self.container_name, self.CONTAINER_COMMAND,
                                             self.submission_path).thenReturn(container)

        self.stage.execute(self.submission)

        verify(container).run()
