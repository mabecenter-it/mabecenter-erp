// Copyright (c) 2024, Dante Devenir and contributors
// For license information, please see license.txt

frappe.ui.form.on("VTigerCRM Import", {
	setup(frm) {
		frm.has_import_file = () => {
			return frm.doc.import_file;
		};
		frm.toggle_display("section_import_preview", false);
		console.log("1 vez")
		frappe.realtime.on("vtigercrm_import_refresh", ({ vtigercrm_import }) => {
			frm.toggle_display("section_import_preview", true);
			/* frm.get_field("import_preview").$wrapper.empty();
			$('<span class="label label-primary text-love">')
				.html(__(`
					<div class="progress">
						<div class="progress-bar progress-bar-striped progress-bar-animated bg-primary" 
							role="progressbar" style="width: 0%;" 
							aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
							0%
						</div>
					</div>
				`))
				.appendTo(frm.get_field("import_preview").$wrapper); */
			frm.import_in_progress = false;
			if (vtigercrm_import !== frm.doc.name) return;
			frappe.model.clear_doc("VTigerCRM Import", frm.doc.name);
			frappe.model.with_doc("VTigerCRM Import", frm.doc.name).then(() => {
				frm.refresh();
			});
		});
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
			args: { vtigercrm_import: frm.doc.name },
			btn: frm.page.btn_primary,
		}).then((r) => {
			if (r.message === true) {
				frm.disable_save();
			}
		});
	},
});
