from typing import Dict

from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.address import AddressHandler
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.bank_account import BankAccountHandler
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.bank_card import BankCardHandler
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.customer import CustomerHandler
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.factory.handler.sales_order import SalesOrderHandler
from .handler.contact import ContactHandler
from .handler.base import DocTypeHandler

class HandlerFactory:
    @staticmethod
    def create_handlers() -> Dict[str, DocTypeHandler]:
        handlers = {
            'Bank Card': BankCardHandler(),
            'Customer': CustomerHandler(),
            'Contact': ContactHandler(),
            'Address': AddressHandler(),
            'Sales Order': SalesOrderHandler(),
            'Bank Account': BankAccountHandler(),
        }
        return handlers

    @staticmethod
    def create_handler(doctype: str) -> DocTypeHandler:
        """
        Crea y devuelve un handler específico basado en el doctype proporcionado.
        
        Args:
            doctype (str): El nombre del doctype para el cual crear el handler.
        
        Returns:
            DocumentHandler: Una instancia del handler correspondiente.
        
        Raises:
            ValueError: Si no existe un handler para el doctype proporcionado.
        """
        handlers = HandlerFactory.create_handlers()
        handler = handlers.get(doctype)
        if not handler:
            raise ValueError(f"No existe un handler para el doctype: {doctype}")
        return handler