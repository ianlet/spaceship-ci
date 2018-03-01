from challenge import TestStage
from src.event_store.event_store_dummy import EventStoreDummy
from .build_stage import BuildStage
from .preparation_stage import PreparationStage
from .verification_stage import VerificationStageEvent, VerificationStageStatus, VerificationStageFailed


class VerificationPipeline:
    def __init__(self, event_store, stages):
        self.event_store = event_store
        self.stages = stages

    def verify(self, submission):
        try:
            self.__execute_verification_stages(submission)
        except VerificationStageFailed as err:
            self.__store_event(submission, err.stage, VerificationStageStatus.FAILED)

    def __execute_verification_stages(self, submission):
        for stage in self.stages:
            self.__store_event(submission, stage, VerificationStageStatus.STARTED)
            stage.execute(submission)
            self.__store_event(submission, stage, VerificationStageStatus.SUCCEEDED)

    def __store_event(self, submission, stage, status):
        stage_started_event = VerificationStageEvent(stage.name, submission.name, status)
        self.event_store.store(stage_started_event)


class VerificationPipelineFactory:
    def __init__(self, repository, base_path, executor):
        self.base_path = base_path
        self.repository = repository
        self.executor = executor

    def create(self):
        stages = [
            PreparationStage(self.repository),
            BuildStage(self.base_path, self.executor),
            TestStage(self.base_path, self.executor)
        ]
        return VerificationPipeline(EventStoreDummy(), stages)
