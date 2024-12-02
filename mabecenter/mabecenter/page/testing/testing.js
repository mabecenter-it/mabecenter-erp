frappe.pages["testing"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("testing"),
		single_column: true,
	});
};

frappe.pages["testing"].on_page_show = function (wrapper) {
	load_desk_page(wrapper);
};

function load_desk_page(wrapper) {
	let $parent = $(wrapper).find(".layout-main-section");
	$parent.empty();

	frappe.require("testing.bundle.js").then(() => {
		frappe.testing = new frappe.ui.Testing({
			wrapper: $parent,
			page: wrapper.page,
		});
	});
}