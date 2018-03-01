from .verification_stage import VerificationStage, VerificationStageFailed


class TrackProgressStage(VerificationStage):
    def __init__(self, base_path, executor, mongo_host):
        super().__init__('track-progress')
        self.base_path = base_path
        self.executor = executor
        self.mongo_host = mongo_host

    def execute(self, submission):
        try:
            container = self.__create_container(submission)
            container.run()
        except:
            raise VerificationStageFailed(self)

    def __create_container(self, submission):
        container_name = f'{submission.slug}--{self.name}'
        container_command = ['./gradlew', 'accept', f'-DteamToken={submission.name}', f'-DmongoHost={self.mongo_host}']
        submission_path = f'{self.base_path}/{submission.path}'
        container = self.executor.create_container(submission.slug, container_name, container_command, submission_path)
        return container
