frappe.provide("configurator.setup");

frappe.pages["setup-wizard"].on_page_load = function (wrapper) {
	if (frappe.sys_defaults.company) {
		frappe.set_route("desk");
		return;
	}
};

frappe.setup.on("before_load", function () {
	configurator.setup.slides_settings.map(frappe.setup.add_slide);
});

configurator.setup.slides_settings = [
	{
		// Organization
		name: "organization",
		title: __("Setup your mother"),
		icon: "fa fa-building",
		fields: [
			{
				fieldname: "company_name",
				label: __("Company Name"),
				fieldtype: "Data",
				reqd: 1,
			}
		],

		/* onload: function (slide) {
			this.create_general_item(slide);
		}, */
	}
]
