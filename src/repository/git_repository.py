import os
import shutil

from git import Repo


class GitRepository:
    def __init__(self, base_path):
        self.base_path = base_path

    def clone(self, submission):
        submission_path = f'{self.base_path}/{submission.path}'
        if os.path.exists(submission_path):
            shutil.rmtree(submission_path)
        Repo.clone_from(submission.url, submission_path)
