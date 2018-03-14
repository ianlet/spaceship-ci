from unittest import TestCase

from mockito import verify, mock, when

from challenge.challenge import Challenge
from challenge.submission import Submission
from verification.track_progress_stage import TrackProgressStage


class TestTrackProgressStage(TestCase):
    ORG_NAME = 'org-name'
    CHALLENGE_NAME = 'challenge-name'
    SUBMISSION_NAME = 'submission-01'
    SUBMISSION_URL = 'git@github.com:org/submission.git'
    BASE_PATH = 'tests'
    MONGO_HOST = 'mongo'

    CONTAINER_COMMAND = ['./gradlew', 'accept', f'-DteamToken={SUBMISSION_NAME}', f'-DmongoHost={MONGO_HOST}']

    challenge = Challenge(ORG_NAME, CHALLENGE_NAME)
    submission = Submission(SUBMISSION_NAME, SUBMISSION_URL, challenge)
    submission_path = f'{BASE_PATH}/{submission.path}'
    container_name = f'{submission.slug}--track-progress'

    def setUp(self):
        self.executor = mock()
        self.container = self.__setup_container()

        self.stage = TrackProgressStage(self.BASE_PATH, self.executor, self.MONGO_HOST)

    def test_the_container_is_run(self):
        self.stage.execute(self.submission)

        verify(self.container).run()

    def __setup_container(self):
        the_container = mock()
        when(self.executor).create_container(self.submission.slug, self.container_name, self.CONTAINER_COMMAND,
                                             self.submission_path).thenReturn(the_container)
        return the_container
