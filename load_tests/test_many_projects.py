import os
import shutil
from unittest import TestCase

import docker
from mockito import mock, when

from src.challenge.challenge import Challenge
from src.challenge.submission import Submission
from src.executor import DockerExecutor
from src.repository import GitRepository
from src.verification.challenge_verifier import ChallengeVerifier
from src.verification.verification_pipeline import VerificationPipelineFactory


class TestManyProjects(TestCase):
    DUMMY_REPO = 'git@github.com:ianlet/spaceship-control.git'
    BASE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/dummy-repositories'
    MONGO_HOST = 'mongo'

    challenge = Challenge('test', 'load-tests')

    def setUp(self):
        if os.path.exists(self.BASE_PATH):
            shutil.rmtree(self.BASE_PATH)
        os.mkdir(self.BASE_PATH)

    def tearDown(self):
        if os.path.exists(self.BASE_PATH):
            shutil.rmtree(self.BASE_PATH)

    def test_it_should_run_pipeline_for_thirty_projects(self):
        event_store = mock()
        repository = GitRepository(self.BASE_PATH)
        docker_client = docker.from_env()
        executor = DockerExecutor(docker_client, 'gradle:jdk8')
        pipeline_factory = VerificationPipelineFactory(event_store, repository, self.BASE_PATH, executor,
                                                       self.MONGO_HOST)
        submissions = []
        for i in range(0, 30):
            submission_name = f'submission-{i}'
            submissions.append(Submission(submission_name, self.DUMMY_REPO, self.challenge))

        submission_repository = mock()
        when(submission_repository).find_by_challenge(self.challenge).thenReturn(submissions)

        verifier = ChallengeVerifier(submission_repository, pipeline_factory)

        verifier.verify_submissions(self.challenge)
