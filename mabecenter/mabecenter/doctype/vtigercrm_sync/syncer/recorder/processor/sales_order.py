# mabecenter/mabecenter/doctype/vtigercrm_sync/syncer/processor/sales_order.py

from .base import EntityProcessor
from frappe import utils, defaults

class SalesOrderProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        if not data:
            return {}
            
        # Extract Sales Order specific data
        sales_order_data = data.get('Sales Order', {})
        
        order_data = {
            'doctype': 'Sales Order',
            'company': defaults.get_defaults().get('company', 'Mabe Center'),
            'currency': 'USD',
            'conversion_rate': 1.0,
            'selling_price_list': 'Standard Selling',
            'price_list_currency': 'USD',
            'transaction_date': sales_order_data.get('transaction_date', utils.today()),
            'delivery_date': sales_order_data.get('transaction_date', utils.today()),
            
            # Custom fields
            'custom_ffm_app_id': sales_order_data.get('custom_ffm_app_id'),
            'custom_subscriber_id': sales_order_data.get('custom_subscriber_id'),
            'custom_plan_hios_id': sales_order_data.get('custom_plan_hios_id'),
            'custom_plan_name': sales_order_data.get('custom_plan_name'),
            'custom_sales_person': sales_order_data.get('custom_sales_person'),
            'custom_sales_date': sales_order_data.get('custom_sales_date'),
            'custom_digitizer': sales_order_data.get('custom_digitizer'),
            'custom_digitizer_date': sales_order_data.get('custom_digitizer_date')
        }
        
        return order_data