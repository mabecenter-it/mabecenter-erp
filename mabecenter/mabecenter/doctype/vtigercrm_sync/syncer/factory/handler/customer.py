from typing import Any
import frappe
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.base import DocTypeHandler

class CustomerHandler(DocTypeHandler):
    def __init__(self):
        self.doctype = 'Customer'

    def process_data(self, doc_data, **kwargs):

        doc_data['customer_name'] = f"{doc_data['first_name']} {doc_data['last_name']}"
        
        existing_doc = self.find_existing(doc_data)
        if existing_doc:
            return self.update(existing_doc, doc_data)
        else:
            doc = frappe.get_doc(doc_data)
            return doc
    
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

    def attach_links(self, entity: Any, link: str, linked_entity: Any, handlers):
        """Adjunta un link a la tabla hija del documento"""
        try:
            for doctype in handlers.get(entity)['links']:
                if doctype == 'Contact':
                    link.set('customer_primary_contact', linked_entity.name)
                    link.save()
                elif doctype == 'Address':
                    link.set('customer_primary_address', linked_entity.name)
                    link.save()
                elif doctype == 'Bank Account':
                    link.set('default_bank_account', linked_entity.name)
                    link.save()
                elif doctype == 'Bank Card':
                    link.set('default_bank_card', linked_entity.name)
                    link.save()
        except Exception as e:
            frappe.logger().error(f"Error adjuntando link {link} a {entity.doctype}: {str(e)}")
            raise
    