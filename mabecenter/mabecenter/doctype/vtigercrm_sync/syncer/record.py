from typing import Dict, Any, Optional, List
import frappe
from frappe import _

class RecordProcessor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.processing_stack = set()
        
    def process_record(self, record, fields):
        # Get mapped data from VTiger record
        mapped_data = record.as_dict(fields)
        processed_results = {}
        
        # Process each entity type in order of dependencies
        processing_order = self._determine_processing_order()
        
        for entity_type in processing_order:
            if entity_type not in self.handlers:
                continue
            
            entity_data = mapped_data.get(entity_type, {})
            
            # Special handling for contacts from owner/spouse/dependents
            if entity_type == 'contact':
                self._process_contact_entities(entity_data, mapped_data, processed_results)
            else:
                # Normal entity processing
                result = self._create_entity(entity_type, entity_data)
                if result:
                    processed_results[entity_type] = result
                    self._update_dependencies(entity_type, result, processed_results)
        
        return processed_results

    def _process_contact_entities(self, contact_data, mapped_data, processed_results):
        contact_info = mapped_data.get('Contact', {})
        
        # Process owner as primary contact
        if 'owner' in contact_info:
            owner_data = contact_info['owner']
            owner_data['is_primary_contact'] = 1
            contact = self._create_entity('contact', owner_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)
        
        # Process spouse contact
        if 'spouse' in contact_info:
            spouse_data = contact_info['spouse']
            spouse_data['is_primary_contact'] = 0
            contact = self._create_entity('contact', spouse_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)
                
        # Process dependent contact
        if 'dependent_1' in contact_info:
            dependent_data = contact_info['dependent_1']
            dependent_data['is_primary_contact'] = 0
            contact = self._create_entity('contact', dependent_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)
        
        # Process spouse if present
        if 'spouse' in mapped_data:
            spouse_data = mapped_data['spouse']
            spouse_data['is_primary_contact'] = 0
            contact = self._create_entity('contact', spouse_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)

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
            else:
                return handler_info['handler'].process(processed_data)
        except Exception as e:
            frappe.logger().error(f"Error in _create_entity for {entity_type}: {str(e)}")
            raise

    def _update_dependencies(self, entity_type: str, doc: Any, results: Dict[str, Any]):
        """Update document with its dependencies"""
        handler_info = self.handlers[entity_type]
        
        if not handler_info['depends_on']:
            return
        
        dependencies = {}
        for dependency in handler_info['depends_on']:
            if dependency in results and results[dependency]:
                dependencies[dependency] = results[dependency].name
        
        if dependencies:
            try:
                handler_info['handler'].update(doc, {}, **dependencies)
            except Exception as e:
                frappe.logger().error(f"Error updating dependencies for {entity_type}: {str(e)}")
                raise

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