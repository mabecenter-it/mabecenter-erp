from .base import EntityProcessor

class CustomerProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        # Create customer data from owner information
        if not data:
            return {}
            
        customer_data = {
            'customer_name': f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
            'customer_type': 'Individual'
        }
        
        # Add optional fields if present
        if data.get('custom_day_of_birth'):
            customer_data['custom_day_of_birth'] = data['custom_day_of_birth']
            
        return customer_data