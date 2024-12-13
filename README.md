# VTigerCRM Sync Module

## Structure

### Root Files
- `vtigercrm_sync.js`: Frontend controller for the VTigerCRM Sync form 
- `vtigercrm_sync.py`: Main DocType implementation with sync functionality
- `vtigercrm_sync.json`: DocType configuration
- `vtigercrm_sync.css`: Styles for the sync interface
- `vtigercrm_sync_list.js`: List view configuration for sync records
- 
### /database
- `base.py`: SQLAlchemy base configuration and declarative base class
- `engine.py`: Database connection configuration
- `unit_of_work.py`: Transaction management implementationKK

### /models
- `vtigercrm_salesordercf.py`: VTiger sales order custom fields model
- `vtigercrm_contact.py.old`: Legacy contact model (deprecated)

### /config
- `config.py`: Configuration management class
- `/mapping/`:
  - `salesorder.json`: Field mappings for sales orders
  - `handler.json`: Handler configurations for different entities

### /syncer
#### /syncer/handler
- `base.py`: Abstract base handler
- `document.py`: Base document handler implementation
- `factory.py`: Handler factory for creating appropriate handlers

#### /syncer/observer
- `base.py`: Abstract progress observer
- `frappe.py`: Frappe-specific progress observer implementation

#### /syncer/processor
- `base.py`: Abstract entity processor
- `sales_order.py`: Sales order processing logic
- `customer.py`: Customer data processing
- `bank_card.py`: Bank card information processing
- `address.py`: Address data processing
- `contact.py`: Contact information processing

#### /syncer/services
- `query.py`: Database query service implementation

### /doctype/vtigercrm_sync_log
- `vtigercrm_sync_log.json`: Log DocType configuration
- `vtigercrm_sync_log.py`: Log implementation
- `vtigercrm_sync_log.js`: Log form script

## Key Components

1. **Sync Engine**: Manages the synchronization process between VTiger CRM and Frappe
2. **Data Processors**: Handle specific entity type transformations
3. **Database Handlers**: Manage database connections and transactions
4. **Progress Tracking**: Real-time sync progress monitoring
5. **Error Handling**: Comprehensive error capture and logging

## Features

- Bidirectional sync between VTiger CRM and Frappe
- Real-time progress tracking
- Custom field mapping support
- Error logging and recovery
- Transaction management
- Entity relationship handling

Test app customize

#### License

mit