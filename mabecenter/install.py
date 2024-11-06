def after_migrate():
    create_bs_item()

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
