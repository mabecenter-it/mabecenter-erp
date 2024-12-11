from .document import BaseDocumentHandler
from .base import DocumentHandler

class HandlerFactory:
    @staticmethod
    def create_handler(doc_type: str) -> DocumentHandler:
        handlers = {
            'Bank Card': BaseDocumentHandler,
            'Customer': BaseDocumentHandler,
            'Contact': BaseDocumentHandler,
            'Address': BaseDocumentHandler,
            'Sales Order': BaseDocumentHandler,
            'Bank Account': BaseDocumentHandler,
        }
        handler_class = handlers.get(doc_type)
        if not handler_class:
            raise ValueError(f"No handler found for {doc_type}")
        return handler_class(doc_type)
