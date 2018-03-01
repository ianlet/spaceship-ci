class ChallengeVerifier:
    def __init__(self, submission_repository, verification_pipeline_factory):
        self.submission_repository = submission_repository
        self.verification_pipeline_factory = verification_pipeline_factory

    def verify_submissions(self, challenge):
        verification_pipeline = self.verification_pipeline_factory.create()
        submissions = self.submission_repository.find_by_challenge(challenge)
        for submission in submissions:
            verification_pipeline.verify(submission)
