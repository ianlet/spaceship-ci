class Submission:
    def __init__(self, name, url, challenge):
        self.name = name
        self.url = url
        self.challenge = challenge

    @property
    def path(self):
        return f'{self.challenge.org}/{self.challenge.name}/{self.name}'

    @property
    def slug(self):
        return f'{self.challenge.org}--{self.challenge.name}-{self.name}'

    def __str__(self) -> str:
        return self.slug


