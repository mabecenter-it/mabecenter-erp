from .base import EntityProcessor
from frappe import utils, defaults

class SalesOrderProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        # Asegurar campos numéricos
        grand_total = float(data.get('grand_total', 0))
        conversion_rate = float(data.get('conversion_rate', 1))
        base_grand_total = float(data.get(grand_total * conversion_rate, 0))
        commission_rate = float(data.get('commission_rate', 0))
        total_commission = float(data.get('total_commission', 0)) 
        base_amount = float(data.get('base_amount', 0))
        
        # Crear la lista para payment_schedule como lista de diccionarios
        payment_schedule = [{
            'doctype': 'Payment Schedule',
            'payment_term': 'Full Payment',
            'invoice_portion': 100,
            'due_date': data.get('transaction_date', utils.today())
        }]
        
        # Create the sales order items list
        sales_order_items = [{
            "doctype": "Sales Order Item",  # Added doctype specification
            "item_code": "BS",
            "qty": 1,
            "rate": 0.0,
            "warehouse": "Stores - MC"
        }]
        
        # Build the processed data dictionary
        processed_data = {
            'doctype': 'Sales Order',
            'company': defaults.get_defaults().get('company', 'Mabe Center'),
            'currency': data.get('currency', 'USD'),
            'conversion_rate': float(data.get('conversion_rate', 1.0)),
            'selling_price_list': 'Standard Selling',
            'price_list_currency': 'USD',
            'delivery_date': data.get('transaction_date', utils.today()),
            'transaction_date': data.get('transaction_date', utils.today()),
            'items': sales_order_items,  # Keep as list, don't convert to string
            'custom_ffm_app_id': data.get('custom_ffm_app_id', ''),
            'custom_subscriber_id': data.get('custom_subscriber_id', ''),
            'custom_plan_hios_id': data.get('custom_plan_hios_id', ''),
            'custom_plan_name': data.get('custom_plan_name', ''),
            'custom_sales_person': data.get('custom_sales_person', ''),
            'custom_sales_date': data.get('custom_sales_date'),
            'custom_digitizer': data.get('custom_digitizer', ''),
            'custom_digitizer_date': data.get('custom_digitizer_date')
        }
        
        # Remove the JSON conversion for lists
        # Only convert numeric fields as needed
        numeric_fields = ['conversion_rate']
        for field in numeric_fields:
            val = processed_data.get(field)
            if isinstance(val, str):
                processed_data[field] = float(val or 0)
                
        return processed_data
    
    def get_child_tables(self, dependencies: dict) -> dict:
        """ 'payment_schedule': [{
                'doctype': 'Payment Schedule',
                'payment_term': 'Full Payment',
                'invoice_portion': 100,
                'due_date': utils.today()
            }], """
        return {
            'items': [{
                "doctype": "Sales Order Item",
                "item_code": "BS",
                "qty": 1,
                "rate": 0.0,
                "warehouse": "Stores - MC"
            }],
            'custom_dependents': [
                {'contact': contact.name}
                for contact in (dependencies.get('contacts') or [])
                if contact  # Filter out None values
            ]
        }