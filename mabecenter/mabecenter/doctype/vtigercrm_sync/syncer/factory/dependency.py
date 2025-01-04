from typing import Dict, Any, List
import frappe

class DependencyResolver:
    def __init__(self, handlers):
        self.handlers = handlers
        self.processing_stack = set()

    def determine_processing_order(self) -> List[str]:
        """Determine order of entity processing based on dependencies"""
        order = []
        visited = set()
        
        def visit(entity_type):
            if entity_type in self.processing_stack:
                raise ValueError(f"Circular dependency detected for {entity_type}")
            
            if entity_type in visited:
                return
                
            self.processing_stack.add(entity_type)
            handler_info = self.handlers.get(entity_type, {})
            
            for dependency in handler_info.get('depends_on', []):
                visit(dependency)
                
            self.processing_stack.remove(entity_type)
            visited.add(entity_type)
            order.append(entity_type)
            
        for entity_type in self.handlers:
            visit(entity_type)
            
        return order