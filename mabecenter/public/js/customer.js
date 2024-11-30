frappe.ui.form.on("Customer", {
	refresh(frm) {
        frm.trigger("show_status_policy");
	},
    show_status_policy(frm) {
        /* let values = {
            base_url: frappe.urllib.get_base_url(),
            category: "Silver",
            plan_name: "Silver 5",
            company: "ambetter",
            premium: "42.32",
            deductible: "0.0",
            max_des: "1275"

            this.wrapper = $(`<div class="row
				${this.df.is_dashboard_section ? "form-dashboard-section" : "form-section"}
				${make_card ? "card-section" : ""}" data-fieldname="${this.df.fieldname}">
			`).appendTo(this.parent);frappe.template.compile(template

        } */
        console.log(frm.doc)
        frappe.call({
            method: "get_current_policy",
            doc: frm.doc,
            args: {
                customer: frm.doc.customer
            },
            freeze: true,
            callback: function(r) {
                console.log(r.message);
                let values = r.message;
                /* let custom_area = new Section({
                    label: __("Custom"),
                    css_class: "form-links",
                    hidden: 1,
                    collapsible: 1,
                    is_dashboard_section: 1,
                    body_html: frappe.render_template(frappe.templates.dashboard, values),
                });*/
                //frm.dashboard.add_section(frappe.render_template(frappe.templates.dashboard, values)); 
                frm.dashboard.policy_area_row.append(frappe.render_template(frappe.templates.dashboard, values));
                //frm.dashboard.policy_area_row.append(frappe.render_template(frappe.templates.index._index, values));
                //frm.dashboard.stats_area.df.collapsible = 0
                //custom_area.show();
                frm.dashboard.policy_area.show();
            }
        })
        if (false) {
            
            frm.dashboard.add_indicator(
                __("Self Appraisal Pending: {0}", [r.message.self_appraisal_pending]),
                "orange",
            );
            frm.dashboard.add_indicator(
                __("Employees without Feedback: {0}", [r.message.feedback_missing]),
                "orange",
            );
            frm.dashboard.add_indicator(
                __("Employees without Goals: {0}", [r.message.goals_missing]),
                "orange",
            );
        }
    }
})