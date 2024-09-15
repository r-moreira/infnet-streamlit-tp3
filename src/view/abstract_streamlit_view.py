from abc import ABC, abstractmethod

class AbstractStreamlitView(ABC):
    
    @abstractmethod
    def render(self):
        pass