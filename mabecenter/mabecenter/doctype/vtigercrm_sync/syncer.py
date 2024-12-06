import frappe
import time

class Syncer:
	def __init__(self):
		for i in range(101):
			frappe.publish_realtime("vtigercrm_sync_refresh", {"percentage": i})
			time.sleep(0.05)