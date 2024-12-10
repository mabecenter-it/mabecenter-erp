import frappe
from abc import ABC, abstractmethod

class ProgressObserver(ABC):
    @abstractmethod
    def update(self, percentage: float, context: dict):
        pass

class FrappeProgressObserver(ProgressObserver):
    def update(self, percentage: float, context: dict):
        frappe.publish_realtime(
            'vtigercrm_sync_refresh',
            {
                'percentage': f"{percentage * 100:.2f}",
                'vtigercrm_sync': context['doc_name']
            }
        ) 