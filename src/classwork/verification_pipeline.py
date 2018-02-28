class VerificationPipeline:

    def __init__(self, stages):
        self.stages = stages

    def verify(self, classwork):
        try:
            self.__execute_verification_stages(classwork)
        except:
            pass

    def __execute_verification_stages(self, classwork):
        for stage in self.stages:
            stage.execute(classwork)
