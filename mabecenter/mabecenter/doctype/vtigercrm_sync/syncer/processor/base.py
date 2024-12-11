from abc import ABC, abstractmethod
from typing import Dict, Any, List

# Base class for all entity processors
class EntityProcessor(ABC):
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Abstract method to process entity data
        pass

    def get_links(self, dependencies: Dict[str, Any]) -> List[Dict[str, str]]:
        """Return list of link objects for the document"""
        return []

    def get_child_tables(self, dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """Return dictionary of child table data"""
        return {}