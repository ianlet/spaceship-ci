from unittest import TestCase

from pymongo import MongoClient

from event_store.event_store_mongo import EventStoreMongo
from verification.verification_stage import VerificationStageEvent, VerificationStageStatus


class TestEventStoreMongo(TestCase):
    A_STAGE = 'build'
    A_SUBMISSION = 'team-01'
    A_STATUS = VerificationStageStatus.SUCCEEDED

    def setUp(self):
        self.mongo_client = MongoClient()
        self.database = self.mongo_client.spaceship_test

        self.event_store = EventStoreMongo(self.database)

    def tearDown(self):
        self.mongo_client.drop_database(self.database)
        self.mongo_client.close()

    def test_store_the_event(self):
        event = VerificationStageEvent(self.A_STAGE, self.A_SUBMISSION, self.A_STATUS)

        self.event_store.store(event)

        self.__assert_event_persisted(event)

    def __assert_event_persisted(self, event):
        event_document = {'stage': event.stage, 'status': event.status.value, 'submission': event.submission,
                          'timestamp': event.timestamp}
        persisted_event = self.database[EventStoreMongo.COLLECTION].find_one(event_document)
        assert persisted_event is not None
