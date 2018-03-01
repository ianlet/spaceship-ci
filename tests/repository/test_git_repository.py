import os
import shutil
from unittest import TestCase

import git
from git import Repo
from mockito import verify, patch, when

from challenge import Submission, Challenge
from repository import GitRepository


class TestGitRepository(TestCase):
    ORG_NAME = 'org-name'
    CHALLENGE_NAME = 'challenge-name'
    SUBMISSION_NAME = 'submission-01'
    SUBMISSION_URL = 'git@github.com:org/submission.git'
    BASE_PATH = 'tests'

    challenge = Challenge(ORG_NAME, CHALLENGE_NAME)
    submission = Submission(SUBMISSION_NAME, SUBMISSION_URL, challenge)
    submission_path = f'{BASE_PATH}/{submission.path}'

    def setUp(self):
        patch(git.Repo.clone_from, lambda a, b: '')

        self.repository = GitRepository(self.BASE_PATH)

    def test_clone_from_submission_url_into_path(self):
        self.repository.clone(self.submission)

        verify(Repo).clone_from(self.SUBMISSION_URL, self.submission_path)

    def test_old_submission_is_cleared_given_it_already_exists(self):
        patch(shutil.rmtree, lambda str: '')
        when(os.path).exists(self.submission_path).thenReturn(True)

        self.repository.clone(self.submission)

        verify(shutil).rmtree(self.submission_path)
