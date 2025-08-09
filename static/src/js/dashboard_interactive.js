// Dashboard Interactive Charts - Plain JavaScript Implementation
(function() {
    'use strict';

    // Auto-initialize when DOM is ready
    function initializeDashboard() {
        console.log('Initializing dashboard charts...');
        
        // Load Chart.js if not available
        if (!window.Chart) {
            console.log('Loading Chart.js...');
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js';
            script.onload = function() {
                console.log('Chart.js loaded successfully');
                createAllCharts();
            };
            script.onerror = function() {
                console.error('Failed to load Chart.js');
            };
            document.head.appendChild(script);
        } else {
            console.log('Chart.js already available');
            createAllCharts();
        }
    }

    function createAllCharts() {
        console.log('Creating charts...');
        
        // Strategic Goals Chart
        const goalsCanvas = document.getElementById('goalsChart');
        if (goalsCanvas) {
            console.log('Creating Strategic Goals chart');
            new Chart(goalsCanvas, {
                type: 'bar',
                data: {
                    labels: ['Infrastructure Development', 'Service Delivery', 'Revenue Enhancement', 'Environmental Management', 'Good Governance'],
                    datasets: [{
                        label: 'Performance (%)',
                        data: [85, 78, 92, 71, 88],
                        backgroundColor: [
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(46, 204, 113, 0.8)',
                            'rgba(243, 156, 18, 0.8)',
                            'rgba(231, 76, 60, 0.8)',
                            'rgba(155, 89, 182, 0.8)'
                        ],
                        borderColor: [
                            'rgba(52, 152, 219, 1)',
                            'rgba(46, 204, 113, 1)',
                            'rgba(243, 156, 18, 1)',
                            'rgba(231, 76, 60, 1)',
                            'rgba(155, 89, 182, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: { 
                                callback: function(value) { 
                                    return value + '%'; 
                                } 
                            }
                        }
                    },
                    onClick: function(event, elements) {
                        if (elements.length > 0) {
                            console.log('Strategic Goal clicked:', elements[0].index);
                        }
                    }
                }
            });
        } else {
            console.log('Goals chart canvas not found');
        }
        
        // KRA Performance Chart
        const kraCanvas = document.getElementById('kraChart');
        if (kraCanvas) {
            console.log('Creating KRA Performance chart');
            new Chart(kraCanvas, {
                type: 'doughnut',
                data: {
                    labels: ['Road Infrastructure', 'Drainage Systems', 'Waste Management', 'Traffic Management', 'Public Transport'],
                    datasets: [{
                        data: [85, 78, 82, 75, 79],
                        backgroundColor: [
                            'rgba(46, 204, 113, 0.8)',
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(243, 156, 18, 0.8)',
                            'rgba(231, 76, 60, 0.8)',
                            'rgba(155, 89, 182, 0.8)'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            position: 'bottom',
                            labels: { usePointStyle: true }
                        }
                    },
                    onClick: function(event, elements) {
                        if (elements.length > 0) {
                            console.log('KRA clicked:', elements[0].index);
                        }
                    }
                }
            });
        } else {
            console.log('KRA chart canvas not found');
        }
        
        // Performance Trends Chart
        const trendsCanvas = document.getElementById('trendsChart');
        if (trendsCanvas) {
            console.log('Creating Performance Trends chart');
            new Chart(trendsCanvas, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'KRA Performance',
                        data: [65, 68, 72, 75, 78, 80],
                        borderColor: 'rgba(46, 204, 113, 1)',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }, {
                        label: 'KPI Performance',
                        data: [60, 63, 67, 70, 73, 75],
                        borderColor: 'rgba(52, 152, 219, 1)',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: { 
                                callback: function(value) { 
                                    return value + '%'; 
                                } 
                            }
                        }
                    },
                    onClick: function(event, elements) {
                        if (elements.length > 0) {
                            console.log('Trend data clicked:', elements[0].index);
                        }
                    }
                }
            });
        } else {
            console.log('Trends chart canvas not found');
        }
        
        // Performance Distribution Chart
        const distributionCanvas = document.getElementById('distributionChart');
        if (distributionCanvas) {
            console.log('Creating Performance Distribution chart');
            new Chart(distributionCanvas, {
                type: 'pie',
                data: {
                    labels: ['Excellent (90%+)', 'Good (70-89%)', 'Fair (50-69%)', 'Poor (<50%)'],
                    datasets: [{
                        data: [25, 35, 28, 12],
                        backgroundColor: [
                            'rgba(46, 204, 113, 0.8)',
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(243, 156, 18, 0.8)',
                            'rgba(231, 76, 60, 0.8)'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            position: 'bottom',
                            labels: { usePointStyle: true }
                        }
                    },
                    onClick: function(event, elements) {
                        if (elements.length > 0) {
                            console.log('Distribution clicked:', elements[0].index);
                        }
                    }
                }
            });
        } else {
            console.log('Distribution chart canvas not found');
        }
        
        console.log('All charts created successfully');
    }

    // Multiple ways to initialize to ensure it works
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initializeDashboard, 1000);
        });
    } else {
        setTimeout(initializeDashboard, 1000);
    }

    // Also try when window loads
    window.addEventListener('load', function() {
        setTimeout(initializeDashboard, 1500);
    });

    // And after a longer delay as fallback
    setTimeout(function() {
        if (!window.chartsInitialized) {
            console.log('Fallback initialization...');
            initializeDashboard();
            window.chartsInitialized = true;
        }
    }, 3000);

})();
