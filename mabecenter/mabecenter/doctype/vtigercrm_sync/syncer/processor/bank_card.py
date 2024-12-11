from .base import EntityProcessor

class BankCardProcessor(EntityProcessor):
    def process(self, data: dict) -> dict:
        data['card_subtype'] = 'Debit' if data['card_subtype'] == 'Debito' else 'Credit'
        return data