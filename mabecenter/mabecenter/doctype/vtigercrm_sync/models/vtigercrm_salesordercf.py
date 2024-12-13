from datetime import date, datetime
from sqlalchemy import MetaData
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import engine
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.base import Base

metadata = MetaData()
metadata.reflect(bind=engine, only=['vtiger_salesordercf'])

class VTigerSalesOrderCF(Base):
    __table__ = metadata.tables['vtiger_salesordercf']

    def as_dict(self, mapping):
        # Convert database record to dictionary using provided mapping
        result = {c.key: getattr(self, c.key) for c in self.__table__.columns}
        
        # Process date values
        for key, value in result.items():
            if isinstance(value, date):
                result[key] = value.strftime("%Y-%m-%d")
                
        # Map fields according to provided mapping
        mapped_data = {}
        for entity_type, fields in mapping.items():
            entity_data = {}
            for descriptive_field, cf_field in fields.items():
                entity_data[descriptive_field] = result.get(cf_field)
            mapped_data[entity_type] = entity_data
            
        return mapped_data