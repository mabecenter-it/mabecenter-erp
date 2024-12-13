from .base import EntityProcessor

class BankCardProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        if not data:
            return {}
            
        card_data = {
            'doctype': 'Bank Card',
            'card_number': data.get('card_number'),
            'expiration': data.get('expiration'),
            'card_type': self._determine_card_type(data),
            'autopay': data.get('autopay', 0),
            'paid': data.get('paid', 0)
        }
        
        # Add address fields if present
        if data.get('zipcode'):
            card_data.update({
                'zipcode': data.get('zipcode'),
                'address1': data.get('address1'),
                'address2': data.get('address2')
            })
            
        return card_data
    
    def _determine_card_type(self, data: dict) -> str:
        subtype = data.get('card_subtype', '').lower()
        if 'debito' in subtype:
            return 'Debit'
        return 'Credit'
    
    def get_links(self, dependencies: dict) -> list:
        links = []
        if dependencies.get('customer'):
            links.append({
                'link_doctype': 'Customer',
                'link_name': dependencies['customer'].name
            })
        return links