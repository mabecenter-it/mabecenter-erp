import frappe
from datetime import date
import json

class SyncConfig:
    def __init__(self):
        self.status_values = ['Active', 'Initial Enrollment', 'Sin Digitar']
        self.effective_date = date(2025, 1, 1)
        self.sell_date = date(2024, 10, 28)
        self.mapping_file = self._load_mapping('salesorder')
        self.handle_file = self._load_mapping('handler')

    def _load_mapping(self, filename):
        filename = frappe.get_app_path(
            'mabecenter', 'mabecenter', 'doctype', 
            'vtigercrm_sync', 'config', 'mapping', f'{filename}.json'
        )
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file) 