from abc import ABC, abstractmethod

class MouseListener(ABC):
    @abstractmethod
    def on_mouse_over(self, mouse_position) -> bool:
        pass

    @abstractmethod
    def on_mouse_left_click(self, mouse_position) -> bool:
        pass

