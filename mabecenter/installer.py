def after_install():
    #create_bs_item()
    pass

def before_install():
    save_config_vtigercrm()

def create_bs_item():
    import frappe

    if not frappe.db.exists('Item', 'BS'):
        # Crear el nuevo item
        new_item = frappe.get_doc({
            'doctype': 'Item',
            'item_code': 'BS',
            'item_group': 'Services',
        })

        # Insertar el nuevo Item en la base de datos
        new_item.insert(ignore_permissions=True)

def save_config_vtigercrm():
    print("save_config_vtigercrm")
    """Save VTiger CRM configuration from environment variables to site config"""
    import os
    import frappe
    from frappe.installer import update_site_config
    frappe.logger("save_config_vtigercrm")
    # Environment variables
    vtiger_config = {
        "db_user_vtiger": os.getenv('VTIGER_USERNAME'),
        "db_password_vtiger": os.getenv('VTIGER_PASSWORD'),
        "db_host_vtiger": os.getenv('VTIGER_HOST'),
        "db_port_vtiger": os.getenv('VTIGER_PORT'),
        "db_name_vtiger": os.getenv('VTIGER_DB_NAME'),
    }

    # Update site config with VTiger settings
    for key, value in vtiger_config.items():
        if value:  # Only update if environment variable exists
            update_site_config(key, value) 