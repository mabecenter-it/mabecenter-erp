# Copyright (c) 2024, Dante Devenir and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer import Syncer
from rq.timeouts import JobTimeoutException
from frappe.model.document import Document

from frappe.utils.background_jobs import enqueue, is_job_enqueued

class VTigerCRMSync(Document):
	def before_save(self):
		self.sync_on = self.creation

	def start_sync(self):
		from frappe.utils.scheduler import is_scheduler_inactive

		run_now = frappe.flags.in_test or frappe.conf.developer_mode
		if is_scheduler_inactive() and not run_now:
			frappe.throw(_("Scheduler is inactive. Cannot import data."), title=_("Scheduler Inactive"))

		job_id = f"vtigercrm_sync::{self.name}"

		if not is_job_enqueued(job_id):
			enqueue(
				start_sync,
				queue="default",
				timeout=10000,
				event="vtigercrm_sync",
				job_id=job_id,
				vtigercrm_sync=self.name,
				now=run_now,
			)
			return True

		return False

@frappe.whitelist()
def form_start_sync(vtigercrm_sync: str):
	return frappe.get_doc("VTigerCRM Sync", vtigercrm_sync).start_sync()


def start_sync(vtigercrm_sync):
	"""This method runs in background job"""
	
	try:
		syncer = Syncer(doc_name=vtigercrm_sync)
		success = syncer.sync()
	except JobTimeoutException:
		frappe.db.rollback()
		vtigercrm_sync.db_set("status", "Timed Out")
	except Exception:
		frappe.db.rollback()
		vtigercrm_sync.db_set("status", "Error")
		vtigercrm_sync.log_error("VTigerCRM Sync failed")
	finally:
		frappe.flags.in_import = False