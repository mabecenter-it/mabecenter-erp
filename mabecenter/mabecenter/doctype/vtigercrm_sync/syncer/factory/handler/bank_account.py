from typing import Any
import frappe
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.base import DocTypeHandler

class BankAccountHandler(DocTypeHandler):
    def __init__(self):
        self.doctype = 'Bank Account'

    def process_data(self, doc_data, **kwargs):
        # Prepare document data
        bank_name = doc_data.get('Bank')
        existing_bank = frappe.db.exists('Bank', {'bank_name': bank_name})

        if existing_bank:
            doc_data['bank'] = existing_bank
        else:
            doc_bank = frappe.get_doc({
                'doctype': 'Bank',
                'bank_name': bank_name
            })
            doc_bank.insert()
            doc_data['bank'] = doc_bank.name

        existing_doc = self.find_existing(doc_data)
        if existing_doc:
            return self.update(existing_doc, doc_data)
        else:
            doc = frappe.get_doc(doc_data)
            return doc
    
    def find_existing(self, doc_data):
        """
        Find existing document based on key fields.
        Returns the document if found, None otherwise.
        """
        bank_name = doc_data.get('Bank')
        account_name = doc_data.get('account_name')
        try:
            existing_bank_account = frappe.get_doc(
                'Bank Account', 
                {
                    'account_name': account_name,
                    'bank': bank_name,
                }
            )
            return existing_bank_account
        except:
            return None
        
    def attach_links(self, entity: Any, processed_results: Any, handlers):
        """Adjunta un link a la tabla hija del documento"""
        try:
            for doctype in handlers.get(entity)['links']:
                if link_name := processed_results[doctype]:
                    processed_results[entity].set('party_type', doctype)
                    processed_results[entity].set('party', link_name.name)
                    processed_results[entity].save()
        except Exception as e:
            frappe.logger().error(f"Error adjuntando link {processed_results[entity].doctype} a {entity.doctype}: {str(e)}")
            raise
    