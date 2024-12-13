from abc import ABC, abstractmethod

class EntityProcessor(ABC):
    @abstractmethod
    def process(self, data: dict) -> dict:
        pass

    def get_links(self, dependencies: dict) -> list:
        return []