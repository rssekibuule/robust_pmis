/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * KCCA Directorate Performance Chart Component
 * 
 * This component renders a performance chart for directorates using Chart.js
 */
export class DirectoratePerformanceChart extends Component {
    setup() {
        this.orm = useService("orm");
        this.chartRef = useRef("chart");
        this.state = useState({
            loading: true,
            directorates: [],
            chartInstance: null
        });
        
        onMounted(() => this.loadData());
    }
    
    async loadData() {
        try {
            this.state.loading = true;
            
            // Fetch directorate data
            const directorates = await this.orm.searchRead(
                "kcca.directorate", 
                [["active", "=", true]], 
                ["name", "overall_performance", "programme_count", "kpi_count", "division_count", "color"]
            );
            
            this.state.directorates = directorates;
            this.renderChart();
            this.state.loading = false;
        } catch (error) {
            console.error("Error loading directorate data:", error);
            this.state.loading = false;
        }
    }
    
    renderChart() {
        if (!this.chartRef.el) return;
        
        // If we already have a chart instance, destroy it
        if (this.state.chartInstance) {
            this.state.chartInstance.destroy();
        }
        
        const ctx = this.chartRef.el.getContext('2d');
        
        // Prepare data for the chart
        const directorateNames = this.state.directorates.map(dir => dir.name);
        const performanceData = this.state.directorates.map(dir => dir.overall_performance);
        const programmeData = this.state.directorates.map(dir => dir.programme_count);
        
        // Generate colors based on performance
        const backgroundColors = this.state.directorates.map(dir => {
            if (dir.color) {
                // Convert decimal color to hex
                return '#' + dir.color.toString(16).padStart(6, '0');
            } else if (dir.overall_performance >= 80) {
                return '#28a745'; // Green for high performance
            } else if (dir.overall_performance >= 60) {
                return '#ffc107'; // Yellow for medium performance
            } else {
                return '#dc3545'; // Red for low performance
            }
        });
        
        // Create the chart
        this.state.chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: directorateNames,
                datasets: [
                    {
                        label: 'Performance (%)',
                        data: performanceData,
                        backgroundColor: backgroundColors,
                        borderColor: backgroundColors.map(color => color),
                        borderWidth: 1,
                        borderRadius: 6,
                        barThickness: 20,
                    },
                    {
                        label: 'Programmes',
                        data: programmeData,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        borderRadius: 6,
                        barThickness: 20,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Directorate Performance & Programmes',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.parsed.y || 0;
                                return `${label}: ${value}${context.datasetIndex === 0 ? '%' : ''}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Value'
                        },
                        grid: {
                            drawBorder: false,
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Directorates'
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}

DirectoratePerformanceChart.template = 'robust_pmis.DirectoratePerformanceChart';

// Register the component
registry.category("view_widgets").add("directorate_performance_chart", DirectoratePerformanceChart);
