from enum import Enum

from utils import ValueObject


class VerificationStage:

    def __init__(self, name):
        self.name = name


class VerificationStageStatus(Enum):
    STARTED = 'started'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'


class VerificationStageEvent(ValueObject):
    __slots__ = 'stage', 'classwork', 'status'


class VerificationStageFailed(Exception):
    def __init__(self, stage):
        self.stage = stage
