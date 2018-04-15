import argparse
import os
import shutil

import docker
from github import Github
from pymongo import MongoClient

from src.challenge.challenge import Challenge
from src.challenge.submission_repository_github import SubmissionRepositoryGithub
from src.event_store.event_store_mongo import EventStoreMongo
from src.executor import DockerExecutor
from src.repository import GitRepository
from src.verification.challenge_verifier import ChallengeVerifier
from src.verification.verification_pipeline import VerificationPipelineFactory


def create_event_store():
    mongo_client = MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']))
    mongo_database = mongo_client[os.environ['SPACESHIP_DATABASE']]
    return EventStoreMongo(mongo_database)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spaceship CI')
    parser.add_argument('-o', '--organization', dest='organization',
                        help='Name of the organization hosting the challenges')
    parser.add_argument('-c', '--challenge', dest='challenge', help='Name of the challenge')
    parser.add_argument('-d', '--directory', dest='directory', help='Where to temporarly store the submissions',
                        default='./submissions')

    args = parser.parse_args()

    base_path = args.directory
    organization = args.organization
    challenge_name = args.challenge
    challenge = Challenge(organization, challenge_name)

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    docker_client = docker.from_env()
    docker_executor = DockerExecutor(docker_client, 'gradle:4.5.1-jdk8')

    github = Github(os.environ['GITHUB_TOKEN'])
    submission_repository = SubmissionRepositoryGithub(github)

    event_store = create_event_store()
    git_repository = GitRepository(base_path)
    verification_pipeline_factory = VerificationPipelineFactory(event_store, git_repository, base_path, docker_executor,
                                                                'mongo')

    challenge_verifier = ChallengeVerifier(submission_repository, verification_pipeline_factory)
    challenge_verifier.verify_submissions(challenge)

    shutil.rmtree(base_path)
