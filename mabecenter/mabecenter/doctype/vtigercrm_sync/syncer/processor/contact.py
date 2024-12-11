from .base import EntityProcessor


class ContactProcessor(EntityProcessor):
    def process(self, data):
        # Process the contact data - basic implementation
        processed_data = {
            **data
            # Add other relevant contact fields
        }
        return processed_data
    
    def get_links(self, dependencies: dict) -> list:
        # Generate links for the contact
        links = []
        # Add customer link if customer exists in dependencies
        if dependencies.get('customer'):
            links.append({
                'link_doctype': 'Customer',
                'link_name': dependencies['customer']
            })
        return links

    