from datetime import date
import time
import frappe
import json

from sqlalchemy.orm import sessionmaker, joinedload

#from mabecenter.mabecenter.doctype.vtigercrm_sync.models.vtigercrm_contact import VTigerContact
from mabecenter.overrides.exception.contact_exist_exception import ContactExist
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import engine
from mabecenter.mabecenter.doctype.vtigercrm_sync.models.vtigercrm_salesordercf import VTigerSalesOrderCF

class Syncer:
    def __init__(self, doc_name):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.doc_name = doc_name
        self.vtigercrm_sync = frappe.get_doc("VTigerCRM Sync", doc_name)

    def sync(self):
        filename = frappe.get_app_path('mabecenter', 'mabecenter', 'doctype', 'vtigercrm_sync', 'config', 'mapping', 'contact.json')
        fields = None
        with open(filename, 'r', encoding='utf-8') as file:
            fields = json.load(file)

            status_values = ['Active', 'Initial Enrollment', 'Sin Digitar']
            effective = date(2025, 1, 1)
            selldate = date(2024, 10, 28)
        
            results = (self.session.query(VTigerSalesOrderCF)
                .filter(
                    VTigerSalesOrderCF.cf_2141.in_(status_values),
                    VTigerSalesOrderCF.cf_2059 == effective,
                    VTigerSalesOrderCF.cf_2179 >= selldate
                ).order_by(VTigerSalesOrderCF.salesorderid.desc())
                .all()
            )

            self.session.close()

            if results:
                total_records = len(results)
                print(f"Total Records Found: {len(results)}\n")

                for idx, record in enumerate(results, start=1):
                    self.update_progress(idx/total_records)
                    contacts = record.as_dict(fields)
                    for contact in contacts:
                        self.do_sync_work(contact)
                        
        """ 
        result = self.session.execute(text("SELECT VERSION();"))
        version = result.fetchone()[0]
        frappe.msgprint(
            msg=f"Conexión exitosa a VtigerCRM. Versión del motor: {version}",
            title='Error',
            raise_exception=FileNotFoundError
        ) """
                
        return True

    def update_progress(self, percentage):
        #frappe.publish_progress(percentage, title='Some title', description='Some description')
        frappe.publish_realtime(
            'vtigercrm_sync_refresh',
            {
                'percentage': f"{percentage * 100:.2f}",
                'vtigercrm_sync': self.doc_name
            }
        )

    def do_sync_work(self, contact):
        try:
            frappe.flags.from_script = True
            doc = frappe.get_doc({
                'doctype': 'Contact',
                **contact
            })
            doc.validate()
            doc.insert()
        except ContactExist as e:
            existing_contact_name = e.contact_name
            doc = frappe.get_doc('Contact', existing_contact_name) 
        finally:
            frappe.flags.from_script = False
