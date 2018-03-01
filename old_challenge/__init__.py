import os


class Challenge:
    def __init__(self, name, organization, assignments):
        self.name = name
        self.organization = organization
        self.assignments = assignments

    def run_pipeline(self, base_path):
        print(f'Starting pipeline for challenge {self.organization}/{self.name}...')

        challenge_path = f'{base_path}/{self.organization}-{self.name}'
        self.__ensure_exists(challenge_path)

        for assignment in self.assignments:
            assignment.clone_or_update(challenge_path)
            try:
                assignment.build(challenge_path)
                print(f'Assignment {assignment.name} successfully built!')
            except:
                print(f'Assignment {assignment.name} build failed!')
                # TODO: Persist error for assignment
                continue

            try:
                assignment.test(challenge_path)
            except:
                print(f'Assignment {assignment.name} test failed!')
                # TODO: Persist error for assignment
                continue

            assignment.evaluate_progress(challenge_path)
            break

    def __ensure_exists(self, challenge_path):
        if not os.path.exists(challenge_path):
            os.makedirs(challenge_path)
