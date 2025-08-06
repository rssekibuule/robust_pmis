odoo.define('robust_pmis.performance_dashboard', function(require) {
    "use strict";
    var FormRenderer = require('web.FormRenderer');
    var Chart = require('chart.js');

    FormRenderer.include({
        _postRender: function() {
            this._super.apply(this, arguments);
            // Only run on performance.dashboard form
            if (this.state.model === 'performance.dashboard') {
                // Delay to ensure DOM is ready
                setTimeout(this._initCharts.bind(this), 100);
            }
        },
        _initCharts: function() {
            var labels = ['KPI', 'Programme', 'Directorate', 'Division'];
            var getValue = function(field) {
                var el = document.querySelector('.o_field_widget[name="' + field + '"]');
                return el ? parseFloat(el.textContent) || 0 : 0;
            };
            var values = [
                getValue('avg_kpi_performance'),
                getValue('avg_programme_performance'),
                getValue('avg_directorate_performance'),
                getValue('avg_division_performance')
            ];
            // Bar
            var barCtx = this.el.querySelector('#performance_overview_chart');
            if (barCtx) {
                new Chart(barCtx.getContext('2d'), {
                    type: 'bar', data: { labels: labels, datasets: [{ label: 'Avg (%)', data: values,
                        backgroundColor: ['#667eea', '#764ba2', '#4facfe', '#00f2fe'],
                        borderColor: ['#4a57a3', '#5a3170', '#3a6fd6', '#0098c7'], borderWidth: 2 }] },
                    options: { scales: { y: { beginAtZero: true, max: 100 } }, plugins: { legend: { position: 'bottom' } } }
                });
            }
            // Pie
            var pieCtx = this.el.querySelector('#performance_distribution_pie');
            if (pieCtx) {
                new Chart(pieCtx.getContext('2d'), {
                    type: 'pie', data: { labels: labels, datasets: [{ data: values,
                        backgroundColor: ['#667eea', '#764ba2', '#4facfe', '#00f2fe'], hoverOffset: 4 }] },
                    options: { plugins: { legend: { position: 'right' } } }
                });
            }
            // Line
            var lineCtx = this.el.querySelector('#performance_line_chart');
            if (lineCtx) {
                new Chart(lineCtx.getContext('2d'), {
                    type: 'line', data: { labels: labels, datasets: [{ data: values,
                        borderColor: '#764ba2', backgroundColor: 'rgba(118,75,162,0.2)', fill: true, tension: 0.4 }] },
                    options: { scales: { y: { beginAtZero: true, max: 100 } }, plugins: { legend: { display: false } } }
                });
            }
        },
    });
});
