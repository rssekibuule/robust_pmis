/** @odoo-module **/

// Dashboard Real-time Data Loader for Odoo 18
class DashboardDataLoader {
    constructor() {
        this.refreshInterval = null;
        this.isLoading = false;
    }

    async loadSummaryData() {
        if (this.isLoading) return;
        this.isLoading = true;
        
        try {
            // Try using Odoo's RPC if available
            let data;
            if (window.odoo && window.odoo.http) {
                const response = await window.odoo.http.post('/performance/dashboard/summary', {});
                data = response.result || response;
            } else {
                // Fallback to fetch API
                const response = await fetch('/performance/dashboard/summary', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {}
                    })
                });
                
                const result = await response.json();
                data = result.result;
            }
            
            if (data) {
                this.updateDashboardUI(data);
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        } finally {
            this.isLoading = false;
        }
    }

    updateDashboardUI(data) {
        console.log('Updating dashboard with real-time data:', data);
        
        // Update strategic goals card
        this.updateFieldValue('total_strategic_goals', data.total_strategic_goals || 0);
        this.updateFieldValue('total_goals', data.total_goals || 0);

        // Update KRAs card
        this.updateFieldValue('total_kras', data.total_kras || 0);

        // Update KPIs card
        this.updateFieldValue('total_kpis', data.total_kpis || 0);

        // Update programmes card
        this.updateFieldValue('total_programmes', data.total_programmes || 0);

        // Update directorates card
        this.updateFieldValue('total_directorates', data.total_directorates || 0);

        // Update divisions card
        this.updateFieldValue('total_divisions', data.total_divisions || 0);

        // Update performance metrics
        this.updatePerformanceMetrics(data);
        
        // Show last updated time
        this.updateLastRefreshTime();
    }

    updateFieldValue(fieldName, value) {
        // Try multiple selectors to find the field
        const selectors = [
            `[name="${fieldName}"]`,
            `field[name="${fieldName}"]`,
            `.o_field_widget[name="${fieldName}"]`,
            `[data-field="${fieldName}"]`,
            `.field-${fieldName}`
        ];

        let updated = false;
        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (element.tagName === 'INPUT') {
                    element.value = value;
                } else {
                    element.textContent = value;
                }
                updated = true;
            });
        }
        
        // If no field found, try to update any element with the field name in its content
        if (!updated) {
            const allElements = document.querySelectorAll('h2, span, div');
            allElements.forEach(element => {
                if (element.getAttribute('field') === fieldName || 
                    element.classList.contains(fieldName)) {
                    element.textContent = value;
                }
            });
        }
    }

    updatePerformanceMetrics(data) {
        // Update performance bars
        this.updatePerformanceBar('kra', data.avg_kra_performance || 0);
        this.updatePerformanceBar('kpi', data.avg_kpi_performance || 0);

        // Update quick stats in the sidebar
        const statsMapping = {
            'kra-performance': data.avg_kra_performance || 0,
            'programme-performance': data.avg_programme_performance || 0,
            'directorate-performance': data.avg_directorate_performance || 0,
            'division-performance': data.avg_division_performance || 0
        };

        Object.entries(statsMapping).forEach(([key, value]) => {
            const elements = document.querySelectorAll(`.${key}-value, .${key}, [data-stat="${key}"]`);
            elements.forEach(element => {
                element.textContent = `${Math.round(value)}%`;
            });
        });
    }

    updatePerformanceBar(type, percentage) {
        const roundedPercentage = Math.round(percentage);
        const selectors = [
            `.${type}-performance-bar`,
            `.performance-bar.${type}`,
            `[data-performance="${type}"]`,
            `.performance-fill.${type}`
        ];

        for (const selector of selectors) {
            const bars = document.querySelectorAll(selector);
            bars.forEach(bar => {
                bar.style.width = `${roundedPercentage}%`;
                
                // Update text content
                const textElement = bar.querySelector('.performance-text') || bar;
                if (textElement) {
                    textElement.textContent = `${roundedPercentage}%`;
                }
                
                // Update color class based on performance
                bar.className = bar.className.replace(/excellent|good|fair|poor/g, '').trim();
                if (roundedPercentage >= 90) {
                    bar.classList.add('excellent');
                } else if (roundedPercentage >= 70) {
                    bar.classList.add('good');
                } else if (roundedPercentage >= 50) {
                    bar.classList.add('fair');
                } else {
                    bar.classList.add('poor');
                }
            });
        }
    }

    updateLastRefreshTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        // Update or create last refresh indicator
        let refreshIndicator = document.querySelector('.dashboard-last-refresh');
        if (!refreshIndicator) {
            refreshIndicator = document.createElement('div');
            refreshIndicator.className = 'dashboard-last-refresh';
            refreshIndicator.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
            `;
            document.body.appendChild(refreshIndicator);
        }
        
        refreshIndicator.textContent = `Last updated: ${timeString}`;
        
        // Fade out after 3 seconds
        setTimeout(() => {
            refreshIndicator.style.opacity = '0.5';
        }, 3000);
    }

    startAutoRefresh(interval = 30000) { // 30 seconds
        this.stopAutoRefresh();
        console.log(`Starting auto-refresh every ${interval/1000} seconds`);
        
        this.refreshInterval = setInterval(() => {
            console.log('Auto-refreshing dashboard data...');
            this.loadSummaryData();
        }, interval);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
            console.log('Auto-refresh stopped');
        }
    }
}

// Initialize dashboard when DOM is ready
function initializeDashboard() {
    console.log('Checking for dashboard elements...');
    
    if (document.querySelector('.o_fullscreen_dashboard, .o_dashboard_form, [model="performance.dashboard"]')) {
        console.log('Dashboard found! Initializing data loader...');
        
        const loader = new DashboardDataLoader();
        
        // Load initial data immediately
        loader.loadSummaryData();
        
        // Start auto-refresh every 30 seconds
        loader.startAutoRefresh(30000);
        
        // Add manual refresh button if it exists
        const refreshButton = document.querySelector('.dashboard-refresh-btn, .btn-refresh');
        if (refreshButton) {
            refreshButton.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Manual refresh triggered');
                loader.loadSummaryData();
            });
        }
        
        // Stop auto-refresh when leaving the page
        window.addEventListener('beforeunload', () => {
            loader.stopAutoRefresh();
        });
        
        // Make loader globally available for debugging
        window.dashboardLoader = loader;
        
        return loader;
    } else {
        console.log('Dashboard not found, retrying in 2 seconds...');
        return null;
    }
}

// Try initialization on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initializeDashboard, 1000); // Wait 1 second for Odoo to load
});

// Also try on window load as backup
window.addEventListener('load', function() {
    if (!window.dashboardLoader) {
        setTimeout(initializeDashboard, 2000); // Wait 2 seconds
    }
});

// Try initialization periodically until successful (max 10 times)
let initAttempts = 0;
const maxAttempts = 10;
const initInterval = setInterval(() => {
    if (initAttempts >= maxAttempts) {
        clearInterval(initInterval);
        console.log('Dashboard initialization max attempts reached');
        return;
    }
    
    if (!window.dashboardLoader) {
        console.log(`Dashboard initialization attempt ${initAttempts + 1}`);
        const loader = initializeDashboard();
        if (loader) {
            clearInterval(initInterval);
            console.log('Dashboard successfully initialized!');
        }
    } else {
        clearInterval(initInterval);
    }
    
    initAttempts++;
}, 3000); // Try every 3 seconds

// Export for manual use
window.DashboardDataLoader = DashboardDataLoader;
