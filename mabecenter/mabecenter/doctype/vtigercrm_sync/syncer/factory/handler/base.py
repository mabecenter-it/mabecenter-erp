# Import abstract base class functionality
from abc import ABC, abstractmethod

# Base class for document handlers
class DocumentHandler(ABC):
    @abstractmethod
    def process(self, data, **kwargs):
        # Abstract method to process document data
        pass
