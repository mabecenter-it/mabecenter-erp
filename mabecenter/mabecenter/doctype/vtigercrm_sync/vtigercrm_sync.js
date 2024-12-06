// Copyright (c) 2024, Dante Devenir and contributors
// For license information, please see license.txt

frappe.ui.form.on("VTigerCRM Sync", {
	setup(frm) {
		frm.toggle_display("section_sync_preview", false);
		frappe.realtime.on("vtigercrm_sync_refresh", ({ percentage }) => {
			//if (vtigercrm_sync !== frm.doc.name) return;
			let $html_wrapper = frm.get_field("sync_preview").$wrapper;
			$html_wrapper.empty();
			$('<div class="progress">')
			.append(
				$('<div class="progress-bar progress-bar-striped progress-bar-animated bg-primary">')
					.attr({
						'role': 'progressbar',
						'style': 'width: 0%;',
						'aria-valuenow': '0',
						'aria-valuemin': '0',
						'aria-valuemax': '100'
					})
					.text('0%')
			)
			.appendTo($html_wrapper);
			let $progress_bar = $html_wrapper.find('.progress-bar');
			$progress_bar.css('width', percentage + '%');
			$progress_bar.attr('aria-valuenow', percentage);
            $progress_bar.text(percentage + '%');
			frappe.model.clear_doc("VTigerCRM Sync", frm.doc.name);
			frappe.model.with_doc("VTigerCRM Sync", frm.doc.name).then(() => {
				frm.refresh();
			});
		})
	},
	onload(frm) {
		if (frm.is_new()) {
			frm.toggle_display("section_sync_preview", false);
		}
	},
	refresh(frm) {
        frm.toggle_display("section_sync_preview", false);
        frm.trigger("update_primary_action");
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
			if (!frm.is_new()) {
				let label = frm.doc.status === "Pending" ? __("Start Sync") : __("Retry");
				frm.page.set_primary_action(label, () => frm.events.start_sync(frm));
			} else {
				frm.page.set_primary_action(__("Save"), () => frm.save());
			}
		}
	},
	start_sync(frm) {
		frm.toggle_display("section_sync_preview", true);
		frm.call({
			method: "form_start_sync",
			args: { vtigercrm_sync: frm.doc.name },
			btn: frm.page.btn_primary,
		}).then((r) => {
			if (r.message === true) {
				frm.disable_save();
			}
		});
	},
});
