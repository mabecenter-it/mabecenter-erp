frappe.ui.form.on('Sales Order', {
    onload: function(frm) {
        console.log("OK")
        //frm.fields_dict["custom_contact_relation"].grid.wrapper.find('.btn-custom-contact').remove();
        //frm.fields_dict["custom_patient_relation"].grid.wrapper.find('.btn-custom-patient').remove();
        //frm.fields_dict["custom_contact_relation"].grid.add_custom_button(__('Add Row'), function() {});
        //frm.fields_dict["custom_patient_relation"].grid.add_custom_button(__('Add Row'), function() {});
    }
});

/*frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm) {
        let row = frappe.get_doc(cdt, cdn);
        console.log("Dentro de item_code del Child Table");
        console.log(row);
    }
});*/

