/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted, onWillUnmount } from "@odoo/owl";


export class PerformanceDashboardController extends FormController {
    setup() {
        super.setup();
        this.orm = useService("orm");

        // Make action service optional to avoid errors
        try {
            this.action = useService("action");
        } catch (error) {
            console.log('Action service not available:', error.message);
            this.action = null;
        }

        onMounted(() => {
            if (this.props.resModel === 'performance.dashboard') {
                // Ensure we initialize only once per mount to avoid unstable re-renders
                if (!this._initialized) {
                    this._initialized = true;
                    console.log('Performance Dashboard mounted successfully');
                    this.initializeDashboard();
                }
            }
        });

        onWillUnmount(() => {
            this.destroyCharts();
            this._initialized = false;
        });
    }

    async initializeDashboard() {
        console.log('Initializing performance dashboard...');

        // Wait for DOM to be ready and attach resize observer for stable charts
        setTimeout(() => {
            this.loadDashboardData();
            this.enhanceVisuals();
            this.populateEntityOptions('organization');
            this._attachResizeHandlers();
        }, 500);
    }

    async loadDashboardData(filters = null) {
        try {
            let data = null;
            // Try JSON endpoint first; if it fails, fall back to ORM
            if (window.odoo && window.odoo.http) {
                try {
                    const response = await window.odoo.http.post('/performance/dashboard/data', { filters });
                    data = response.result || response;
                } catch (e) {
                    // JSON route may not exist; proceed to ORM fallback
                }
            }
            if (!data) {
                const dashboardId = this.model?.root?.resId || 1;
                const method = filters ? 'get_filtered_dashboard_data' : 'get_dashboard_data';
                const args = filters ? [dashboardId, filters] : [dashboardId];
                data = await this.orm.call('performance.dashboard', method, args);
            }

            this.updateDashboardMetrics(data);
            this.renderCharts(data);
            this.updateTimestamp();
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            // Fallback to basic chart rendering
            this.renderBasicCharts();
        }
    }

    updateDashboardMetrics(data) {
        if (data.summary && data.summary.avg_performance !== undefined) {
            const performance = data.summary.avg_performance;
            const performanceClass = this.getPerformanceClass(performance);

            // Animate performance bar
            setTimeout(() => {
                const fillEl = document.querySelector('.performance-fill');
                const textEl = document.querySelector('.performance-text');

                if (fillEl) {
                    fillEl.style.width = performance + '%';
                    fillEl.classList.add(performanceClass);
                }
                if (textEl) {
                    textEl.textContent = performance.toFixed(1) + '%';
                }
            }, 500);
        }
    }

    getPerformanceClass(performance) {
        if (performance >= 90) return 'excellent';
        if (performance >= 70) return 'good';
        if (performance >= 50) return 'fair';
        return 'poor';
    }

    renderCharts(data) {
        this.ensureChartJS(() => {
            this.renderExecutiveGauges(data);
            this.renderOverviewChart(data);
            this.renderTrendsChart(data);
            this.renderDistributionChart(data);
            this.renderDirectorateContributionChart(data);
            this.renderDivisionContributionChart(data);
            this.renderTopKPIs(data);
        });
    }

    renderBasicCharts() {
        // Fallback basic charts with placeholder data
        const basicData = {
            summary: {
                total_strategic_goals: 5,
                total_kras: 37,
                total_kpis: 108,
                total_programmes: 19,
                total_directorates: 19,
                total_divisions: 10,
                avg_performance: 75
            },
            distribution: {
                excellent: 40,
                good: 35,
                fair: 20,
                poor: 5
            },
            top_kpis: []
        };

        this.renderCharts(basicData);
    }

    ensureChartJS(callback) {
        if (window.Chart) {
            callback();
            return;
        }
        // Avoid infinite retries causing console spam
        this._chartRetryCount = (this._chartRetryCount || 0) + 1;
        if (this._chartRetryCount > 20) {
            console.error('Chart.js failed to load after multiple attempts. Rendering fallback charts.');
            try { callback(); } catch (e) { /* ignore */ }
            return;
        }
        setTimeout(() => this.ensureChartJS(callback), 250);
    }

