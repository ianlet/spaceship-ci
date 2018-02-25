import argparse
import os

from github import Github

from challenge.repository import ChallengeRepositoryGithub

# import docker
# client = docker.from_env()
# container = client.containers.run("bfirsh/reticulate-splines", detach=True)
# print(container.id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spaceship CI')
    parser.add_argument('-o', '--organization', dest='organization',
                        help='Name of the organization hosting the challenges')
    parser.add_argument('-c', '--challenge', dest='challenge', help='Name of the challenge')

    args = parser.parse_args()

    organization = args.organization
    challenge_name = args.challenge
    base_path = '/tmp/spaceship-ci'

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    github = Github(os.environ['GITHUB_TOKEN'])
    challenge_repository = ChallengeRepositoryGithub(github)
    challenge = challenge_repository.find_by_name_and_org(challenge_name, organization)
    challenge.run_pipeline(base_path)
