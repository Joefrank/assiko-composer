from abc import abstractmethod

class Event:   

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)
    
    def get_all_listeners(self):
        return self.listeners
    
    def clear_listeners(self):
        self.listeners = []

    @abstractmethod 
    def notify(self) -> bool:
        pass