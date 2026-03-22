
import pygame

from DataClasses.EventData import EVENT_TYPES
from EventHandlers.EventSubscription import EventSubscription
from Helpers.ScreeHelper import ScreenHelper
from Model.Containers.Window import Window


class MainWindowEventHandler:

    def __init__(self):
        self.event_subscriptions = []
        self.init_event_subscriptions()

    def init_event_subscriptions(self):
        for supported_event, _, handler_name in EVENT_TYPES:
            self.event_subscriptions.append(EventSubscription(supported_event, handler_name))           

    def subscribe(self, event_type, subscriber):
        # Find the subscription for the event type and add the subscriber to it
        subscription = next((s for s in self.event_subscriptions if s.event_type == event_type), None)
        #check that subscription exists for the event type and also that subscriber is not already subscribed to avoid duplicates 
        if subscription and subscriber not in subscription.subscribers:     
            subscription.subscribe(subscriber) 
        # check that event doesn't already exist in supported_events then add it.
        if event_type not in subscriber.supported_events:
            subscriber.supported_events.append(event_type)     

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            #try:
                # find corresponding subscription for event.type
                subscription = next((s for s in self.event_subscriptions if s.event_type == event.type), None)
                if subscription:
                    # notify all subscribers of the event in order of their z-index (higher z-index first)
                    ordered_subscribers = sorted(subscription.subscribers, key=lambda s: s.z_index, reverse=True)
                    for subscriber in ordered_subscribers: 
                        # if subscriber is not visible and it's a mouse event, skip it and move to the next one
                        if not subscriber.visible and not ScreenHelper.is_keyboard_event(event):
                            continue    
                                          
                        handler = getattr(subscriber, subscription.handler_name, None)
                        if handler:
                            is_event_handled = handler(event)
                            if is_event_handled:
                                break               
                
            #except Exception as e:
               # print(f"Error handling event {event.type}: {e}")
                #self.logger.error(f"Error handling event {event.type}: {e}")
                #self.state.add_error(f"Event handling error: {e}")
       
        