class EventStoreMongo:
    COLLECTION = 'events'

    def __init__(self, database):
        self.database = database
        self.collection = database[self.COLLECTION]

    def store(self, event):
        event = {
            'stage': event.stage,
            'submission': event.submission,
            'status': event.status.value,
            'timestamp': event.timestamp
        }
        self.collection.insert_one(event)
