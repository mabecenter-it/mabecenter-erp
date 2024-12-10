def after_migrate():
    create_bs_item()

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
    import os
    import frappe
    import json

    
    """Guardar la configuración de VTiger CRM desde las variables de entorno al archivo site_config.json"""
    
    # Variables de entorno
    vtiger_config = {
        "db_user_vtiger": os.getenv('VTIGER_USERNAME'),
        "db_password_vtiger": os.getenv('VTIGER_PASSWORD'),
        "db_host_vtiger": os.getenv('VTIGER_HOST'),
        "db_port_vtiger": os.getenv('VTIGER_PORT'),
        "db_name_vtiger": os.getenv('VTIGER_DB_NAME'),
    }

    # Obtener la ruta del archivo site_config.json
    site_config_path = frappe.get_site_config_path()

    # Cargar el archivo site_config.json
    with open(site_config_path, 'r') as f:
        site_config = json.load(f)

    # Actualizar la configuración con las variables de entorno
    for key, value in vtiger_config.items():
        if value:  # Solo actualizar si la variable de entorno está definida
            site_config[key] = value

    # Guardar los cambios en el archivo site_config.json
    with open(site_config_path, 'w') as f:
        json.dump(site_config, f, indent=4)

    frappe.msgprint("VTiger CRM configuración guardada correctamente.")
