# Import required datetime types for handling dates
from datetime import date, datetime
# Import SQLAlchemy components for database operations
from sqlalchemy import MetaData
# Import database engine configuration
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import engine
# Import SQLAlchemy base class
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.base import Base
# Import entity processors for different data types
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.processor import (
    CustomerProcessor,
    BankCardProcessor,
    SalesOrderProcessor,
    AddressProcessor,
    ContactProcessor
)

# Create metadata object for table reflection
metadata = MetaData()
# Reflect only the vtiger_salesordercf table from database
metadata.reflect(bind=engine, only=['vtiger_salesordercf'])

class VTigerSalesOrderCF(Base):
    # Map class to existing database table
    __table__ = metadata.tables['vtiger_salesordercf']
    
    # Define default structure for entity data
    DEFAULT_ENTITIES = {
        'customer': {},        # Customer entity data
        'salesorder': {},      # Sales order data
        'contacts': [],        # List of contact entities
        'address': {},         # Address information
        'pay': {},            # Payment details
        'card': {},           # Bank card information
        'account': {}         # Bank account information
    }

    # Map entity types to their processors and target entities
    ENTITY_PROCESSORS = {
        'owner': ('customer', CustomerProcessor().process),      # Process owner as customer
        'card': ('card', BankCardProcessor().process),          # Process card details
        'salesorder': ('salesorder', SalesOrderProcessor().process),  # Process sales order
        'address': ('address', AddressProcessor().process),      # Process address
        'contact': ('contacts', ContactProcessor().process),     # Process contact info
    }

    def as_dict(self, mapping, exclude_empty=True):
        # Convert database record to dictionary using provided mapping
        result = {c.key: getattr(self, c.key) for c in self.__table__.columns}
        # Create copy of default entities structure
        entities = self.DEFAULT_ENTITIES.copy()
        
        def process_field_value(value):
            # Convert date objects to string format
            return value.strftime("%Y-%m-%d") if isinstance(value, date) else value
        
        def process_entity_data(fields):
            # Process fields for an entity type
            data = {}
            has_data = False
            
            # Map descriptive fields to custom field values
            for descriptive_field, cf_field in fields.items():
                value = process_field_value(result.get(cf_field))
                data[descriptive_field] = value
                
                # Check if field has meaningful value
                if value not in [None, '', 0, 0.0]:
                    has_data = True
                    
            return (data, has_data) if exclude_empty else (data, True)
        
        # Process each entity type in the mapping
        for entity_type, fields in mapping.items():
            data, has_data = process_entity_data(fields)
            
            # Skip if no data and excluding empty
            if not has_data:
                continue
                
            # Apply entity processor if available
            if entity_type in self.ENTITY_PROCESSORS:
                target_entity, processor = self.ENTITY_PROCESSORS[entity_type]
                processed_data = processor(data)
                
                # Handle special cases for contacts
                if entity_type in ['owner', 'spouse', 'dependent_1']:
                    entities['contacts'].append(processed_data)
                
                entities[target_entity] = processed_data
            else:
                # Store raw data if no processor defined
                entities[entity_type] = data
        
        return entities