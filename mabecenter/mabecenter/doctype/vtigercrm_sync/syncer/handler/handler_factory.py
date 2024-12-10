import frappe
from mabecenter.overrides.exception.base_document_exist import BaseDocumentExist
from abc import ABC, abstractmethod

class DocumentHandler(ABC):
    @abstractmethod
    def process(self, data, **kwargs):
        pass

class BaseDocumentHandler(DocumentHandler):
    def __init__(self, doctype):
        self.doctype = doctype

    def process(self, data, **kwargs):
        try:
            frappe.flags.from_script = True
            
            # Separate child tables from main data
            child_tables = {}
            main_data = {}
            
            for key, value in data.items():
                if isinstance(value, list):
                    child_tables[key] = value
                else:
                    main_data[key] = value

            # Prepare main document data
            doc_data = {
                'doctype': self.doctype,
                **main_data,
                **kwargs
            }
            
            doc = frappe.get_doc(doc_data)
            
            # Add child table entries
            for table_field, entries in child_tables.items():
                for entry in entries:
                    child_doctype = frappe.get_meta(self.doctype).get_field(table_field).options
                    if isinstance(entry, dict):
                        entry['doctype'] = child_doctype
                        doc.append(table_field, entry)
                    else:
                        # Handle string/primitive values
                        doc.append(table_field, {
                            'doctype': child_doctype,
                            'name': str(entry)
                        })
            
            if hasattr(doc, 'validate'):
                doc.validate()
                
            doc.insert()
            return doc
        except BaseDocumentExist as e:
            existing_name = e.doctype_name
            return frappe.get_doc(self.doctype, existing_name)
        finally:
            frappe.flags.from_script = False

class HandlerFactory:
    @staticmethod
    def create_handler(doc_type: str) -> DocumentHandler:
        handlers = {
            'Bank Card': BaseDocumentHandler,
            'Customer': BaseDocumentHandler,
            'Contact': BaseDocumentHandler,
            'Address': BaseDocumentHandler,
            'Sales Order': BaseDocumentHandler,
            'Bank Account': BaseDocumentHandler,
        }
        handler_class = handlers.get(doc_type)
        if not handler_class:
            raise ValueError(f"No handler found for {doc_type}")
        return handler_class(doc_type)