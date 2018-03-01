class Submission:
    def __init__(self, challenge):
        self.name = f'{challenge.org}--{challenge.name}'
        self.challenge = challenge
