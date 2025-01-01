# Copyright (c) 2024, Dante Devenir and contributors
# For license information, please see license.txt

# Import Frappe framework components
import frappe
from frappe import _
# Import sync implementation
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.syncer import Syncer
# Import job timeout exception
from rq.timeouts import JobTimeoutException
# Import document base class
from frappe.model.document import Document
# Import background job utilities
from frappe.utils.background_jobs import enqueue, is_job_enqueued

class VTigerCRMSync(Document):
	def before_save(self):
		# Set sync timestamp before saving
		self.sync_on = self.creation

	def start_sync(self):
		# Import scheduler status check
		from frappe.utils.scheduler import is_scheduler_inactive

		# Determine if sync should run immediately
		run_now = frappe.flags.in_test or frappe.conf.developer_mode
		if is_scheduler_inactive() and not run_now:
			frappe.throw(_("Scheduler is inactive. Cannot import data."), title=_("Scheduler Inactive"))

		# Create unique job ID
		job_id = f"vtigercrm_sync::{self.name}"

		# Enqueue sync job if not already running
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

@frappe.whitelist(allow_guest=True)
def form_start_sync(vtigercrm_sync: str):
	# Start sync from form
	print("frappe.whitelist init")
	frappe.logger().info("frappe.whitelist init")
	return frappe.get_doc("VTigerCRM Sync", vtigercrm_sync).start_sync()


def start_sync(vtigercrm_sync):
	"""This method runs in background job"""
	print("start_sync init")
	frappe.logger().info("start_sync init")

	try:
		# Execute sync process
		Syncer(doc_name=vtigercrm_sync).sync()
	except JobTimeoutException:
		# Handle timeout
		frappe.db.rollback()
		doc = frappe.get_doc("VTigerCRM Sync", vtigercrm_sync)
		doc.db_set("status", "Timed Out")
	except Exception:
		# Handle general errors
		frappe.db.rollback()
		doc = frappe.get_doc("VTigerCRM Sync", vtigercrm_sync)
		doc.db_set("status", "Error")
		doc.log_error("VTigerCRM Sync failed")
	finally:
		# Reset import flag
		frappe.flags.in_import = False