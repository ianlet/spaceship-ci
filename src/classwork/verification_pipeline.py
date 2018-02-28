from classwork.verification_stage import VerificationStageEvent, VerificationStageStatus, VerificationStageFailed


class VerificationPipeline:

    def __init__(self, event_store, stages):
        self.event_store = event_store
        self.stages = stages

    def verify(self, classwork):
        try:
            self.__execute_verification_stages(classwork)
        except VerificationStageFailed as err:
            self.__store_event(classwork, err.stage, VerificationStageStatus.FAILED)

    def __execute_verification_stages(self, classwork):
        for stage in self.stages:
            self.__store_event(classwork, stage, VerificationStageStatus.STARTED)
            stage.execute(classwork)
            self.__store_event(classwork, stage, VerificationStageStatus.SUCCEEDED)

    def __store_event(self, classwork, stage, status):
        stage_started_event = VerificationStageEvent(stage.name, classwork.name, status)
        self.event_store.store(stage_started_event)
