# Copyright (c) 2024, Dante Devenir and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _
from rq.timeouts import JobTimeoutException
from frappe.model.document import Document
from frappe.core.doctype.data_import.importer import Importer
from frappe.utils.background_jobs import enqueue, is_job_enqueued

class VTigerCRMImport(Document):
	def start_import(self):
		from frappe.utils.scheduler import is_scheduler_inactive

		run_now = frappe.flags.in_test or frappe.conf.developer_mode
		if is_scheduler_inactive() and not run_now:
			frappe.throw(_("Scheduler is inactive. Cannot import data."), title=_("Scheduler Inactive"))

		job_id = f"data_import::{self.name}"

		if not is_job_enqueued(job_id):
			enqueue(
				start_import,
				queue="default",
				timeout=10000,
				event="data_import",
				job_id=job_id,
				data_import=self.name,
				now=run_now,
			)
			return True

		return False

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