let imports_in_progress = [];

frappe.listview_settings["VTigerCRM Sync"] = {
	onload(listview) {
		frappe.realtime.on("vtigercrm_sync_progress", (data) => {
			if (!imports_in_progress.includes(data.vtigercrm_sync)) {
				imports_in_progress.push(data.vtigercrm_sync);
			}
		});
		frappe.realtime.on("vtigercrm_sync_refresh", (data) => {
			imports_in_progress = imports_in_progress.filter((d) => d !== data.vtigercrm_sync);
			listview.refresh();
		});
	},
	get_indicator: function (doc) {
		var colors = {
			Pending: "orange",
			"Not Started": "orange",
			"Partial Success": "orange",
			Success: "green",
			"In Progress": "orange",
			Error: "red",
			"Timed Out": "orange",
		};
		let status = doc.status;

		if (imports_in_progress.includes(doc.name)) {
			status = "In Progress";
		}
		return [__(status), colors[status], "status,=," + doc.status];
	},
	formatters: {
		import_type(value) {
			return {
				"Insert New Records": __("Insert"),
				"Update Existing Records": __("Update"),
			}[value];
		},
	},
	hide_name_column: true,
};