from .base import EntityProcessor

class BankAccountProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        if not data:
            return {}
            
        account_data = {
            'account_name': data.get('account_name'),
            'bank': data.get('Bank'),
            'route_number': data.get('Ruta')
        }
        
        return account_data
    
    def get_links(self, dependencies: dict) -> list:
        links = []
        if dependencies.get('customer'):
            links.append({
                'link_doctype': 'Customer',
                'link_name': dependencies['customer'].name
            })
            
        return links