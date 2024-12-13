from typing import Dict, Any
import frappe

class ContactProcessor:
    def __init__(self, handlers):
        self.handlers = handlers

    def process_contacts(self, contact_data: Dict[str, Any], mapped_data: Dict[str, Any], processed_results: Dict[str, Any]):
        """Process all contact types (owner, spouse, dependent)"""
        contact_info = mapped_data.get('Contact', {})
        
        self._process_contact_type('owner', contact_info, processed_results, is_primary=True)
        self._process_contact_type('spouse', contact_info, processed_results)
        self._process_contact_type('dependent_1', contact_info, processed_results)

    def _process_contact_type(self, contact_type: str, contact_info: Dict[str, Any], processed_results: Dict[str, Any], is_primary: bool = False):
        """Process a specific type of contact"""
        if contact_type not in contact_info:
            return
            
        contact_data = contact_info[contact_type]
        contact_data['is_primary_contact'] = 1 if is_primary else 0
        
        contact = self._create_contact(contact_data)
        if contact:
            processed_results.setdefault('contacts', []).append(contact)

    def _create_contact(self, data: Dict[str, Any]) -> Any:
        """Create a new contact document"""
        handler_info = self.handlers['contact']
        return handler_info['handler'].process(data) 