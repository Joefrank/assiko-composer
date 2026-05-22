

class Timer:

    def __init__(self, timer_name: str, interval: int):
        self.timer_name = timer_name
        self.interval = interval
        self.subscribers = []
        self.ticks = 0

    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def notify_subscribers(self, dt: int = 0):
        for subscriber in self.subscribers:
            handler = getattr(subscriber, "on_timer_tick", None)
            if handler:
                handler(dt)

    def tick(self, dt: int):
        self.ticks += dt
        if self.ticks >= self.interval:
            self.notify_subscribers()
            self.ticks = 0