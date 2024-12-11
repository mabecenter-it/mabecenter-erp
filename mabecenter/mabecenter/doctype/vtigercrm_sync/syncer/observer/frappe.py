import frappe
from .base import ProgressObserver

class FrappeProgressObserver(ProgressObserver):
    def update(self, percentage: float, context: dict):
        frappe.publish_realtime(
            'vtigercrm_sync_refresh',
            {
                'percentage': f"{percentage * 100:.2f}",
                'vtigercrm_sync': context['doc_name']
            }
        )