    renderOverviewChart(data) {
        const ctx = document.getElementById('performanceOverviewChart');
        if (!ctx || !window.Chart) return;

        if (this.overviewChart) {
            this.overviewChart.destroy();
        }

        // Horizontal bar: one bar per Strategic Goal, showing performance % vs target line
        const goals = data.goals_performance || [];
        const labels = goals.map(g => g.name);
        const perf = goals.map(g => Math.round(g.performance || 0));
        const target = goals.map(g => Math.round((g.target || 100)));

        this.overviewChart = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Achievement %',
                        data: perf,
                        backgroundColor: 'rgba(102, 126, 234, 0.85)',
                        borderRadius: 6,
                        barThickness: 18,
                    },
                    {
                        label: 'Target %',
                        data: target,
                        type: 'line',
                        borderColor: 'rgba(17, 153, 142, 1)',
                        borderDash: [6, 4],
                        pointRadius: 0,
                        tension: 0,
                        fill: false
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                resizeDelay: 200,
                animation: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.x}%` } }
                },
                scales: {
                    x: { beginAtZero: true, max: 160, grid: { color: 'rgba(0,0,0,0.05)' } },
                    y: { grid: { display: false } }
                }
            }
        });
    }

    renderTrendsChart(data) {
        const ctx = document.getElementById('trendsChart');
        if (!ctx || !window.Chart) return;

        if (this.trendsChart) {
            this.trendsChart.destroy();
        }

        const avg = (data.summary && data.summary.avg_performance) || 75;
        const series = [avg - 10, avg - 6, avg - 4, avg - 2, avg - 1, avg].map(v =>
            Math.max(0, Math.min(100, v))
        );

        this.trendsChart = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [
                    {
                        label: 'Overall Performance',
                        data: series,
                        borderColor: 'rgba(102, 126, 234, 1)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Target',
                        data: [70, 75, 80, 85, 88, 90],
                        borderColor: 'rgba(17, 153, 142, 1)',
                        fill: false,
                        borderDash: [5, 5],
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                resizeDelay: 200,
                animation: false
            }
        });
    }

    renderDistributionChart(data) {
        const ctx = document.getElementById('distributionChart');
        if (!ctx || !window.Chart) return;

        if (this.distributionChart) {
            this.distributionChart.destroy();
        }

        const distribution = data.distribution || { excellent: 40, good: 35, fair: 20, poor: 5 };

        this.distributionChart = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Excellent', 'Good', 'Fair', 'Poor'],
                datasets: [{
                    data: [distribution.excellent, distribution.good, distribution.fair, distribution.poor],
                    backgroundColor: ['#11998e', '#667eea', '#fcb69f', '#fa709a']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                resizeDelay: 200,
                animation: false
            }
        });
    }

    renderDirectorateContributionChart(data) {
        const canvas = document.getElementById('directorateContribChart');
        if (!canvas || !window.Chart) return;
        this.dirChart && this.dirChart.destroy();
        const rows = (data.directorate_contributions || []).slice(0, 10);
        const labels = rows.map(r => r.name);
        const kpi = rows.map(r => r.kpi_achievement || 0);
        const prog = rows.map(r => r.programme_progress || 0);
        this.dirChart = new Chart(canvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    { label: 'KPI Achievement %', data: kpi, backgroundColor: 'rgba(37, 117, 252, 0.8)' },
                    { label: 'Programme Progress %', data: prog, backgroundColor: 'rgba(54, 211, 153, 0.8)' },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                plugins: { legend: { position: 'top' } },
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    }

    renderDivisionContributionChart(data) {
        const canvas = document.getElementById('divisionContribChart');
        if (!canvas || !window.Chart) return;
        this.divChart && this.divChart.destroy();
        const rows = (data.division_contributions || []).slice(0, 10);
        const labels = rows.map(r => r.name);
        const prog = rows.map(r => r.programme_progress || 0);
        const ind = rows.map(r => r.indicator_achievement || 0);
        this.divChart = new Chart(canvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    { label: 'Programme Progress %', data: prog, backgroundColor: 'rgba(246, 173, 85, 0.9)' },
                    { label: 'Indicators Achievement %', data: ind, backgroundColor: 'rgba(128, 90, 213, 0.9)' },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                plugins: { legend: { position: 'top' } },
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    }

    renderTopKPIs(data) {
        const list = document.getElementById('topPerformersList');
        if (!list) return;

        const items = (data.top_kpis || []).slice(0, 6).map(kpi =>
            `<div class="top-kpi-item">
                <span class="kpi-name">${kpi.name}</span>
                <span class="kpi-score">${(kpi.performance || 0).toFixed(1)}%</span>
            </div>`
        ).join('');

        list.innerHTML = items || '<div class="text-muted">No KPI data available.</div>';
    }

    renderExecutiveGauges(data) {
        const cfg = (value, colors) => ({
            type: 'doughnut',
            data: {
                labels: ['Value', 'Remainder'],
                datasets: [{
                    data: [Math.max(0, Math.min(100, value)), 100 - Math.max(0, Math.min(100, value))],
                    backgroundColor: colors,
                    borderWidth: 0,
                    circumference: 180,
                    rotation: 270,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } },
                animation: { duration: 400 }
            },
            plugins: [{
                id: 'centerText',
                beforeDraw(chart) {
                    const { ctx, chartArea } = chart;
                    const val = chart.config.data.datasets[0].data[0];
                    ctx.save();
                    ctx.font = '700 20px Segoe UI, sans-serif';
                    ctx.fillStyle = '#1a202c';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText((typeof val === 'number' ? Math.round(val) : val) + '%', (chartArea.left + chartArea.right) / 2, (chartArea.top + chartArea.bottom) / 1.25);
                    ctx.restore();
                }
            }]
        });

        const summary = data.summary || {};
        const overall = summary.avg_performance ?? 0;
        const kra = summary.avg_kra_performance ?? 0;
        const programme = summary.avg_programme_performance ?? 0;
        const portfolio = (() => {
            const dist = data.distribution || { excellent: 0, good: 0, fair: 0, poor: 0 };
            const total = (dist.excellent || 0) + (dist.good || 0) + (dist.fair || 0) + (dist.poor || 0);
            if (!total) return 0;
            return Math.round(((dist.excellent + dist.good) / total) * 100);
        })();

        const ensureCanvas = (id) => document.getElementById(id)?.getContext('2d');
        const overCtx = ensureCanvas('gaugeOverall');
        const kraCtx = ensureCanvas('gaugeKRA');
        const progCtx = ensureCanvas('gaugeProgramme');
        const portCtx = ensureCanvas('gaugePortfolio');
        // Harmonize gauge palette with purple theme for better aesthetics
        if (overCtx) { this._gaugeOverall?.destroy?.(); this._gaugeOverall = new Chart(overCtx, cfg(overall, ['#5b7cfa', '#e9edf5'])); }
        if (kraCtx) { this._gaugeKRA?.destroy?.(); this._gaugeKRA = new Chart(kraCtx, cfg(kra, ['#36d399', '#e9edf5'])); }
        if (progCtx) { this._gaugeProgramme?.destroy?.(); this._gaugeProgramme = new Chart(progCtx, cfg(programme, ['#f6ad55', '#e9edf5'])); }
        if (portCtx) { this._gaugePortfolio?.destroy?.(); this._gaugePortfolio = new Chart(portCtx, cfg(portfolio, ['#6b3fa0', '#e9edf5'])); }
    }

    enhanceVisuals() {
        // Apply filters
        const applyBtn = document.getElementById('apply-filters');
        if (applyBtn) {
            applyBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const filters = this.collectFilters();
                this.loadDashboardData(filters);
            });
        }

        // React to scope changes to populate entity options
        const scopeEl = document.getElementById('filter-scope');
        if (scopeEl) {
            scopeEl.addEventListener('change', (e) => {
                const scope = e.target.value || 'organization';
                this.populateEntityOptions(scope);
            });
        }

        // Refresh button
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.updateTimestamp();
                this.loadDashboardData();
            });
        }

        // Card click handlers with real navigation
        document.querySelectorAll('.metric-card, .quick-link').forEach(card => {
            card.addEventListener('click', async (e) => {
                const xmlid = e.currentTarget.dataset.actionXmlid;
                if (!xmlid) return;
                if (this.action && this.action.doAction) {
                    try {
                        await this.action.doAction(xmlid);
                        return;
                    } catch (err) {
                        console.warn('doAction failed, falling back to hash navigation', err);
                    }
                }
                window.open('/web#action=' + xmlid, '_self');
            });
            // Basic keyboard accessibility
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
        });
    }

    async populateEntityOptions(scope) {
        try {
            const entityEl = document.getElementById('filter-entity');
            if (!entityEl) return;

            // Determine model based on scope
            let model = null;
            let labelAll = 'All';
            if (scope === 'strategic_goal') { model = 'strategic.goal'; labelAll = 'All Goals'; }
            else if (scope === 'strategic_objective') { model = 'strategic.objective'; labelAll = 'All Objectives'; }
            else if (scope === 'programme') { model = 'kcca.programme'; labelAll = 'All Programmes'; }
            else if (scope === 'directorate') { model = 'kcca.directorate'; labelAll = 'All Directorates'; }
            else if (scope === 'division') { model = 'kcca.division'; labelAll = 'All Divisions'; }
            else { entityEl.innerHTML = '<option value="all">All</option>'; return; }

            const records = await this.orm.searchRead(model, [['active', '=', true]], ['name']);
            const options = [`<option value="all">${labelAll}</option>`]
                .concat(records.map(r => `<option value="${r.id}">${r.name}</option>`));
            entityEl.innerHTML = options.join('');
        } catch (error) {
            console.error('Error populating entities:', error);
        }
    }

    collectFilters() {
        const dataTypeEl = document.getElementById('filter-data-type');
        const scopeEl = document.getElementById('filter-scope');
        const entityEl = document.getElementById('filter-entity');
        const performanceEl = document.getElementById('filter-performance');
        const periodEl = document.getElementById('filter-period');
        return {
            data_type: dataTypeEl?.value || 'all',
            scope: scopeEl?.value || 'organization',
            entity: entityEl?.value || 'all',
            performance: performanceEl?.value || 'all',
            period: periodEl?.value || 'fy'
        };
    }

    updateTimestamp() {
        const span = document.querySelector('#dashboard-timestamp span');
        if (span) {
            const now = new Date();
            span.textContent = now.toLocaleString();
        }
    }

    _attachResizeHandlers() {
        // Debounced window resize to reduce thrashing during scroll/resize
        if (this._resizeHandler) return;
        let rafId = null;
        const onResize = () => {
            if (rafId) cancelAnimationFrame(rafId);
            rafId = requestAnimationFrame(() => {
                if (!this._initialized) return;
                try {
                    // Recalculate chart sizes without recreating data
                    [this.overviewChart, this.trendsChart, this.distributionChart].forEach(ch => ch && ch.resize());
                } catch (e) {
                    // As a last resort, re-render
                    this.loadDashboardData();
                }
            });
        };
        this._resizeHandler = onResize;
        window.addEventListener('resize', this._resizeHandler, { passive: true });
    }

    destroyCharts() {
        if (this._resizeHandler) {
            window.removeEventListener('resize', this._resizeHandler);
            this._resizeHandler = null;
        }
        if (this.overviewChart) {
            this.overviewChart.destroy();
            this.overviewChart = null;
        }
        if (this.trendsChart) {
            this.trendsChart.destroy();
            this.trendsChart = null;
        }
        if (this.distributionChart) {
            this.distributionChart.destroy();
            this.distributionChart = null;
        }
    }
}

export const PerformanceDashboardFormView = {
    ...formView,
    Controller: PerformanceDashboardController,
};

registry.category("views").add("performance_dashboard_form", PerformanceDashboardFormView);
