odoo.define('robust_pmis.interactive_dashboard', function(require) {
    "use strict";
    
    var FormRenderer = require('web.FormRenderer');
    var rpc = require('web.rpc');
    var core = require('web.core');
    
    FormRenderer.include({
        _postRender: function() {
            this._super.apply(this, arguments);
            // Only run on performance.dashboard form
            if (this.state.model === 'performance.dashboard') {
                setTimeout(this._initInteractiveDashboard.bind(this), 500);
            }
        },
        
        _initInteractiveDashboard: function() {
            this._setupEventListeners();
            this._initCharts();
            this._loadDashboardData();
        },
        
        _setupEventListeners: function() {
            // No header refresh button anymore; keep placeholder for future hooks
        },
        
        _initCharts: function() {
            // Ensure Chart.js is available
            if (typeof Chart === 'undefined') {
                console.error('Chart.js is not loaded');
                return;
            }
            
            // Configure Chart.js defaults for better visuals
            if (Chart.defaults) {
                Chart.defaults.color = '#4A5568';
                Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
                Chart.defaults.animation.duration = 1000;
                Chart.defaults.responsive = true;
                Chart.defaults.maintainAspectRatio = false;
            }
            
            // Clear any existing charts
            this._destroyExistingCharts();
            
            // Initialize empty charts that will be populated with data
            this._initEmptyCharts();
        },
        
        _refreshDashboard: function() {
            // Simple refresh without header button UI state
            return this._loadDashboardData();
        },
        
        _loadDashboardData: function() {
            var self = this;
            
            // Get real-time metrics first
            return rpc.query({
                model: 'performance.dashboard',
                method: 'get_realtime_metrics',
                args: [self.state.res_id],
            }).then(function(metrics) {
                self._updateMetricsDisplay(metrics);
                
                // Then get chart data
                return rpc.query({
                    model: 'performance.dashboard', 
                    method: 'get_dashboard_data',
                    args: [self.state.res_id],
                });
            }).then(function(chartData) {
                self._updateChartsWithData(chartData);
                self._updateTopPerformersList(chartData.top_kpis);
            });
        },
        
        _updateMetricsDisplay: function(metrics) {
            // Update metric cards with real-time data
            var self = this;
            var metricFields = {
                'total_strategic_goals': metrics.total_strategic_goals,
                'total_kras': metrics.total_kras,
                'total_kpis': metrics.total_kpis,
                'total_programmes': metrics.total_programmes,
                'total_directorates': metrics.total_directorates,
                'total_divisions': metrics.total_divisions,
                'avg_kra_performance': (metrics.avg_kra_performance || 0).toFixed(1),
                'avg_kpi_performance': (metrics.avg_kpi_performance || 0).toFixed(1),
                'avg_programme_performance': (metrics.avg_programme_performance || 0).toFixed(1)
            };
            
            Object.keys(metricFields).forEach(function(fieldName) {
                var field = self.el.querySelector('.o_field_widget[name="' + fieldName + '"]');
                if (field) {
                    if (fieldName.includes('avg_') && field.classList.contains('o_field_progressbar')) {
                        // For progressbar fields, update differently
                        var valueElem = field.querySelector('.o_progressbar_value');
                        if (valueElem) {
                            valueElem.textContent = metricFields[fieldName] + '%';
                        }
                        
                        var barElem = field.querySelector('.progress-bar');
                        if (barElem) {
                            barElem.style.width = metricFields[fieldName] + '%';
                        }
                    } else {
                        // For regular fields
                        field.textContent = metricFields[fieldName];
                    }
                }
            });
        },
        
        _initEmptyCharts: function() {
            var self = this;
            
            // Performance Overview Chart - with custom tooltip
            var overviewCtx = this.el.querySelector('#performanceOverviewChart');
            if (overviewCtx) {
                // Strategic goals sample data with actual goals and targets
                var goalLabels = ['Improved Service Delivery', 'Economic Growth', 'Infrastructure Dev.', 'Social Dev.', 'Governance'];
                var goalPerformance = [75, 68, 82, 91, 63];
                var goalTargets = [90, 80, 95, 100, 85];
                
                this.overviewChart = new Chart(overviewCtx.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: goalLabels,
                        datasets: [
                            {
                                label: 'Current Progress',
                                data: goalPerformance,
                                backgroundColor: [
                                    'rgba(102, 126, 234, 0.8)',
                                    'rgba(17, 153, 142, 0.8)', 
                                    'rgba(252, 182, 159, 0.8)',
                                    'rgba(250, 112, 154, 0.8)',
                                    'rgba(168, 237, 234, 0.8)'
                                ],
                                borderColor: 'rgba(255, 255, 255, 0.5)',
                                borderWidth: 2,
                                borderRadius: 4,
                                order: 2
                            },
                            {
                                label: 'Target',
                                data: goalTargets,
                                backgroundColor: 'rgba(0, 0, 0, 0)',
                                borderColor: 'rgba(0, 0, 0, 0.5)',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                type: 'line',
                                pointRadius: 4,
                                pointBackgroundColor: 'white',
                                pointBorderColor: 'rgba(0, 0, 0, 0.5)',
                                pointBorderWidth: 2,
                                order: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { 
                                display: true,
                                position: 'top',
                                labels: {
                                    padding: 15,
                                    usePointStyle: true,
                                    boxWidth: 10
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                                titleColor: '#2D3748',
                                bodyColor: '#4A5568',
                                titleFont: { weight: 'bold' },
                                bodyFont: { size: 13 },
                                displayColors: true,
                                borderWidth: 1,
                                borderColor: '#E2E8F0',
                                callbacks: {
                                    label: function(context) {
                                        if (context.dataset.label === 'Current Progress') {
                                            return 'Progress: ' + context.parsed.y.toFixed(1) + '%';
                                        } else {
                                            return 'Target: ' + context.parsed.y.toFixed(1) + '%';
                                        }
                                    },
                                    afterLabel: function(context) {
                                        if (context.dataset.label === 'Current Progress') {
                                            var datasetIndex = context.datasetIndex;
                                            var dataIndex = context.dataIndex;
                                            var target = context.chart.data.datasets[1].data[dataIndex];
                                            var current = context.parsed.y;
                                            var percentage = ((current / target) * 100).toFixed(1);
                                            return 'Achievement: ' + percentage + '% of target';
                                        }
                                        return '';
                                    }
                                }
                            }
                        },
                        scales: {
                            y: { 
                                beginAtZero: true, 
                                max: 100,
                                grid: { color: 'rgba(226, 232, 240, 0.5)' },
                                ticks: { 
                                    font: { size: 12 },
                                    callback: function(value) {
                                        return value + '%';
                                    }
                                },
                                title: {
                                    display: true,
                                    text: 'Performance (%)',
                                    font: {
                                        size: 14,
                                        weight: 'bold'
                                    }
                                }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { 
                                    font: { size: 12 },
                                    maxRotation: 45,
                                    minRotation: 45
                                }
                            }
                        },
                        animation: {
                            duration: 1000
                        }
                    }
                });
            }
            
            // Trends Chart
            var trendsCtx = this.el.querySelector('#trendsChart');
            if (trendsCtx) {
                this.trendsChart = new Chart(trendsCtx.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: ['Loading...'],
                        datasets: [{
                            label: 'Performance Trend',
                            data: [0],
                            borderColor: 'rgba(102, 126, 234, 1)',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointHoverRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            tooltip: {
                                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                                titleColor: '#2D3748',
                                bodyColor: '#4A5568',
                                titleFont: { weight: 'bold' },
                                bodyFont: { size: 13 },
                                borderWidth: 1,
                                borderColor: '#E2E8F0'
                            }
                        },
                        scales: {
                            y: { 
                                beginAtZero: true, 
                                max: 100,
                                grid: { color: 'rgba(226, 232, 240, 0.5)' }
                            },
                            x: {
                                grid: { display: false }
                            }
                        }
                    }
                });
            }
            
            // Distribution Chart - with custom tooltip
            var distributionCtx = this.el.querySelector('#distributionChart');
            if (distributionCtx) {
                this.distributionChart = new Chart(distributionCtx.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Loading...'],
                        datasets: [{
                            data: [100],
                            backgroundColor: ['rgba(102, 126, 234, 0.8)'],
                            borderWidth: 2,
                            borderColor: 'white'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '70%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 15,
                                    usePointStyle: true,
                                    pointStyle: 'circle'
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                                titleColor: '#2D3748',
                                bodyColor: '#4A5568',
                                titleFont: { weight: 'bold' },
                                bodyFont: { size: 13 },
                                displayColors: true,
                                borderWidth: 1,
                                borderColor: '#E2E8F0',
                                callbacks: {
                                    label: function(context) {
                                        return context.label + ': ' + context.parsed + ' KPIs';
                                    }
                                }
                            }
                        },
                        animation: {
                            animateRotate: true,
                            animateScale: true
                        }
                    }
                });
            }
        },
        
        _updateChartsWithData: function(data) {
            // Update Performance Overview Chart
            if (this.overviewChart) {
                if (data.goals_performance && data.goals_performance.length > 0) {
                    const sortedGoals = [...data.goals_performance].sort((a, b) => b.performance - a.performance);
                    
                    // Update labels and current performance data
                    this.overviewChart.data.labels = sortedGoals.map(g => this._truncateText(g.name, 20));
                    this.overviewChart.data.datasets[0].data = sortedGoals.map(g => g.performance);
                    
                    // Set target values (assuming 100% or using target from data if available)
                    const targetValues = sortedGoals.map(g => g.target || 100);
                    this.overviewChart.data.datasets[1].data = targetValues;
                    
                    // Update colors for the bars
                    this.overviewChart.data.datasets[0].backgroundColor = sortedGoals.map((g, i) => {
                        const colors = [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(17, 153, 142, 0.8)', 
                            'rgba(252, 182, 159, 0.8)',
                            'rgba(250, 112, 154, 0.8)',
                            'rgba(168, 237, 234, 0.8)'
                        ];
                        return colors[i % colors.length];
                    });
                    
                    this.overviewChart.update();
                } else {
                    // Keep the default sample data if no real data is available
                    console.log("No goals performance data available, using sample data");
                }
            }
            
            // Update Trends Chart with KRA performance
            if (this.trendsChart && data.kras_performance) {
                const sortedKras = [...data.kras_performance].sort((a, b) => b.performance - a.performance).slice(0, 6);
                this.trendsChart.data.labels = sortedKras.map(k => this._truncateText(k.name, 15));
                this.trendsChart.data.datasets[0].data = sortedKras.map(k => k.performance);
                this.trendsChart.update();
            }
            
            // Update Distribution Chart
            if (this.distributionChart && data.distribution) {
                this.distributionChart.data.labels = ['Excellent (90%+)', 'Good (70-89%)', 'Fair (50-69%)', 'Poor (<50%)'];
                this.distributionChart.data.datasets[0].data = [
                    data.distribution.excellent || 0,
                    data.distribution.good || 0,
                    data.distribution.fair || 0,
                    data.distribution.poor || 0
                ];
                this.distributionChart.data.datasets[0].backgroundColor = [
                    'rgba(17, 153, 142, 0.8)',
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(252, 182, 159, 0.8)',
                    'rgba(250, 112, 154, 0.8)'
                ];
                this.distributionChart.update();
            }
        },
        
        _updateTopPerformersList: function(topKpis) {
            // Find the top performers list container
            var listContainer = this.el.querySelector('#topPerformersList');
            if (!listContainer || !topKpis || !topKpis.length) return;
            
            // Clear the container
            listContainer.innerHTML = '';
            
            // Add the top performers
            topKpis.slice(0, 5).forEach(function(kpi, index) {
                var performerItem = document.createElement('div');
                performerItem.className = 'performer-item';
                
                // Get color based on performance
                var performanceColor = '#10B981'; // Default good color
                if (kpi.performance < 50) {
                    performanceColor = '#EF4444'; // Red for poor
                } else if (kpi.performance < 70) {
                    performanceColor = '#F59E0B'; // Yellow/amber for fair
                } else if (kpi.performance >= 90) {
                    performanceColor = '#059669'; // Dark green for excellent
                }
                
                performerItem.innerHTML = `
                    <div class="performer-rank">${index + 1}</div>
                    <div class="performer-info">
                        <div class="performer-name">${this._truncateText(kpi.name, 30)}</div>
                        <div class="performer-category">${kpi.kra || 'No KRA'}</div>
                    </div>
                    <div class="performer-progress" style="color: ${performanceColor}">
                        ${kpi.performance.toFixed(1)}%
                    </div>
                `;
                
                listContainer.appendChild(performerItem);
            }, this);
            
            // Add "View All" link if there are more than 5
            if (topKpis.length > 5) {
                var viewAllLink = document.createElement('div');
                viewAllLink.className = 'view-all-link';
                viewAllLink.innerHTML = '<a href="/web#action=robust_pmis.action_key_performance_indicator">View all KPIs</a>';
                listContainer.appendChild(viewAllLink);
            }
        },
        
    // Removed timestamp update; banner is gone
        
        _truncateText: function(text, maxLength) {
            if (!text) return '';
            return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
        },
        
        _destroyExistingCharts: function() {
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
    });
});
