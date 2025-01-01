from datetime import date
from sqlalchemy import MetaData
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import get_engine
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.base import Base

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_salesordercf'])

class VTigerSalesOrderCF(Base):
    __table__ = metadata.tables['vtiger_salesordercf']

    def as_dict(self, mapping):
        """
        Convierte un registro de base de datos a un diccionario utilizando el mapeo proporcionado.
        Soporta mapeos anidados para manejar entidades como 'Contact' con subentidades.
        
        :param mapping: Diccionario que define el mapeo de campos.
        :return: Diccionario mapeado.
        """
        # Convertir el registro de la base de datos a un diccionario
        result = {c.key: getattr(self, c.key) for c in self.__table__.columns}
        
        # Procesar valores de fecha
        for key, value in result.items():
            if isinstance(value, date):
                result[key] = value.strftime("%Y-%m-%d")
        
        def map_fields(fields_mapping, data):
            """
            Mapea campos según el mapeo proporcionado. Soporta mapeos anidados.
            
            :param fields_mapping: Diccionario de mapeo de campos.
            :param data: Diccionario de datos originales.
            :return: Diccionario mapeado.
            """
            mapped = {}
            for descriptive_field, cf_field in fields_mapping.items():
                if isinstance(cf_field, dict):
                    # Si el valor es un diccionario, procesarlo recursivamente
                    mapped[descriptive_field] = map_fields(cf_field, data)
                else:
                    mapped[descriptive_field] = data.get(cf_field)
            return mapped
        
        # Mapear los campos según el mapeo proporcionado
        mapped_data = {}
        for entity_type, fields in mapping.items():
            mapped_data[entity_type] = map_fields(fields, result)
                    
        return mapped_data
