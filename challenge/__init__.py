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
            self.__clone_or_update_assignment(assignment, assignment_path)

    def __clone_or_update_assignment(self, assignment, assignment_path):
        if os.path.exists(assignment_path):
            self.__update_assignment(assignment, assignment_path)
        else:
            self.__clone_assignment(assignment, assignment_path)

    def __clone_assignment(self, assignment, assignment_path):
        print(f'Cloning assignment {assignment.name} into {assignment_path}...')
        assignment_repo = Repo.clone_from(assignment.url, assignment_path)
        print(f'Assignment cloned!')

        print(f'Checking out {assignment.name} to master...')
        assignment_repo.heads.master.checkout()

    def __update_assignment(self, assignment, assignment_path):
        print(f'Assignment {assignment.name} already exists at {assignment_path}')

        print(f'Checking out {assignment.name} to master...')
        assignment_repo = Repo(assignment_path)
        assignment_repo.heads.master.checkout()

        print(f'Updating assignment {assignment.name}...')
        origin = assignment_repo.remote('origin')
        origin.pull(['--ff', '--force'])

        print(f'Assignment updated!')

    def __ensure_exists(self, challenge_path):
        if not os.path.exists(challenge_path):
            os.makedirs(challenge_path)


class Assignment:
    def __init__(self, name, url):
        self.name = name
        self.url = url
