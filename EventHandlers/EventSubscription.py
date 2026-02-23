
class EventSubscription:
    def __init__(self, event_type, handler_name):
        self.event_type = event_type
        self.handler_name = handler_name
        self.subscribers = []

    def subscribe(self, subscriber):
        # check if object is not already subscribed
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
           # print(f"Subscriber {subscriber.name} subscribed to event {self.event_type} with handler {self.handler_name}")