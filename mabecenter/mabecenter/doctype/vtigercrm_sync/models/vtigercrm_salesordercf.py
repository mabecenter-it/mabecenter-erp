from datetime import date, datetime
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.handler.entity_processors import AddressProcessor, BankCardProcessor, CustomerProcessor, SalesOrderProcessor
from sqlalchemy import MetaData
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import engine
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.base import Base

metadata = MetaData()
metadata.reflect(bind=engine, only=['vtiger_salesordercf'])

class VTigerSalesOrderCF(Base):
    __table__ = metadata.tables['vtiger_salesordercf']

    def as_dict(self, mapping, exclude_empty=True):
        result = {c.key: getattr(self, c.key) for c in self.__table__.columns}
        
        entity_processors = {
            'owner': CustomerProcessor().process,
            'card': BankCardProcessor().process,
            'salesorder': SalesOrderProcessor().process,
        }
        
        def process_field_value(value):
            return value.strftime("%Y-%m-%d") if isinstance(value, date) else value
        
        def process_entity_data(fields):
            data = {}
            has_data = False
            
            for descriptive_field, cf_field in fields.items():
                value = process_field_value(result.get(cf_field))
                data[descriptive_field] = value
                
                if value not in [None, '', 0, 0.0]:
                    has_data = True
                    
            return (data, has_data) if exclude_empty else (data, True)
        
        entities = {
            'customer': {},
            'salesorder': {},
            'contacts': [],
            'address': {},
            'pay': {},
            'card': {},
            'account': {}
        }
        
        for entity_type, fields in mapping.items():
            data, has_data = process_entity_data(fields)
            
            if not has_data:
                continue
                
            if entity_type in entity_processors:
                processed_data = entity_processors[entity_type](data)
                
                if entity_type == 'owner':
                    entities['customer'] = processed_data
                    entities['contacts'].append(processed_data)
                else:
                    entities[entity_type] = processed_data
            else:
                entities[entity_type] = data
        
        return (
            entities['customer'],
            entities['salesorder'],
            entities['contacts'],
            entities['address'],
            entities['pay'],
            entities['card'],
            entities['account']
        )