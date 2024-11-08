# Copyright (c) 2024, Dante Devenir and contributors
# For license information, please see license.txt

# import frappe
import frappe
from rq.timeouts import JobTimeoutException
from frappe.model.document import Document
from frappe.core.doctype.vtigercrm_import.importer import Importer



class VTigerCRMImport(Document):
	pass

@frappe.whitelist()
def form_start_import(vtigercrm_import: str):
	return frappe.get_doc("VTigerCRM Import", vtigercrm_import).start_import()


def start_import(vtigercrm_import):
	"""This method runs in background job"""
	vtigercrm_import = frappe.get_doc("VTigerCRM Import", vtigercrm_import)
	try:
		i = Importer(vtigercrm_import.reference_doctype, vtigercrm_import=vtigercrm_import)
		i.import_data()
	except JobTimeoutException:
		frappe.db.rollback()
		vtigercrm_import.db_set("status", "Timed Out")
	except Exception:
		frappe.db.rollback()
		vtigercrm_import.db_set("status", "Error")
		vtigercrm_import.log_error("VTigerCRM import failed")
	finally:
		frappe.flags.in_import = False

	frappe.publish_realtime("vtigercrm_import_refresh", {"vtigercrm_import": vtigercrm_import.name})