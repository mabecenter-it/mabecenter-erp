from .base import EntityProcessor

class AddressProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        if not data:
            return {}
            
        address_data = {
            'address_type': 'Shipping',
            'address_line1': data.get('address_line1'),
            'city': data.get('city'),
            'state': data.get('state'),
            'pincode': data.get('pincode'),
            'country': 'United States',
            'is_shipping_address': 1,
            'is_primary_address': 1
        }
        
        # Add optional address line 2 if present
        if data.get('address_line2'):
            address_data['address_line2'] = data['address_line2']
            
        return address_data
    
    def get_links(self, dependencies: dict) -> list:
        links = []
        if dependencies.get('customer'):
            links.append({
                'link_doctype': 'Customer',
                'link_name': dependencies['customer'].name
            })
        return links