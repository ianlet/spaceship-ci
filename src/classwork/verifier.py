class ClassworkVerifier:

    def __init__(self, classwork_repository, verification_pipeline):
        self.classwork_repository = classwork_repository
        self.verification_pipeline = verification_pipeline

    def verify_for_assignment(self, assignment):
        classworks = self.classwork_repository.find_by_assignment(assignment)
        for classwork in classworks:
            self.verification_pipeline.verify(classwork)
