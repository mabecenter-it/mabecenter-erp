// Copyright (c) 2024, Dante Devenir and contributors
// For license information, please see license.txt

frappe.ui.form.on("VTigerCRM Import", {
	setup(frm) {
		frm.has_import_file = () => {
			return frm.doc.import_file || frm.doc.google_sheets_url;
		};
	},
    onload_post_render(frm) {
		frm.trigger("update_primary_action");
	},
    update_primary_action(frm) {
		if (frm.is_dirty()) {
			frm.enable_save();
			return;
		}
		frm.disable_save();
		if (frm.doc.status !== "Success") {
			if (!frm.is_new() && frm.has_import_file()) {
				let label = frm.doc.status === "Pending" ? __("Start Import") : __("Retry");
				frm.page.set_primary_action(label, () => frm.events.start_import(frm));
			} else {
				frm.page.set_primary_action(__("Save"), () => frm.save());
			}
		}
	},
	start_import(frm) {
		frm.call({
			method: "form_start_import",
			args: { data_import: frm.doc.name },
			btn: frm.page.btn_primary,
		}).then((r) => {
			if (r.message === true) {
				frm.disable_save();
			}
		});
	},
});
