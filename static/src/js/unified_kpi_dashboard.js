/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useSubEnv, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class UnifiedKPIDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = useState({
            strategicKPIs: [],
            programmeKPIs: [],
            totalCount: 0,
            strategicCount: 0,
            programmeCount: 0,
            loading: true,
            avgPerformance: 0,
        });

        this.loadKPIData();
    }

    async loadKPIData() {
        try {
            // Load strategic KPIs
            const strategicKPIs = await this.orm.searchRead(
                "key.performance.indicator",
                [["active", "=", true]],
                ["name", "achievement_percentage", "status", "kra_id", "directorate_id", "classification_level", "parent_type"]
            );

            // Load programme KPIs
            const programmeKPIs = await this.orm.searchRead(
                "performance.indicator",
                [["active", "=", true]],
                ["name", "achievement_percentage", "status", "parent_programme_id", "outcome_id", "results_chain_level"]
            );

            // Calculate statistics
            const allPerformances = [
                ...strategicKPIs.map(kpi => kpi.achievement_percentage || 0),
                ...programmeKPIs.map(kpi => kpi.achievement_percentage || 0)
            ];

            const avgPerformance = allPerformances.length > 0 
                ? allPerformances.reduce((sum, perf) => sum + perf, 0) / allPerformances.length 
                : 0;

            this.state.strategicKPIs = strategicKPIs;
            this.state.programmeKPIs = programmeKPIs;
            this.state.strategicCount = strategicKPIs.length;
            this.state.programmeCount = programmeKPIs.length;
            this.state.totalCount = strategicKPIs.length + programmeKPIs.length;
            this.state.avgPerformance = avgPerformance;
            this.state.loading = false;
        } catch (error) {
            console.error("Error loading KPI data:", error);
            this.state.loading = false;
        }
    }

    async openStrategicKPIs() {
        await this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Strategic KPIs',
            res_model: 'key.performance.indicator',
            view_mode: 'list,form',
            domain: [['active', '=', true]],
            context: {},
        });
    }

    async openProgrammeKPIs() {
        await this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Programme KPIs',
            res_model: 'performance.indicator',
            view_mode: 'list,form',
            domain: [['active', '=', true]],
            context: {},
        });
    }

    async openAllKPIs() {
        // Open a unified view or action
        await this.action.doAction({
            type: 'ir.actions.client',
            tag: 'unified_kpi_list',
        });
    }

    getStatusColor(status) {
        const colors = {
            'achieved': 'success',
            'on_track': 'info',
            'at_risk': 'warning',
            'behind': 'danger',
            'not_started': 'secondary'
        };
        return colors[status] || 'secondary';
    }

    getStatusText(status) {
        const texts = {
            'achieved': 'Achieved',
            'on_track': 'On Track',
            'at_risk': 'At Risk',
            'behind': 'Behind',
            'not_started': 'Not Started'
        };
        return texts[status] || 'Unknown';
    }
}

UnifiedKPIDashboard.template = "robust_pmis.UnifiedKPIDashboard";

registry.category("actions").add("unified_kpi_dashboard", UnifiedKPIDashboard);
