from typing import Dict, Any, Optional, List
import frappe
from .dependency import DependencyResolver
from .contact import ContactProcessor

class RecordProcessor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.dependency_resolver = DependencyResolver(handlers)
        self.contact_processor = ContactProcessor(handlers)
        
    def process_record(self, record, fields):
        # Get mapped data from VTiger record
        mapped_data = record.as_dict(fields)
        processed_results = {}
        
        # Process each entity type in order of dependencies
        processing_order = self.dependency_resolver.determine_processing_order()
        
        for entity_type in processing_order:
            if entity_type not in self.handlers:
                continue
                
            entity_data = mapped_data.get(entity_type, {})
            
            # Special handling for contacts
            if entity_type == 'contact':
                self.contact_processor.process_contacts(entity_data, mapped_data, processed_results)
            else:
                # Normal entity processing
                result = self._create_entity(entity_type, entity_data)
                if result:
                    processed_results[entity_type] = result
                    self.dependency_resolver.update_dependencies(entity_type, result, processed_results)
        
        return processed_results

    def _create_entity(self, entity_type: str, data: Dict[str, Any]) -> Optional[Any]:
        """Create a new document without dependencies"""
        if not data:
            return None
        
        processed_data = self._preprocess_data(data)
        handler_info = self.handlers[entity_type]
        
        try:
            existing_record = handler_info['handler'].find_existing(processed_data)
            if existing_record:
                return existing_record
            return handler_info['handler'].process(processed_data)
        except Exception as e:
            frappe.logger().error(f"Error in _create_entity for {entity_type}: {str(e)}")
            raise

    def _preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocesses the input data by removing None values and empty strings"""
        return {
            k: v for k, v in data.items() 
            if v is not None and v != ''
        } 