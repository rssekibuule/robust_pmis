/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class KpiLinkageDashboard extends Component {}

KpiLinkageDashboard.template = "robust_pmis.kpi_linkage_dashboard_client";

registry.category("actions").add("kpi_linkage_dashboard", KpiLinkageDashboard);

export default KpiLinkageDashboard;
