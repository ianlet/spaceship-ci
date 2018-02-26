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
            assignment.clone_or_update(challenge_path)

    def __ensure_exists(self, challenge_path):
        if not os.path.exists(challenge_path):
            os.makedirs(challenge_path)


class Assignment:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def clone_or_update(self, base_path):
        path = f'{base_path}/{self.name}'
        if os.path.exists(path):
            print(f'Assignment {self.name} already exists at {path}')
            self.__update(path)
        else:
            self.__clone(path)

    def __clone(self, path):
        print(f'Cloning assignment {self.name} into {path}...')
        assignment_repo = Repo.clone_from(self.url, path)
        print(f'Assignment cloned!')

        print(f'Checking out {self.name} to master...')
        assignment_repo.heads.master.checkout()

    def __update(self, path):
        print(f'Checking out {self.name} to master...')
        assignment_repo = Repo(path)
        assignment_repo.heads.master.checkout()

        print(f'Updating assignment {self.name}...')
        origin = assignment_repo.remote('origin')
        origin.pull(['--ff', '--force'])

        print(f'Assignment updated!')
