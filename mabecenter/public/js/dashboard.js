class CustomFormDashboard extends frappe.ui.form.Dashboard {
    constructor(parent, frm) {
        // Primero, configura la sección personalizada
        super(parent, frm);
        this.setup_policy_area();

        // Luego, reconfigura las secciones para asegurar que la nueva sección aparezca primero
        this.reorder_sections();
    }

    // Método para configurar la sección personalizada
    setup_policy_area() {
        this.policy_area_row = $(`<div class="row"></div>`);
        this.policy_area = this.make_section({
            label: __('<div class="typography-module__avenir20___P6Onc colors-module__royal___DNLA3" data-public="true">Plans&nbsp;<span class="typography-module__avenir14___G860v colors-module__slate5___GdMkG">2024</span></div>'),
            css_class: "policy-area hs-bg",
            hidden: 1,
            collapsible: 0,
            is_dashboard_section: 1,
            body_html: this.policy_area_row,
        });
    }

    // Método para reordenar las secciones y asegurar que policy_area aparezca primero
    reorder_sections() {
        this.parent.prepend(this.policy_area.wrapper);
    }

    // Método opcional para refrescar la sección personalizada
    refresh() {
        super.refresh();
        this.refresh_policy_area();
    }

    refresh_policy_area() {
        // Lógica para refrescar el contenido de la sección personalizada
        this.policy_area_row.empty();
		this.policy_area.hide();
		/* const labelElement = document.querySelector('.section-head');
        if (labelElement) {
            const labelText = labelElement.innerHTML;
            labelElement.innerHTML = labelText.replace(/(2024)/g, '<span class="highlight">$1</span>');
        } */
    }
}

// Sobrescribe el dashboard del formulario con tu clase personalizada
frappe.ui.form.Dashboard = CustomFormDashboard;