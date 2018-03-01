from challenge import Submission


class SubmissionRepositoryGithub:
    def __init__(self, github):
        self.github = github

    def find_by_challenge(self, challenge):
        org = self.github.get_organization(challenge.org)
        repos = org.get_repos()
        submission_repos = [repo for repo in repos if repo.name.startswith(challenge.name)]
        submissions = []
        for repo in submission_repos:
            submission_name = repo.name.replace(f'{challenge.name}-', '')
            git_url = repo.ssh_url
            submission = Submission(submission_name, git_url, challenge)
            submissions.append(submission)
        return submissions
