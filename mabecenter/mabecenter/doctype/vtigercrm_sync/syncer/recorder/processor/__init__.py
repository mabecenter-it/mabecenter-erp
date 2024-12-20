from .customer import CustomerProcessor
from .bank_card import BankCardProcessor
from .sales_order import SalesOrderProcessor
from .address import AddressProcessor
from .contact import ContactProcessor
from .base import EntityProcessor

__all__ = [
    'CustomerProcessor',
    'BankCardProcessor',
    'SalesOrderProcessor',
    'AddressProcessor',
    'ContactProcessor',
    'EntityProcessor'
]