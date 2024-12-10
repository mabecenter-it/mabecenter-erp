from frappe import utils
from abc import ABC, abstractmethod

class EntityProcessor(ABC):
    @abstractmethod
    def process(self, data: dict) -> dict:
        pass

class CustomerProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        return {
            **data,
            'customer_name': f"{data['first_name']} {data['last_name']}"
        }

class BankCardProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        data['card_type'] = 'Debit' if data['card_type'] == 'Debito' else 'Credit'
        return data

class AddressProcessor(EntityProcessor):
    def process(self, data: dict, customer_name) -> dict:
        return {
            **data,
            'address_title': customer_name,
            'address_type': "Shipping",
            'country': "United states"
        }
        
class SalesOrderProcessor(EntityProcessor):
    def process(self, data: dict):
        # Asegurar campos numéricos
        grand_total = float(data.get('grand_total', 0))
        conversion_rate = float(data.get('conversion_rate', 1))
        base_grand_total = float(data.get(grand_total * conversion_rate, 0))
        commission_rate = float(data.get('commission_rate', 0))
        total_commission = float(data.get('total_commission', 0))
        
        # Crear la lista para payment_schedule como lista de diccionarios
        payment_schedule = [{
            'doctype': 'Payment Schedule',
            'payment_term': 'Full Payment',
            'invoice_portion': 100,
            'due_date': data.get('transaction_date', utils.today())
        }]
        
        # Construir el diccionario final con valores por defecto adecuados
        processed_data = {
            **data,
            'doctype': data.get('doctype', 'Sales Order'),
            'grand_total': grand_total,
            'base_grand_total': base_grand_total,
            'delivery_date': data.get('transaction_date', utils.today()),
            'currency': data.get('currency', 'USD'),
            'conversion_rate': conversion_rate,
            'commission_rate': commission_rate,
            'amount_eligible_for_commission': 0,
            'total_commission': total_commission,
        }
        
        # Convertir a float si algún campo numérico viene como string
        numeric_fields = ['commission_rate', 'amount_eligible_for_commission', 'total_commission']
        for field in numeric_fields:
            val = processed_data.get(field)
            if isinstance(val, str):
                processed_data[field] = float(val or 0)
                
        return processed_data