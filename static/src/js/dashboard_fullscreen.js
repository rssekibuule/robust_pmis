/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";

export class DashboardFullscreen extends Component {
    setup() {
        onMounted(() => {
            this.makeFullScreen();
        });
    }

    makeFullScreen() {
        // Remove any width constraints from parent containers
        const elementsToExpand = [
            '.o_action_manager',
            '.o_content',
            '.o_form_view',
            '.o_form_sheet_bg',
            '.o_main_content',
            '.o_web_client'
        ];

        elementsToExpand.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                el.style.width = '100%';
                el.style.maxWidth = 'none';
                el.style.margin = '0';
                el.style.padding = '0';
            });
        });

        // Specifically target the dashboard form
        const dashboard = document.querySelector('.o_fullscreen_dashboard');
        if (dashboard) {
            dashboard.style.width = '100vw';
            dashboard.style.minHeight = '100vh';
            dashboard.style.margin = '0';
            dashboard.style.padding = '0';
        }

        // Target the sheet within dashboard
        const dashboardSheet = document.querySelector('.o_dashboard_sheet');
        if (dashboardSheet) {
            dashboardSheet.style.width = '100%';
            dashboardSheet.style.maxWidth = 'none';
            dashboardSheet.style.padding = '20px';
        }
    }
}

// Auto-execute when dashboard loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.o_fullscreen_dashboard')) {
        const dashboard = new DashboardFullscreen();
        dashboard.makeFullScreen();
    }
});

// Also execute on window load and resize
window.addEventListener('load', function() {
    if (document.querySelector('.o_fullscreen_dashboard')) {
        const dashboard = new DashboardFullscreen();
        dashboard.makeFullScreen();
    }
});

window.addEventListener('resize', function() {
    if (document.querySelector('.o_fullscreen_dashboard')) {
        const dashboard = new DashboardFullscreen();
        dashboard.makeFullScreen();
    }
});
