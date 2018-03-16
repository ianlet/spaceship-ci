from .verification_stage import VerificationStage, VerificationStageFailed


class BuildStage(VerificationStage):
    def __init__(self, base_path, executor):
        super().__init__('build')
        self.base_path = base_path
        self.executor = executor

    def execute(self, submission):
        print(f'[BUILD STAGE] - {submission} - STARTED')
        container_name = f'{submission.slug}--{self.name}'
        container_command = ['./gradlew', 'build', '--refresh-dependencies', '-x', 'test']
        submission_path = f'{self.base_path}/{submission.path}'

        try:
            container = self.executor.create_container(submission.slug, container_name, container_command,
                                                       submission_path)
            container.run()
            print(f'[BUILD STAGE] - {submission} - DONE')
        except Exception as err:
            print(f'[BUILD STAGE] - {submission} - FAILED')
            raise VerificationStageFailed(self)
