from .build_stage import BuildStage
from .preparation_stage import PreparationStage
from .test_stage import TestStage
from .track_progress_stage import TrackProgressStage
from .verification_stage import VerificationStageEvent, VerificationStageStatus, VerificationStageFailed


class VerificationPipeline:
    def __init__(self, event_store, stages):
        self.event_store = event_store
        self.stages = stages

    def verify(self, submission):
        print("Starting verification pipeline for", submission)
        try:
            self.__execute_verification_stages(submission)
            print("Verification pipeline succeeded for", submission)
        except VerificationStageFailed as err:
            self.__store_event(submission, err.stage, VerificationStageStatus.FAILED)
            print("Verification pipeline failed for", submission)

    def __execute_verification_stages(self, submission):
        for stage in self.stages:
            self.__store_event(submission, stage, VerificationStageStatus.STARTED)
            stage.execute(submission)
            self.__store_event(submission, stage, VerificationStageStatus.SUCCEEDED)

    def __store_event(self, submission, stage, status):
        stage_started_event = VerificationStageEvent(stage.name, submission.name, status)
        self.event_store.store(stage_started_event)


class VerificationPipelineFactory:
    def __init__(self, event_store, repository, base_path, executor, mongo_host):
        self.event_store = event_store
        self.base_path = base_path
        self.repository = repository
        self.executor = executor
        self.mongo_host = mongo_host

    def create(self):
        stages = [
            PreparationStage(self.repository),
            BuildStage(self.base_path, self.executor),
            TestStage(self.base_path, self.executor),
            TrackProgressStage(self.base_path, self.executor, self.mongo_host)
        ]
        return VerificationPipeline(self.event_store, stages)
