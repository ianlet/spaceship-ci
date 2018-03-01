class EventStoreDummy:
    def store(self, event):
        print(f'Received event {event}')
