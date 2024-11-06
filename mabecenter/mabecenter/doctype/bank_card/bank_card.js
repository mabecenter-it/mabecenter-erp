// Copyright (c) 2024, Dante Devenir and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Bank Card", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Bank Card', {
    card_number: function(frm) {
        // Tomar el valor del campo card_number
        let card_number = frm.doc.card_number || '';

        // Verificar si el número de tarjeta tiene 15 o 16 caracteres
        if (card_number.length !== 15 && card_number.length !== 16) {
            frappe.msgprint(__('El número de tarjeta debe tener 15 o 16 dígitos.'));
            frm.set_value('card_type', '');
            return;
        }

        // Determinar el tipo de tarjeta basado en el primer dígito
        let card_type = '';
        if (card_number[0] == '3') {
            card_type = 'American Express';
        } else if (card_number[0] == '4') {
            card_type = 'Visa';
        } else if (card_number[0] == '5') {
            card_type = 'Mastercard';
        } else if (card_number[0] == '6') {
            card_type = 'Discovery';
        } else {
            frappe.msgprint(__('Number Card Invalid. Must start with 3 (American Express), 4 (Visa), 5 (Mastercard), or 6 (Discovery).'));
            frm.set_value('card_type', '');
            return;
        }

        // Actualizar el campo 'card_type' con el valor determinado
        frm.set_value('card_type', card_type);
    },/* ,
    onload: function(frm) {
        // Si el Card se está creando desde un Customer, establecer automáticamente el campo party
        console.log(frm.doc.customer)
        frm.set_value('party', frm.doc.customer);
    }, */
    /* setup: function (frm) {
		frm.set_query("party_type", function () {
			return {
				query: "erpnext.setup.doctype.party_type.party_type.get_party_type",
			};
		});
	}, */
    refresh: function(frm) {
        frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Bank Card' };

        // Mostrar los campos address_html y contact_html solo si el documento no es nuevo
        frm.toggle_display(['address_html', 'contact_html'], !frm.doc.__islocal);

        if (frm.doc.__islocal) {
            // Limpiar contactos y direcciones cuando el documento es nuevo
            frappe.contacts.clear_address_and_contact(frm);
        } else {
            // Renderizar los contactos y direcciones asociados al documento
            frappe.contacts.render_address_and_contact(frm);
        }

        if (!frm.is_new()) {
            frm.set_df_property('card_number', 'read_only', 1);
        }
	},

});
