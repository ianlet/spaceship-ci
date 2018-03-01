class ChallengeVerifier:
    def __init__(self, submission_repository, verification_pipeline):
        self.submission_repository = submission_repository
        self.verification_pipeline = verification_pipeline

    def verify_submissions(self, challenge):
        submissions = self.submission_repository.find_by_challenge(challenge)
        for submission in submissions:
            self.verification_pipeline.verify(submission)
