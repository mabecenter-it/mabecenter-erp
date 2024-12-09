from datetime import date, datetime
from sqlalchemy import MetaData
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import engine
from mabecenter.mabecenter.doctype.vtigercrm_sync.database.base import Base

metadata = MetaData()
metadata.reflect(bind=engine, only=['vtiger_salesordercf'])

class VTigerSalesOrderCF(Base):
    __table__ = metadata.tables['vtiger_salesordercf']

    def as_dict(self, mapping, exclude_empty = True):
        # Get the mapped columns as key-value pairs
        result = {c.key: getattr(self, c.key) for c in self.__table__.columns}

        contacts = []

        for relationship, fields in mapping.items():
            contact = {}
            has_data = False

            # Iterate over each descriptive field and its corresponding custom field
            for descriptive_field, cf_field in fields.items():
                value = result.get(cf_field)
                converted_value = value.strftime("%Y-%m-%d") if isinstance(value, date) else value
                contact[descriptive_field] = converted_value

                # Check if the contact has meaningful data
                if converted_value not in [None, '', 0, 0.0]:
                    has_data = True

            # Optionally exclude contacts without meaningful data
            if exclude_empty and not has_data:
                continue  # Skip adding this contact

            contacts.append(contact)

        return contacts
