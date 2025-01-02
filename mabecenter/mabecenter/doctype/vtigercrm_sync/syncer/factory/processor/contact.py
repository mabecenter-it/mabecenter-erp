from .base import EntityProcessor

class ContactProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        if not data:
            return {}
            
        contact_data = {}
        contact_info = data.get('Contact', {})
        
        # Process owner contact (primary)
        owner = contact_info.get('owner', {})
        if owner:
            contact_data = {
                'first_name': owner.get('first_name', ''),
                'last_name': owner.get('last_name', ''),
                'custom_day_of_birth': owner.get('custom_day_of_birth'),
                'is_primary_contact': 1
            }
            
        return contact_data
    
    def process_additional_contacts(self, data: dict) -> list:
        """Process spouse and dependent contacts"""
        contacts = []
        contact_info = data.get('Contact', {})
        
        # Process spouse contact
        spouse = contact_info.get('spouse', {})
        if spouse:
            contacts.append({
                'first_name': spouse.get('first_name', ''),
                'last_name': spouse.get('last_name', ''),
                'custom_day_of_birth': spouse.get('custom_day_of_birth'),
                'is_primary_contact': 0
            })
            
        # Process dependent contact
        dependent = contact_info.get('dependent_1', {})
        if dependent:
            contacts.append({
                'first_name': dependent.get('first_name', ''),
                'last_name': dependent.get('last_name', ''),
                'custom_day_of_birth': dependent.get('custom_day_of_birth'),
                'is_primary_contact': 0
            })
            
        return contacts