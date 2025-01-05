# Import abstract base class functionality
from abc import ABC, abstractmethod
from typing import Any, Dict
import frappe
from mabecenter.overrides.exception.base_document_exist import BaseDocumentExist

# Base class for document handlers
class DocTypeHandler(ABC):
    @abstractmethod
    def attach_links(self, entity: Any, processed_results: Any, handlers):
        # Abstract method to process document data
        pass
    
    @abstractmethod
    def process_data(self, data, **kwargs):
        # Abstract method to process document data
        pass

    def process(self, data, processed_dependencies = None, **kwargs):
        try:
            # Set flag to indicate script execution
            frappe.flags.from_script = True
            
            # Process data and dependencies
            processed_data = data
            child_tables, main_data = self._split_data(processed_data)

            doc_data = {
                'doctype': self.doctype,
                **main_data,
            }

            # implement depend_on
            if processed_dependencies:
                doc_data['customer'] = processed_dependencies['Customer'].name
                        
            doc = self.process_data(doc_data)
            
            # Validate if method exists
            if hasattr(doc, 'validate'):
                doc.validate()
                

            if not doc.creation:
                doc.insert()
            
            
            return doc
            
        except BaseDocumentExist as e:
            # Handle existing document case
            return frappe.get_doc(self.doctype, e.doctype_name)
        finally:
            # Reset script flag
            frappe.flags.from_script = False 

    @abstractmethod
    def find_existing(self, data):
        pass

    def _process_dependencies(self, dependencies):
        """Process dependencies and return their names"""
        processed = {}
        for dep_name, dep_doc in dependencies.items():
            if dep_doc:
                if isinstance(dep_doc, str):
                    processed[dep_name] = dep_doc
                else:
                    processed[dep_name] = dep_doc.name
        return processed

    def update(self, existing_doc, new_data, **dependencies):
        # Update existing document with new data
        for key, value in new_data.items():
            if hasattr(existing_doc, key):
                setattr(existing_doc, key, value)
        
        # Save updated document
        existing_doc.save()
        return existing_doc

    def _split_data(self, data):
        """Separate data into child tables and main data"""
        child_tables = {}
        main_data = {}
        
        for key, value in data.items():
            if isinstance(value, list):
                child_tables[key] = value
            else:
                main_data[key] = value
                
        return child_tables, main_data