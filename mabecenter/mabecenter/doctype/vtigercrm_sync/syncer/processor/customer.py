from .base import EntityProcessor

class CustomerProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        processed = {
            **data,
            'customer_name': f"{data['first_name']} {data['last_name']}"
        }
        
        if 'card' in data:
            processed['default_bank_card'] = data['card']
        if 'account' in data:
            processed['default_bank_account'] = data['account']
            
        return processed