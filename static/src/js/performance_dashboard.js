odoo.define('robust_pmis.performance_dashboard_charts', function(require) {
    "use strict";
    var FormRenderer = require('web.FormRenderer');

    FormRenderer.include({
        _postRender: function() {
            this._super.apply(this, arguments);
            // Only run on performance.dashboard form and check for chart canvas elements
            if (this.state.model === 'performance.dashboard' && 
                this.el.querySelector('#performanceOverviewChart')) {
                // Delay to ensure DOM is ready and CSS is loaded
                setTimeout(this._initDashboardCharts.bind(this), 1500);
            }
        },
        
        _initDashboardCharts: function() {
            console.log('Initializing charts for performance dashboard...');
            
            // Access Chart.js from the global window object (loaded via CDN)
            var Chart = window.Chart;
            
            // Ensure Chart.js is loaded
            if (typeof Chart === 'undefined') {
                console.error('Chart.js is not loaded from CDN');
                // Retry after a longer delay to allow CDN loading
                setTimeout(this._initDashboardCharts.bind(this), 2000);
                return;
            }
            
            console.log('Chart.js loaded successfully, version:', Chart.version);
            
            // Clear any existing charts first
            this._destroyDashboardCharts();
            
            // Chart configuration
            Chart.defaults.responsive = true;
            Chart.defaults.maintainAspectRatio = false;
            Chart.defaults.plugins.legend.display = true;
            
            var getValue = function(field) {
                var el = document.querySelector('.o_field_widget[name="' + field + '"]');
                var value = el ? parseFloat(el.textContent) || 0 : 0;
                console.log('Field ' + field + ' value:', value);
                return value;
            };
            
            // Get actual values from dashboard fields
            var goalValue = getValue('total_strategic_goals') || 5;
            var kraValue = getValue('total_kras') || 37;
            var kpiValue = getValue('total_kpis') || 108;
            var progValue = getValue('total_programmes') || 19;
            
            // Performance Overview Chart (Main Center Chart)
            var overviewCtx = this.el.querySelector('#performanceOverviewChart');
            if (overviewCtx) {
                console.log('Found performanceOverviewChart canvas element');
                try {
                    this.overviewChart = new Chart(overviewCtx.getContext('2d'), {
                        type: 'bar',
                        data: {
                            labels: ['Strategic Goals', 'KRAs', 'KPIs', 'Programmes', 'Directorates', 'Divisions'],
                            datasets: [{
                                label: 'Count',
                                data: [goalValue, kraValue, kpiValue, progValue, getValue('total_directorates') || 19, getValue('total_divisions') || 10],
                                backgroundColor: [
                                    'rgba(102, 126, 234, 0.8)',
                                    'rgba(17, 153, 142, 0.8)',
                                    'rgba(252, 182, 159, 0.8)',
                                    'rgba(250, 112, 154, 0.8)',
                                    'rgba(168, 237, 234, 0.8)',
                                    'rgba(251, 194, 235, 0.8)'
                                ],
                                borderColor: [
                                    'rgba(102, 126, 234, 1)',
                                    'rgba(17, 153, 142, 1)',
                                    'rgba(252, 182, 159, 1)',
                                    'rgba(250, 112, 154, 1)',
                                    'rgba(168, 237, 234, 1)',
                                    'rgba(251, 194, 235, 1)'
                                ],
                                borderWidth: 2,
                                borderRadius: 8,
                                borderSkipped: false,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    grid: {
                                        color: 'rgba(0,0,0,0.1)'
                                    },
                                    ticks: {
                                        font: {
                                            size: 12
                                        }
                                    }
                                },
                                x: {
                                    grid: {
                                        display: false
                                    },
                                    ticks: {
                                        font: {
                                            size: 11
                                        },
                                        maxRotation: 45,
                                        minRotation: 0
                                    }
                                }
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                tooltip: {
                                    backgroundColor: 'rgba(0,0,0,0.8)',
                                    titleColor: '#fff',
                                    bodyColor: '#fff',
                                    borderColor: 'rgba(255,255,255,0.2)',
                                    borderWidth: 1,
                                    callbacks: {
                                        label: function(context) {
                                            return context.dataset.label + ': ' + context.parsed.y;
                                        }
                                    }
                                }
                            }
                        }
                    });
                } catch (error) {
                    console.error('Error creating performance overview chart:', error);
                }
            } else {
                console.error('Could not find performanceOverviewChart canvas element');
            }
            
            // Performance Trends Chart (Center Bottom)
            var trendsCtx = this.el.querySelector('#trendsChart');
            if (trendsCtx) {
                console.log('Found trendsChart canvas element');
                try {
                    this.trendsChart = new Chart(trendsCtx.getContext('2d'), {
                        type: 'line',
                        data: {
                            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                            datasets: [{
                                label: 'Overall Performance',
                                data: [65, 72, 78, 82, 85, 88],
                                borderColor: 'rgba(102, 126, 234, 1)',
                                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                                fill: true,
                                tension: 0.4,
                                pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                                pointBorderColor: '#fff',
                                pointBorderWidth: 2,
                                pointRadius: 4,
                                pointHoverRadius: 6
                            }, {
                                label: 'Target',
                                data: [70, 75, 80, 85, 88, 90],
                                borderColor: 'rgba(17, 153, 142, 1)',
                                backgroundColor: 'rgba(17, 153, 142, 0.05)',
                                fill: false,
                                tension: 0.3,
                                pointBackgroundColor: 'rgba(17, 153, 142, 1)',
                                pointBorderColor: '#fff',
                                pointBorderWidth: 2,
                                pointRadius: 3,
                                pointHoverRadius: 5,
                                borderDash: [5, 5]
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 100,
                                    grid: {
                                        color: 'rgba(0,0,0,0.1)'
                                    },
                                    ticks: {
                                        callback: function(value) {
                                            return value + '%';
                                        },
                                        font: {
                                            size: 11
                                        }
                                    }
                                },
                                x: {
                                    grid: {
                                        display: false
                                    },
                                    ticks: {
                                        font: {
                                            size: 11
                                        }
                                    }
                                }
                            },
                            plugins: {
                                legend: {
                                    position: 'top',
                                    align: 'start',
                                    labels: {
                                        usePointStyle: true,
                                        padding: 15,
                                        font: {
                                            size: 11
                                        }
                                    }
                                },
                                tooltip: {
                                    backgroundColor: 'rgba(0,0,0,0.8)',
                                    titleColor: '#fff',
                                    bodyColor: '#fff',
                                    borderColor: 'rgba(255,255,255,0.2)',
                                    borderWidth: 1,
                                    callbacks: {
                                        label: function(context) {
                                            return context.dataset.label + ': ' + context.parsed.y + '%';
                                        }
                                    }
                                }
                            }
                        }
                    });
                } catch (error) {
                    console.error('Error creating trends chart:', error);
                }
            } else {
                console.error('Could not find trendsChart canvas element');
            }
            
            // Performance Distribution Chart (Right Column)
            var distributionCtx = this.el.querySelector('#distributionChart');
            if (distributionCtx) {
                console.log('Found distributionChart canvas element');
                try {
                    this.distributionChart = new Chart(distributionCtx.getContext('2d'), {
                        type: 'doughnut',
                        data: {
                            labels: ['Excellent', 'Good', 'Fair', 'Poor'],
                            datasets: [{
                                data: [40, 35, 20, 5],
                                backgroundColor: [
                                    'rgba(17, 153, 142, 0.8)',
                                    'rgba(102, 126, 234, 0.8)',
                                    'rgba(252, 182, 159, 0.8)',
                                    'rgba(250, 112, 154, 0.8)'
                                ],
                                borderColor: [
                                    'rgba(17, 153, 142, 1)',
                                    'rgba(102, 126, 234, 1)',
                                    'rgba(252, 182, 159, 1)',
                                    'rgba(250, 112, 154, 1)'
                                ],
                                borderWidth: 2,
                                hoverOffset: 4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    align: 'center',
                                    labels: {
                                        usePointStyle: true,
                                        padding: 10,
                                        font: {
                                            size: 10
                                        }
                                    }
                                },
                                tooltip: {
                                    backgroundColor: 'rgba(0,0,0,0.8)',
                                    titleColor: '#fff',
                                    bodyColor: '#fff',
                                    borderColor: 'rgba(255,255,255,0.2)',
                                    borderWidth: 1,
                                    callbacks: {
                                        label: function(context) {
                                            return context.label + ': ' + context.parsed + '%';
                                        }
                                    }
                                }
                            }
                        }
                    });
                } catch (error) {
                    console.error('Error creating distribution chart:', error);
                }
            } else {
                console.error('Could not find distributionChart canvas element');
            }
            
            console.log('Charts initialization completed');
        },
        
        _destroyDashboardCharts: function() {
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
        },
    });
});
