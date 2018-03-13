from datetime import datetime
from enum import Enum

from src.utils import ValueObject


class VerificationStage:
    def __init__(self, name):
        self.name = name


class VerificationStageStatus(Enum):
    STARTED = 'started'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'


class VerificationStageEvent(ValueObject):
    __slots__ = 'stage', 'submission', 'status', 'timestamp'

    def __init__(self, *vals):
        super().__init__(*vals, datetime.now())


class VerificationStageFailed(Exception):
    def __init__(self, stage):
        self.stage = stage
