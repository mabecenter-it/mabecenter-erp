import frappe
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.handler.base import DocumentHandler
from mabecenter.overrides.exception.base_document_exist import BaseDocumentExist

class BaseDocumentHandler(DocumentHandler):
    def __init__(self, doctype):
        self.doctype = doctype

    def find_existing(self, data):
        """
        Find existing document based on key fields.
        Returns the document if found, None otherwise.
        """
        filters = {}
        
        # Get metadata for the doctype
        meta = frappe.get_meta(self.doctype)
        
        # Check for unique fields in the doctype
        for df in meta.fields:
            if df.unique and df.fieldname in data:
                filters[df.fieldname] = data[df.fieldname]
        
        # If no unique fields found, try common identifying fields
        if not filters:
            common_identifiers = ['name', 'code', 'id', 'email', 'phone']
            for field in common_identifiers:
                if field in data:
                    filters[field] = data[field]
                    break
        
        # Return None if no filters could be determined
        if not filters:
            return None
        
        try:
            # Attempt to find existing document
            existing_name = frappe.db.get_value(self.doctype, filters, 'name')
            if existing_name:
                return frappe.get_doc(self.doctype, existing_name)
        except Exception as e:
            frappe.logger().error(f"Error finding existing {self.doctype}: {str(e)}")
            
        return None

    def update(self, existing_doc, new_data, **dependencies):
        # Update existing document with new data
        for key, value in new_data.items():
            if hasattr(existing_doc, key):
                setattr(existing_doc, key, value)
        
        # Save updated document
        existing_doc.save()
        return existing_doc

    def process(self, data, **kwargs):
        try:
            # Set flag to indicate script execution
            frappe.flags.from_script = True
            
            # Process data and dependencies
            processed_data = self._process_json_data(data)
            child_tables, main_data = self._split_data(processed_data)
            processed_dependencies = self._process_dependencies(kwargs)
            
            # Prepare document data
            doc_data = {
                'doctype': self.doctype,
                **main_data,
                **processed_dependencies
            }
            
            # Check for existing document
            existing_doc = self.find_existing(doc_data)
            if existing_doc:
                return self.update(existing_doc, doc_data)
            
            # Create new document
            doc = frappe.get_doc(doc_data)
            
            # Add child tables if they exist
            for table_name, table_data in child_tables.items():
                if hasattr(doc, table_name):
                    for row in table_data:
                        doc.append(table_name, row)
            
            # Validate if method exists
            if hasattr(doc, 'validate'):
                doc.validate()
                
            # Insert new document
            doc.insert()
            return doc
            
        except BaseDocumentExist as e:
            # Handle existing document case
            return frappe.get_doc(self.doctype, e.doctype_name)
        finally:
            # Reset script flag
            frappe.flags.from_script = False

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

    def _process_json_data(self, data):
        """Process JSON strings in data"""
        processed_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    import json
                    processed_value = json.loads(value)
                    if isinstance(processed_value, dict):
                        processed_data[key] = processed_value
                    else:
                        processed_data[key] = value
                except json.JSONDecodeError:
                    processed_data[key] = value
            else:
                processed_data[key] = value
        return processed_data