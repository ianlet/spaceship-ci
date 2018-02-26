from challenge import Challenge
from challenge.assignment import Assignment


class ChallengeRepositoryGithub:
    def __init__(self, github, docker):
        self.github = github
        self.docker = docker

    def find_by_name_and_org(self, name, organization):
        assignments = self.__find_assignments(name, organization)
        return Challenge(name, organization, assignments)

    def __find_assignments(self, challenge_name, organization):
        org = self.github.get_organization(organization)
        repos = org.get_repos()
        assignment_repos = [repo for repo in repos if repo.name.startswith(challenge_name)]
        assignments = []
        for repo in assignment_repos:
            assignment_name = repo.name.replace(f'{challenge_name}-', '')
            git_url = repo.ssh_url
            assignment = Assignment(self.docker, assignment_name, git_url)
            assignments.append(assignment)
        return assignments
