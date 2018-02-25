import os

from git import Repo


class Challenge:
    def __init__(self, name, organization, assignments):
        self.name = name
        self.organization = organization
        self.assignments = assignments

    def run_pipeline(self, base_path):
        print(f'Starting pipeline for challenge {self.organization}/{self.name}...')
        challenge_path = f'{base_path}/{self.organization}-{self.name}'
        self.__ensure_exists(challenge_path)

        for assignment in self.assignments:
            assignment_path = f'{challenge_path}/{assignment.name}'
            print(f'Cloning assignment {assignment.name} into {assignment_path}...')
            assignment_repo = Repo.clone_from(assignment.url, assignment_path)
            print(f'Assignment cloned!')

    def __ensure_exists(self, challenge_path):
        if not os.path.exists(challenge_path):
            os.makedirs(challenge_path)


class Assignment:
    def __init__(self, name, url):
        self.name = name
        self.url = url
