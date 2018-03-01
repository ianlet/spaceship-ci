from .verification_stage import VerificationStage, VerificationStageFailed


class TestStage(VerificationStage):
    def __init__(self, base_path, executor):
        super().__init__('test')
        self.base_path = base_path
        self.executor = executor

    def execute(self, submission):
        container_name = f'{submission.slug}--{self.name}'
        container_command = ['./gradlew', 'test']
        submission_path = f'{self.base_path}/{submission.path}'

        try:
            container = self.executor.create_container(submission.slug, container_name, container_command,
                                                       submission_path)
            container.run()
        except:
            raise VerificationStageFailed(self)
