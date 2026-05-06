from typing import Any
import frappe
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.base import DocTypeHandler

class ContactHandler(DocTypeHandler):
    def __init__(self):
        self.doctype = 'Contact'


    def process_data(self, doc_data, **kwargs):
        try:
            existing_doc = self.find_existing(doc_data)
            if existing_doc:
                return self.update(existing_doc, doc_data)
            
            # Map CIUDADANO to valid option
            if 'custom_document' in doc_data:
                custom_doc = str(doc_data['custom_document']).strip().upper()
                frappe.logger().info(f"DEBUG: custom_document before mapping: {custom_doc}")
                if custom_doc == 'CIUDADANO':
                    doc_data['custom_document'] = 'Citizen'
                    frappe.logger().info("DEBUG: Mapped CIUDADANO to Citizen")
                elif custom_doc == 'RESIDENTE':
                    doc_data['custom_document'] = 'Resident (I-551)'
                    frappe.logger().info("DEBUG: Mapped RESIDENTE to Resident (I-551)")
                else:
                    frappe.logger().info(f"DEBUG: No mapping found for {custom_doc}")
                
                frappe.logger().info(f"DEBUG: custom_document after mapping: {doc_data['custom_document']}")
            
            # Log the data being processed
            frappe.logger().info(f"Creating Contact with data: {doc_data}")
            
            # Create new document

            doc = frappe.get_doc(doc_data)
            return doc  
        except Exception as e:
            frappe.logger().error(f"Error in ContactHandler.process_data: {str(e)}")
            frappe.logger().error(f"Data that caused error: {doc_data}")
            raise  

    def find_existing(self, data):
        """
        Find existing document based on key fields.
        Returns the document if found, None otherwise.
        """
        if data.get("first_name") and data.get("last_name") and data.get("custom_day_of_birth"):
            existing_name = frappe.db.get_value(
                self.doctype,
                {
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "custom_day_of_birth": data["custom_day_of_birth"],
                },
                "name",
            )
            if existing_name:
                return frappe.get_doc(self.doctype, existing_name)

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
    
    def attach_links(self, entity: Any, processed_results: Any, handlers):
        """Adjunta un link a la tabla hija del documento"""
        try:
            for doctype in handlers.get(entity)['links']:
                if link_name := processed_results[doctype]:
                    for contact in processed_results[entity]:
                        contact = frappe.get_doc(self.doctype, contact.name)
                        if any(
                            link.link_doctype == doctype and link.link_name == link_name.name
                            for link in contact.links
                        ):
                            continue

                        contact.append('links', {
                            'link_doctype': doctype,
                            'link_name': link_name.name
                        })
                        contact.save()
        except Exception as e:
            frappe.logger().error(f"Error adjuntando links para {entity}: {str(e)}")
            raise
