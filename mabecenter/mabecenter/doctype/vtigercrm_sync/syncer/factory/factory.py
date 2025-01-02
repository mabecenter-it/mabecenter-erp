from typing import Dict
from .handler.document import BaseDocumentHandler
from .handler.base import DocumentHandler

class HandlerFactory:
    @staticmethod
    def create_handlers() -> Dict[str, DocumentHandler]:
        handlers = {
            'Bank Card': BaseDocumentHandler('Bank Card'),
            'Customer': BaseDocumentHandler('Customer'),
            'Contact': BaseDocumentHandler('Contact'),
            'Address': BaseDocumentHandler('Address'),
            'Sales Order': BaseDocumentHandler('Sales Order'),
            'Bank Account': BaseDocumentHandler('Bank Account'),
        }
        return handlers

    @staticmethod
    def create_handler(doctype: str) -> DocumentHandler:
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