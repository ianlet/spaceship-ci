import argparse
import os

import docker
from github import Github

from src.challenge import ChallengeVerifier, SubmissionRepositoryGithub, VerificationPipelineFactory, Challenge
from src.executor import DockerExecutor
from src.repository import GitRepository

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spaceship CI')
    parser.add_argument('-o', '--organization', dest='organization',
                        help='Name of the organization hosting the challenges')
    parser.add_argument('-c', '--challenge', dest='challenge', help='Name of the challenge')

    args = parser.parse_args()

    organization = args.organization
    challenge_name = args.challenge
    challenge = Challenge(organization, challenge_name)
    base_path = '/tmp/spaceship-ci'

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    docker_client = docker.from_env()
    docker_executor = DockerExecutor(docker_client, 'gradle:4.5.1-jdk8', 1357, 5000)

    github = Github(os.environ['GITHUB_TOKEN'])
    submission_repository = SubmissionRepositoryGithub(github)

    git_repository = GitRepository(base_path)
    verification_pipeline_factory = VerificationPipelineFactory(git_repository, base_path, docker_executor)

    challenge_verifier = ChallengeVerifier(submission_repository, verification_pipeline_factory)
    challenge_verifier.verify_submissions(challenge)
