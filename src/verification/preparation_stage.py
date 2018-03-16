from .verification_stage import VerificationStage


class PreparationStage(VerificationStage):
    def __init__(self, repository):
        super().__init__('preparation')
        self.repository = repository

    def execute(self, submission):
        print(f'[PREPARATION STAGE] - {submission} - STARTED')
        self.repository.clone(submission)
        print(f'[PREPARATION STAGE] - {submission} - DONE')
