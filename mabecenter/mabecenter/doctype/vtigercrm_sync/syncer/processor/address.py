from .base import EntityProcessor

class AddressProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        return {
            **data,
            'address_type': "Shipping",
            'country': "United states"
        }