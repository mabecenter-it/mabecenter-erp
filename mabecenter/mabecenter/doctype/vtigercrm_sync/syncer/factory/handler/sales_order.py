from typing import Any
import frappe
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.base import DocTypeHandler

class SalesOrderHandler(DocTypeHandler):
    def __init__(self):
        self.doctype = 'Sales Order'

    def process_data(self, doc_data, **kwargs):
        # Prepare document data
        
        existing_doc = self.find_existing(doc_data)
        if existing_doc:
            return self.update(existing_doc, doc_data)
        
        doc_data['delivery_date'] = '2025-01-15'
        doc_data['company'] = 'Mabe Center'

        doc = frappe.get_doc(doc_data)

        doc.append('items', {
            'item_code': 'BS',
            'qty': '1',
            'rate': '100',
        })

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
            if df.fieldname in data:
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
            else:
                return None
        except Exception as e:
            frappe.logger().error(f"Error finding existing {self.doctype}: {str(e)}")
    
    def attach_links(self, entity: Any, processed_results: Any, handlers):
        """Adjunta un link a la tabla hija del documento"""
        try:
            """ for doctype in handlers.get(entity)['links']:
                if link_name := processed_results[doctype]:
                    processed_results[entity].append('links', {
                        'link_doctype': doctype,
                        'link_name': link_name.name
                    })
                    link_name.save() """
            pass
        except Exception as e:
            frappe.logger().error(f"Error adjuntando link {processed_results[entity].doctype} a {entity.doctype}: {str(e)}")
            raise