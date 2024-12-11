from typing import Dict, Any, Optional, List
import frappe
from frappe import _

class RecordProcessor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.processing_stack = set()
        
    def process_record(self, record, fields):
        results = record.as_dict(fields)
        
        for entity in results:
            if entity in self.handlers:
                self._process_entity(entity, results[entity], results)
    
    
    def _process_entity(self, entity_type: str, data: Dict[str, Any], results: Dict, **kwargs) -> Optional[Any]:
        # Add check for circular dependencies
        if entity_type in self.processing_stack:
            frappe.logger().warning(f"Circular dependency detected for {entity_type}")
            return None
        
        self.processing_stack.add(entity_type)
        
        try:
            processed_data = self._preprocess_data(data)            
            handler_info = self.handlers[entity_type]
            
            # Process dependencies
            dependencies = {}
            if handler_info['depends_on']:
                for dependency in handler_info['depends_on']:
                    if dependency in results:
                        dep_handler = self.handlers.get(dependency)
                        if dep_handler:
                            dep_result = self._process_entity(dependency, results[dependency], results)
                            dependencies[dependency] = dep_result.name if dep_result else None
            
            # Process current entity
            try:
                existing_record = handler_info['handler'].find_existing(processed_data)
                
                if existing_record:
                    result = handler_info['handler'].update(existing_record, processed_data, **dependencies)
                else:
                    result = handler_info['handler'].process(processed_data, **dependencies)
                    
                results[entity_type] = result
                return result
                
            except Exception as e:
                frappe.logger().error(f"Error processing {entity_type}: {str(e)}")
                return None
                
        finally:
            # Always remove from processing stack, even if there's an error
            self.processing_stack.remove(entity_type)

    def _resolve_dependencies(self, depends_on: List[str], results: Dict[str, Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolves dependencies for a handler based on previous results and additional kwargs.
        
        Args:
            depends_on: List of dependency names
            results: Dictionary containing previously processed results
            kwargs: Additional keyword arguments
            
        Returns:
            Dictionary containing resolved dependencies
        """
        dependencies = {}
        
        if not depends_on:
            return dependencies
            
        for dependency in depends_on:
            if dependency in results:
                dependencies[dependency] = results[dependency]
            elif dependency in kwargs:
                dependencies[dependency] = kwargs[dependency]
                
        return dependencies

    def _preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocesses the input data by removing None values and empty strings.
        
        Args:
            data: Dictionary containing the data to process
            
        Returns:
            Dictionary with cleaned data
        """
        return {
            k: v for k, v in data.items() 
            if v is not None and v != ''
        }