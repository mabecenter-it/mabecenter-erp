(() => {
  // ../mabecenter/mabecenter/public/js/dashboard.js
  var CustomFormDashboard = class extends frappe.ui.form.Dashboard {
    constructor(parent, frm) {
      super(parent, frm);
      this.setup_policy_area();
      this.reorder_sections();
    }
    setup_policy_area() {
      this.policy_area_row = $(`<div class="row"></div>`);
      this.policy_area = this.make_section({
        label: __('<div class="typography-module__avenir20___P6Onc colors-module__royal___DNLA3" data-public="true">Plans&nbsp;<span class="typography-module__avenir14___G860v colors-module__slate5___GdMkG">2024</span></div>'),
        css_class: "policy-area hs-bg",
        hidden: 1,
        collapsible: 0,
        is_dashboard_section: 1,
        body_html: this.policy_area_row
      });
    }
    reorder_sections() {
      this.parent.prepend(this.policy_area.wrapper);
    }
    refresh() {
      super.refresh();
      this.refresh_policy_area();
    }
    refresh_policy_area() {
      this.policy_area_row.empty();
      this.policy_area.hide();
    }
  };
  frappe.ui.form.Dashboard = CustomFormDashboard;

  // frappe-html:/workspace/development/frappe-bench/apps/mabecenter/mabecenter/templates/dashboard.html
  frappe.templates["dashboard"] = `<div class="col-sm-12">
    <!-- <div class="hs-plans-label m-2">
        <svg focusable="false" aria-hidden="true" viewBox="0 0 18 18" width="20px">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12.2799 2.36298V5.7196H15.6352C16.0494 5.7196 16.3852 6.05539 16.3852 6.4696V11.5315C16.3852 11.9457 16.0494 12.2815 15.6352 12.2815H12.2799V15.637C12.2799 16.0512 11.9441 16.387 11.5299 16.387H6.46948C6.05526 16.387 5.71948 16.0512 5.71948 15.637V12.2815H2.36523C1.95102 12.2815 1.61523 11.9457 1.61523 11.5315V6.4696C1.61523 6.05539 1.95102 5.7196 2.36523 5.7196H5.71948V2.36298C5.71948 1.94876 6.05526 1.61298 6.46948 1.61298H11.5299C11.9441 1.61298 12.2799 1.94876 12.2799 2.36298ZM10.7799 11.5315C10.7799 11.1173 11.1156 10.7815 11.5299 10.7815H14.8852V7.2196H11.5299C11.1156 7.2196 10.7799 6.88382 10.7799 6.4696V3.11298H7.21948V6.4696C7.21948 6.88382 6.88369 7.2196 6.46948 7.2196H3.11523V10.7815H6.46948C6.88369 10.7815 7.21948 11.1173 7.21948 11.5315V14.887H10.7799V11.5315Z" fill="currentColor"></path>
        </svg>
        <span>Health plan</span>
        
    </div> -->
    <div class="row">
        <div class="col-sm-6 col-xs-12">
            <div class="typography-module__avenirBold16___eAfIA colors-module__royal___DNLA3" data-public="true">
                <svg class="MuiSvgIcon-root MuiSvgIcon-fontSizeLarge css-1ol1nt9" focusable="false" aria-hidden="true" viewBox="0 0 18 18" data-testid="HealthIconIcon">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M12.2799 2.36298V5.7196H15.6352C16.0494 5.7196 16.3852 6.05539 16.3852 6.4696V11.5315C16.3852 11.9457 16.0494 12.2815 15.6352 12.2815H12.2799V15.637C12.2799 16.0512 11.9441 16.387 11.5299 16.387H6.46948C6.05526 16.387 5.71948 16.0512 5.71948 15.637V12.2815H2.36523C1.95102 12.2815 1.61523 11.9457 1.61523 11.5315V6.4696C1.61523 6.05539 1.95102 5.7196 2.36523 5.7196H5.71948V2.36298C5.71948 1.94876 6.05526 1.61298 6.46948 1.61298H11.5299C11.9441 1.61298 12.2799 1.94876 12.2799 2.36298ZM10.7799 11.5315C10.7799 11.1173 11.1156 10.7815 11.5299 10.7815H14.8852V7.2196H11.5299C11.1156 7.2196 10.7799 6.88382 10.7799 6.4696V3.11298H7.21948V6.4696C7.21948 6.88382 6.88369 7.2196 6.46948 7.2196H3.11523V10.7815H6.46948C6.88369 10.7815 7.21948 11.1173 7.21948 11.5315V14.887H10.7799V11.5315Z" fill="currentColor"></path>
                </svg> 
                Health plan
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-sm-6 col-xs-12">
            <div class="layouts-module__my15___zruiT">
                <span class="MuiBox-root css-0" data-public="true">
                    <div class="box-module__box___khUTV box-module__floatHigh___a50ox box-module__white___ZCWj8 box-module__boxMd___RnCHM">
                        <div class="box-module__header___ZQaCf">
                            <div class="layouts-module__pt20___jhIUM layouts-module__pb15___NHkN7">
                                <div class="typography-module__avenir14___G860v layouts-module__flex___vBBZi layouts-module__flexBetween___UVg8g">
                                    <div style="width: 66%;"><img src="/assets/configurator/icons/{{company}}.png" alt="UnitedHealthcare" class="issuer-logo" data-public="true" style="min-height: 0px; max-height: 30px; max-width: 100%; width: auto;">
                                    </div>
                                    <div style="display: flex; margin-top: -10px;">
                                        <div class="metal_badge-module__metal___kjebu metal_badge-module__sm___VlcbJ">
                                            <img alt="Silver-badge" class="metal_badge-module__icon___VjlSA metal_badge-module__iconSm___mAfVw" src="/assets/configurator/icons/styleguide/metals/{{category}}.png">
                                            <div class="inline-block metal_badge-module__metalLabel___ukBfN metal_badge-module__silver___Jq0_e">{{category}}</div>
                                        </div>
                                        <span class="layouts-module__ml6___PY2sV layouts-module__flex___vBBZi">
                                            <span class="layouts-module__mt4___V2pmP">+</span>
                                            &nbsp;
                                            <img class="csr_badge-module__badge___Qg6LR" src="/assets/configurator/icons/csr.png" alt="csr-badge">
                                        </span>
                                    </div>
                                </div>
                                <div class="layouts-module__pb0____S1ng layouts-module__mt10___Rk7LF layouts-module__block___hy1HS">{{plan_name}} - {{plan_type}}</div>
                                <div class="layouts-module__block___hy1HS colors-module__slate5___GdMkG">{{plan_code}}</div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-xs-4" style="text-align: center;">
                                <span class="typography-module__avenir20___P6Onc">
                                    <strong>
                                        <sup class="typography-module__avenir12___UNfvY" style="position: relative; bottom: 0.55em;">$</sup>
                                        {{premium}}
                                    </strong>
                                </span>
                                <div>
                                    <span class="typography-module__avenir12___UNfvY colors-module__slate5___GdMkG" style="position: relative; top: -3px;">Premium</span>
                                </div>
                                <span class="colors-module__red3___B67ho typography-module__avenir11___J9knq effects-module__strikethrough___AxSwd layouts-module__block___hy1HS" style="margin-top: -7px;">
                                    Was <span>$</span>{{total_premium}}
                                </span>
                            </div>
                            <div class="col-xs-4" style="text-align: center;">
                                <span class="typography-module__avenir20___P6Onc">
                                    <span>
                                        <sup class="typography-module__avenir12___UNfvY" style="position: relative; bottom: 0.55em;">$</sup>
                                        {{deductible}}
                                    </span>
                                </span>
                                <div>
                                    <span class="typography-module__avenir12___UNfvY colors-module__slate5___GdMkG" style="position: relative; top: -3px;">Deductible</span>
                                </div>
                            </div>
                            <div class="col-xs-4" style="text-align: center;">
                                <span class="typography-module__avenir20___P6Onc">
                                    <sup class="typography-module__avenir12___UNfvY" style="position: relative; bottom: 0.55em;">$</sup>
                                    {{max_des}}
                                </span>
                                <div>
                                    <span class="typography-module__avenir12___UNfvY colors-module__slate5___GdMkG" style="position: relative; top: -3px;">OOP max</span>
                                </div>
                            </div>
                        </div>
                        <div class="box-module__footer___gGsJL">
                            <div class="text-center layouts-module__my10___DveeP typography-module__avenir14___G860v row">
                                <div class="col-sm-6 col-xs-12">
                                    <a href="/agents/ana-daniella-corrales/clients/553277558282/plan?ffm_policy_id=83729161" data-public="true" style="cursor: pointer;">View full plan details</a>
                                </div>
                                <div class="col-sm-6 col-xs-12">
                                    <a target="_blank" href="https://www.uhc.com/content/dam/uhcdotcom/en/ifp/sbc/fl/sbc.68398FL0030040-06.en.2024.pdf" data-public="true">View summary of benefits</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </span>
            </div>
        </div>
        <div class="col-sm-6 col-xs-12">
            <div class="layouts-module__mt15___Q9oBN">
                <div class="mobile_table-module__underlined___PdfOb">
                    <div class="mobile_table-module__section___UdbIc effects-module__slateBorderBottom___QTEjR layouts-module__pb20___pt574 layouts-module__mb20___mUYnF">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Status</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span>
                                            <span>
                                                <svg class="MuiSvgIcon-root MuiSvgIcon-colorSuccess MuiSvgIcon-fontSizeMedium css-14x16ip" focusable="false" aria-hidden="true" viewBox="-1 -1 18 18" data-testid="CheckEncircledIconIcon" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M8 16C12.4183 16 16 12.4183 16 8C16 3.58172 12.4183 0 8 0C3.58172 0 0 3.58172 0 8C0 12.4183 3.58172 16 8 16ZM12.2592 4.03497C11.9136 3.65501 11.3312 3.65501 10.9855 4.03497L6.68684 9.47041L5.01769 7.59469C4.66855 7.21082 4.08763 7.21082 3.74123 7.58968C3.41973 7.94491 3.41973 8.49801 3.74037 8.85049L6.074 11.4672C6.2383 11.6459 6.46767 11.75 6.70942 11.75C6.95179 11.75 7.18043 11.646 7.34483 11.4672L12.2805 5.26982C12.58 4.9422 12.58 4.38761 12.2592 4.03497Z" fill="currentColor"></path></svg>
                                                {{status}}
                                            </span>
                                        </span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Effective</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span>{{effective}}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Expiration</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span>{{expiration}}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Members</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="notranslate" style="font-family: inherit; font-size: inherit; font-weight: inherit;">{{owner}}</span>
                                        {% if (members.length > 0) { %}
                                            {% for (const member of members) { %}
                                                <br>
                                                <span class="notranslate" style="font-family: inherit; font-size: inherit; font-weight: inherit;">{%= member.patient %}</span>
                                            {% } %}
                                        {% } %}
                                        
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Subscriber ID</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="notranslate" style="font-family: inherit; font-size: inherit; font-weight: inherit;">{{subscriber_id}}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">FFM ID</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="notranslate" style="font-family: inherit; font-size: inherit; font-weight: inherit;">{{ffm_id}}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Carrier phone</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span>{{carrier_phone}}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span class="MuiBox-root css-0" data-public="true">Payment phone</span>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span>{{payment_phone}}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="typography-module__avenirBold14___BK87c colors-module__royal___DNLA3 layouts-module__pr20___FVS4h layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <div class="layouts-module__pr6___yZzqr" style="white-space: nowrap;">
                                            <span class="MuiBox-root css-0" data-public="true">Agent of Record</span>
                                            <div style="display: inline-block;">
                                                <span tabindex="0" role="button">
                                                    <img alt="help" src="/assets/configurator/icons/enroll/help_icon_grey@2x.png" style="height: 14px; position: relative; bottom: 1px; margin: 0px 2px;">
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="typography-module__avenir14___G860v layouts-module__pb4____P0xG mobile_table-module__td___J6qCB">
                                        <span>
                                            <span>{{broker}} (NPN: {{npn}})</span>
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="MuiStack-root css-vtsccc">
                <button class="buttons-module__smallOutline___Tfra7" tabindex="0" type="button" data-public="true">Cancel plan</button>
            </div>
        </div>
        <div class="col-sm-6 col-xs-12">
            <div></div>
        </div>
    </div>
    <!-- <div class="row">
        <div class="col-sm-6">
            <div class="card">
                <div class="row plan-prices">
                    <div class="plan-type col-sm-3">
                        <img src="https://s3.amazonaws.com/healthsherpa_hcgov_files_prod/insurance_full/issuers/logos/000/000/343/original/1_uhc.png?1651247734" alt="UnitedHealthcare" class="issuer-logo" data-public="true" style="min-height: 0px; max-height: 30px; max-width: 100%; width: auto;">
                        <!--<img src="/assets/configurator/img/{{ company }}.png" alt="Logo1" class="logo">
                    </div>
                    <div style="display: flex; margin-top: -10px;">
                        <div class="metal_badge-module__metal___kjebu metal_badge-module__sm___VlcbJ">
                            <img alt="Silver-badge" class="metal_badge-module__icon___VjlSA metal_badge-module__iconSm___mAfVw" src="/assets/configurator/icons/styleguide/metals/bronze.png">
                            <div class="inline-block metal_badge-module__metalLabel___ukBfN metal_badge-module__silver___Jq0_e">SILVER</div>
                        </div>
                        <span class="layouts-module__ml6___PY2sV layouts-module__flex___vBBZi">
                            <span class="layouts-module__mt4___V2pmP">+</span>
                            <img class="csr_badge-module__badge___Qg6LR" src="/assets/configurator/icons/csr_icon_2x.png" alt="csr-badge">
                        </span>
                    </div>
                    <!-- <div class="plan-type col-sm-9 justify-content-center">
                        <p class="plan-name">{{ plan_name }}</p>
                    </div>
                </div>
                <div class="plan-prices">
                    <div class="price-item">
                        <span class="price-value">{{ premium }}</span>
                        <span class="price-label">Premium</span>
                        <span class="old-price">Was $2028.58</span>
                    </div>
                    <div class="price-item">
                        <span class="price-value">{{ deductible }}</span>
                        <span class="price-label">Deductible</span>
                    </div>
                    <div class="price-item">
                        <span class="price-value">{{ max_des }}</span>
                        <span class="price-label">POO m\xE1x.</span>
                    </div>
                </div>
                <div class="plan-links">
                    <a href="#" class="text-blue-500">Ver detalles completos del plan</a>
                    <a href="#" class="text-blue-500">Ver lista de beneficios</a>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="card plan-status">
                <ul>
                    <li><strong>Estado:</strong> Inscrito</li>
                    <li><strong>Vigente:</strong> 6/1/2024</li>
                    <li><strong>Vencimiento:</strong> 6/30/2024</li>
                    <li><strong>Miembros:</strong> ISAAC TREJO RAMIREZ, DALIA TREJO</li>
                    <li><strong>ID de subscritor:</strong> 0018475352</li>
                    <li><strong>ID de FFM:</strong> 5280429770</li>
                    <li><strong>Tel\xE9fono de pago:</strong> (877) 687-1169</li>
                    <li><strong>Agente registrado:</strong> beatriz sierra (NPN: 8602276)</li>
                </ul>
            </div>
        </div>
    </div> -->
</div>`;

  // frappe-html:/workspace/development/frappe-bench/apps/mabecenter/mabecenter/templates/jinja.html
  frappe.templates["jinja"] = `{% set topics = frappe.get_all("Discussion Topic",
{"reference_doctype": doctype, "reference_docname": docname}, ["name", "title", "owner", "creation"]) %}


<div class="discussions-parent {% if single_thread %} is-single-thread {% endif %}"
	data-doctype="{{ doctype | urlencode }}" data-docname="{{ docname | urlencode }}">

	{% if not single_thread %}
	{% include "frappe/templates/discussions/topic_modal.html" %}
	{% endif %}

	<div class="discussions-header">
		<span class="discussions-section-title">{{ _(title) }}</span>
		{% if topics | length and not single_thread %}
		{% include "frappe/templates/discussions/search.html" %}
		{% endif %}

		{% if topics and not single_thread %}
		{% include "frappe/templates/discussions/button.html" %}
		{% endif %}
	</div>

	<div class="">
		{% if topics and not single_thread %}

		<div class="discussions-sidebar">

			{% for topic in topics %}
			{% set replies = frappe.get_all("Discussion Reply", {"topic": topic.name})%}
			{% include "frappe/templates/discussions/sidebar.html" %}

			{% if loop.index != topics | length %}
			<div class="card-divider"></div>
			{% endif %}

			{% endfor %}
		</div>

		<div class="hide" id="discussion-group">
			{% for topic in topics %}
			{% include "frappe/templates/discussions/reply_section.html" %}
			{% endfor %}
		</div>

		{% elif single_thread %}
		{% set topic = topics[0] if topics | length else None %}
		{% include "frappe/templates/discussions/reply_section.html" %}

		{% else %}
		<div class="empty-state">
			<div>
			  <img class="icon icon-xl" src="/assets/frappe/icons/timeless/message.svg">
			</div>
			<div class="empty-state-text">
			  <div class="empty-state-heading">{{ empty_state_title }}</div>
			  <div class="course-meta">{{ empty_state_subtitle }}</div>
			</div>
			<div>
				{% if frappe.session.user == "Guest" %}
				<div class="btn btn-default btn-md login-from-discussion"> {{ _("Login") }} </div>
				{% elif condition is defined and not condition %}
				<div class="btn btn-default btn-md login-from-discussion" data-redirect="{{ redirect_to }}">
					{{ button_name }}
				</div>
				{% else %}
				{% include "frappe/templates/discussions/button.html" %}
				{% endif %}
			</div>
		</div>
		{% endif %}
	</div>
</div`;
})();
//# sourceMappingURL=mabecenter.bundle.U3FRNP2X.js.map
