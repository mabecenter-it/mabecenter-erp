# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe


def get_context(context):
	if frappe.session.user == "Guest":
		raise frappe.PermissionError
	
	attendance = frappe.get_doc("Attendance", frappe.form_dict.attendance)

	attendance.has_permission("read")

	context.doc = attendance
	context.no_cache = 1
	context.show_sidebar = True