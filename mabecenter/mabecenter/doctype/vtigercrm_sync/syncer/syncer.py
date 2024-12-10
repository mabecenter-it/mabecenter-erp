import frappe

from sqlalchemy.orm import sessionmaker

from mabecenter.mabecenter.doctype.vtigercrm_sync.database.engine import engine
from mabecenter.mabecenter.doctype.vtigercrm_sync.models.vtigercrm_salesordercf import VTigerSalesOrderCF
from mabecenter.mabecenter.doctype.vtigercrm_sync.config.config import SyncConfig
from mabecenter.overrides.exception.sync_error import SyncError
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.handler.handler_factory import HandlerFactory
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.handler.progress_observer import FrappeProgressObserver
from mabecenter.mabecenter.doctype.vtigercrm_sync.syncer.handler.unit_of_work import UnitOfWork

class Syncer:
    def __init__(self, doc_name):
        self.doc_name = doc_name
        self.vtigercrm_sync = frappe.get_doc("VTigerCRM Sync", doc_name)
        self.handler_factory = HandlerFactory()
        self.progress_observer = FrappeProgressObserver()
        self.unit_of_work = UnitOfWork(lambda: sessionmaker(bind=engine)())
        self.config = SyncConfig()
            
        self.handlers = {
            entity_type: {
                'handler': self.handler_factory.create_handler(config['doctype']),
                'depends_on': config['depends_on']
            }
            for entity_type, config in self.config.handle_file.items()
        }
    
    def validate_connection(self):
        """Validate database connection and version"""
        try:
            from sqlalchemy import text
            with self.unit_of_work as session:
                result = session.execute(text("SELECT VERSION();"))
                version = result.fetchone()[0]
                frappe.logger().info(f"Successfully connected to VTigerCRM. Engine version: {version}")
        except Exception as e:
            frappe.logger().error(f"Database connection error: {str(e)}")
            raise SyncError("Failed to connect to VTigerCRM database") from e

    def sync(self):        
        try:
            with self.unit_of_work as session:  
                # Validate connection first
                self.validate_connection()
                
                results = (session.query(VTigerSalesOrderCF)
                    .filter(
                        VTigerSalesOrderCF.cf_2141.in_(self.config.status_values),
                        VTigerSalesOrderCF.cf_2059 == self.config.effective_date,
                        VTigerSalesOrderCF.cf_2179 >= self.config.sell_date
                    ).order_by(VTigerSalesOrderCF.salesorderid.desc())
                    .limit(1)
                    .all()
                )
                
                if not results:
                    frappe.logger().info("No records found for sync")
                    return True
                
                total_records = len(results)
                frappe.logger().info(f"Found {total_records} records to sync")
                
                for idx, record in enumerate(results, start=1):
                    try:
                        self.update_progress(idx/total_records)
                        self.process_record(record, self.config.mapping_file)
                    except Exception as e:
                        frappe.logger().error(f"Error processing record {idx}: {str(e)}")
                        raise SyncError(f"Failed to process record {idx}") from e
                
                return True
                
        except Exception as e:
            frappe.logger().error(f"Sync error: {str(e)}")
            raise

    def process_record(self, record, fields):
        customer, salesorder, contacts, address, pay, card, account = record.as_dict(fields)
        
        # Initialize results dictionary
        results = {}
        
        def process_entity(entity_type, data, **kwargs):
            if not data or entity_type not in self.handlers:
                return None
            
            # Ensure data is a dictionary and convert values appropriately
            processed_data = {}
            for k, v in data.items():
                if v is None:
                    processed_data[k] = None
                elif k in ['grand_total', 'conversion_rate']:
                    # Ensure numeric fields are properly converted
                    try:
                        processed_data[k] = float(v)
                    except (ValueError, TypeError):
                        processed_data[k] = 0.0
                else:
                    processed_data[k] = str(v)
            
            # Special handling for card data
            if entity_type == 'card' and not processed_data.get('Number'):
                return None
            
            # Special handling for sales order
            if entity_type == 'salesorder':
                if not processed_data.get('grand_total'):
                    processed_data['grand_total'] = 0.0
                if not processed_data.get('conversion_rate'):
                    processed_data['conversion_rate'] = 1.0
            
            handler_info = self.handlers[entity_type]
            dependencies = {}
            
            # Resolve dependencies
            for dep in handler_info['depends_on']:
                if dep in results:
                    dependencies[f"{dep}_name"] = results[dep].name if results[dep] else None
            
            try:
                result = handler_info['handler'].process(processed_data, **dependencies, **kwargs)
                results[entity_type] = result
                return result
            except Exception as e:
                frappe.logger().error(f"Error processing {entity_type}: {str(e)}")
                return None
        
        # Process entities in order of dependencies
        if card and card.get('card_number'):  # Only process card if Number exists
            process_entity('card', card)
        #process_entity('account', account)
        customer_doc = process_entity('customer', customer)
        
        # Process contacts and store them
        contact_docs = []
        for contact in contacts:
            contact_doc = process_entity('contact', contact)
            if contact_doc and customer_doc:
                contact_doc.append('links', {
                    'link_doctype': 'Customer',
                    'link_name': customer_doc.name
                })
                contact_doc.save()
                contact_docs.append(contact_doc)
        results['contacts'] = contact_docs
        
        # Process address with customer name
        if customer_doc:
            process_entity('address', address, customer_name=customer_doc.name)
        
        # Process salesorder
        salesorder_doc = process_entity('salesorder', salesorder)
        if salesorder_doc and contact_docs:
            # Skip the first contact as it's usually the main customer
            for contact_doc in contact_docs[1:]:
                salesorder_doc.append('custom_dependents', {
                    'contact': contact_doc.name
                })
            salesorder_doc.save()
        
        return results

    def update_progress(self, percentage):
        #frappe.publish_progress(percentage, title='Some title', description='Some description')
        frappe.publish_realtime(
            'vtigercrm_sync_refresh',
            {
                'percentage': f"{percentage * 100:.2f}",
                'vtigercrm_sync': self.doc_name
            }
        )