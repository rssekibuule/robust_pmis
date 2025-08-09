odoo.define('robust_pmis.dashboard', function (require) {
    'use strict';

    var FormView = require('web.FormView');
    var FormController = require('web.FormController');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');

    var DashboardController = FormController.extend({
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                if (self.modelName === 'performance.dashboard') {
                    self._populateDirectorates();
                    self._loadDashboardData();
                    self._enhanceVisuals();
                }
            });
        },

        _loadDashboardData: function () {
            var self = this;

            var filters = self._collectFilters();

            // Load dashboard data via RPC with filters
            rpc.query({
                route: '/performance/dashboard/data',
                params: { filters: filters }
            }).then(function (data) {
                self._updateDashboardMetrics(data);
                self._renderCharts(data);
            }).catch(function (error) {
                console.error('Error loading dashboard data:', error);
            });
        },

        _updateDashboardMetrics: function (data) {
            // Update performance bars with animations
            var self = this;

            if (data.summary && data.summary.avg_performance !== undefined) {
                var performance = data.summary.avg_performance;
                var performanceClass = self._getPerformanceClass(performance);

                // Animate performance bar
                setTimeout(function () {
                    $('.performance-fill').css('width', performance + '%')
                                         .addClass(performanceClass);
                    $('.performance-text').text(performance.toFixed(1) + '%');
                }, 500);
            }
        },

        _getPerformanceClass: function (performance) {
            if (performance >= 90) return 'excellent';
            if (performance >= 70) return 'good';
            if (performance >= 50) return 'fair';
            return 'poor';
        },

        _renderCharts: function (data) {
            var self = this;
            // Render three charts using Chart.js with real data
            function ensureChartJS(cb){
                if (window.Chart) return cb();
                console.warn('Chart.js not loaded yet');
                setTimeout(cb, 300);
            }
            ensureChartJS(function(){
                self._renderOverviewChart(data);
                self._renderTrendsChart(data);
                self._renderDistributionChart(data);
                self._renderTopKPIs(data);
            });
        },

        _renderOverviewChart: function(data){
            var ctx = document.getElementById('performanceOverviewChart');
            if (!ctx || !window.Chart) return;
            if (this._overviewInstance) { this._overviewInstance.destroy(); }
            var s = data.summary || {};
            this._overviewInstance = new Chart(ctx.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['Strategic Goals','KRAs','KPIs','Programmes','Directorates','Divisions'],
                    datasets: [{
                        label: 'Count',
                        data: [s.total_strategic_goals||s.total_goals||0, s.total_kras||0, s.total_kpis||0, s.total_programmes||0, s.total_directorates||0, s.total_divisions||0],
                        backgroundColor: 'rgba(102,126,234,0.8)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio:false, plugins:{legend:{display:false}} }
            });
        },

        _renderTrendsChart: function(data){
            var ctx = document.getElementById('trendsChart');
            if (!ctx || !window.Chart) return;
            if (this._trendsInstance) { this._trendsInstance.destroy(); }
            // Placeholder trend derived from averages
            var avg = (data.summary && data.summary.avg_performance) || 0;
            var series = [avg-10, avg-6, avg-4, avg-2, avg-1, avg].map(v=>Math.max(0, Math.min(100, v)));
            this._trendsInstance = new Chart(ctx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['Jan','Feb','Mar','Apr','May','Jun'],
                    datasets: [
                        {label:'Overall Performance', data: series, borderColor:'rgba(102,126,234,1)', backgroundColor:'rgba(102,126,234,0.1)', fill:true, tension:0.4},
                        {label:'Target', data:[70,75,80,85,88,90], borderColor:'rgba(17,153,142,1)', fill:false, borderDash:[5,5], tension:0.3}
                    ]
                },
                options: { responsive:true, maintainAspectRatio:false }
            });
        },

        _renderDistributionChart: function(data){
            var ctx = document.getElementById('distributionChart');
            if (!ctx || !window.Chart) return;
            if (this._distInstance) { this._distInstance.destroy(); }
            var d = data.distribution || {excellent:0, good:0, fair:0, poor:0};
            this._distInstance = new Chart(ctx.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['Excellent','Good','Fair','Poor'],
                    datasets: [{
                        data: [d.excellent, d.good, d.fair, d.poor],
                        backgroundColor: ['#11998e','#667eea','#fcb69f','#fa709a']
                    }]
                },
                options: { responsive:true, maintainAspectRatio:false }
            });
        },

        _renderTopKPIs: function(data){
            var list = document.getElementById('topPerformersList');
            if (!list) return;
            var items = (data.top_kpis || []).slice(0,6).map(function(k){
                return `<div class="top-kpi-item"><span class="kpi-name">${k.name}</span><span class="kpi-score">${(k.performance||0).toFixed(1)}%</span></div>`;
            }).join('');
            list.innerHTML = items || '<div class="muted">No KPI data.</div>';
        },

        _enhanceVisuals: function () {
            // Add hover effects and animations to cards
            $(document).on('mouseenter', '.dashboard-card', function () {
                $(this).addClass('shadow-lg');
            }).on('mouseleave', '.dashboard-card', function () {
                $(this).removeClass('shadow-lg');
            });

            var self = this;

            // Apply filters
            $(document).off('click', '#apply-filters').on('click', '#apply-filters', function () {
                self._loadDashboardData();
            });

            // Card drilldowns via action service with context-aware filters
            $(document).off('click', '.metric-card, .quick-link').on('click', '.metric-card, .quick-link', function () {
                var xmlid = $(this).data('action-xmlid');
                if (!xmlid) return;

                var f = self._collectFilters();
                var ctx = { 'search_default_active': 1 };

                function mapPerformanceToKPI(perf){
                    if (perf === 'excellent') return { 'search_default_achieved': 1 };
                    if (perf === 'good') return { 'search_default_on_track': 1 };
                    if (perf === 'fair') return { 'search_default_at_risk': 1 };
                    if (perf === 'poor') return { 'search_default_behind': 1 };
                    return {};
                }

                function mapPerformanceToPIAP(perf){
                    if (perf === 'excellent') return { 'search_default_completed': 1 };
                    if (perf === 'good' || perf === 'fair') return { 'search_default_in_progress': 1 };
                    if (perf === 'poor') return { 'search_default_on_hold': 1 };
                    return {};
                }

                // Add directorate default when provided
                var dirId = (f.directorate && f.directorate !== 'all') ? parseInt(f.directorate, 10) : null;

                if (xmlid === 'robust_pmis.action_key_performance_indicator' || xmlid === 'robust_pmis.action_strategic_kpi_with_programmes'){
                    if (dirId) ctx['search_default_directorate_id'] = dirId;
                    Object.assign(ctx, mapPerformanceToKPI(f.performance));
                    ctx['search_default_group_by_status'] = 1;
                } else if (xmlid === 'robust_pmis.action_programme_objective_indicators'){
                    // Programme-level indicators
                    ctx['search_default_group_by_programme'] = 1;
                    if (dirId) ctx['directorate_id'] = dirId; // consumed by search filter in view
                    Object.assign(ctx, mapPerformanceToKPI(f.performance));
                } else if (xmlid === 'robust_pmis.action_piap_action'){
                    Object.assign(ctx, mapPerformanceToPIAP(f.performance));
                    if (dirId) ctx['directorate_id'] = dirId; // consumed by search filter in view
                    ctx['search_default_group_programme'] = 1; // group by programme if defined in search view
                } else if (xmlid === 'robust_pmis.action_directorate_performance_dashboard'){
                    ctx['search_default_group_by_directorate'] = 1;
                    if (dirId) ctx['search_default_directorate_id'] = dirId;
                } else if (xmlid === 'robust_pmis.action_division_performance_dashboard'){
                    ctx['search_default_group_by_division'] = 1;
                }

                self.do_action(xmlid, { additional_context: ctx });
            });

            // Refresh button in header
            $(document).off('click', '#refresh-dashboard').on('click', '#refresh-dashboard', function(){
                self._loadDashboardData();
            });

            // Animate cards on load
            $('.dashboard-card, .metric-card').each(function (index) {
                var card = $(this);
                setTimeout(function () {
                    card.addClass('animate-in');
                }, index * 100);
            });
        },

        _populateDirectorates: function(){
            // basic population via RPC to read directorates
            rpc.query({
                model: 'kcca.directorate', method: 'search_read', args: [ [['active','=',true]], ['name'] ]
            }).then(function(rows){
                var sel = document.getElementById('filter-directorate');
                if (!sel) return;
                sel.innerHTML = '<option value="all">All Directorates</option>' +
                    rows.map(function(r){ return '<option value="'+r.id+'">'+r.name+'</option>'; }).join('');
            }).catch(function(){ /* ignore */ });
        }
    });

    var DashboardFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DashboardController,
        }),
    });

    // Register the view
    var viewRegistry = require('web.view_registry');
    viewRegistry.add('performance_dashboard_form', DashboardFormView);

    // Helpers
    DashboardController.prototype._collectFilters = function(){
        var directorate = $('#filter-directorate').val() || 'all';
        var performance = $('#filter-performance').val() || 'all';
        var period = $('#filter-period').val() || 'fy';
        return { directorate: directorate, performance: performance, period: period };
    };

    return DashboardFormView;
});

// Additional utility functions for dashboard
odoo.define('robust_pmis.dashboard_utils', function (require) {
    'use strict';

    var utils = {
        formatNumber: function (num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            }
            if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toString();
        },

        getPerformanceColor: function (performance) {
            if (performance >= 90) return '#4caf50';
            if (performance >= 70) return '#2196f3';
            if (performance >= 50) return '#ff9800';
            return '#f44336';
        },

        getPerformanceIcon: function (performance) {
            if (performance >= 90) return 'fa-trophy';
            if (performance >= 70) return 'fa-thumbs-up';
            if (performance >= 50) return 'fa-exclamation-triangle';
            return 'fa-warning';
        }
    };

    return utils;
});
