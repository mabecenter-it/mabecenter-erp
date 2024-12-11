from abc import ABC, abstractmethod

class ProgressObserver(ABC):
    @abstractmethod
    def update(self, percentage: float, context: dict):
        pass
