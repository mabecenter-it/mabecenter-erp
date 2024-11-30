from frappe import _

def get_setup_stages(args=None):
	return [
		{
			"status": _("Wrapping up"),
			"fail_msg": _("Failed to login"),
			"tasks": [{"fn": fin, "args": args, "fail_msg": _("Failed to login")}],
		},
	]

def fin(args):
	pass