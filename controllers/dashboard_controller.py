from odoo import http
from odoo.http import request
import json


class PerformanceDashboardController(http.Controller):

    @http.route('/performance/dashboard/data', type='json', auth='user')
    def get_dashboard_data(self, filters=None):
        """Return JSON data for dashboard charts and widgets.
        Accepts optional 'filters' dict from the client to provide filtered analytics.
        """
        dashboard = request.env['performance.dashboard'].search([], limit=1)
        if not dashboard:
            dashboard = request.env['performance.dashboard'].create({})

        # Normalize filters from jsonrequest if not passed as arg
        if filters is None:
            try:
                payload = request.jsonrequest or {}
                filters = payload.get('filters')
            except Exception:
                filters = None

        # Get real-time metrics
        realtime_data = dashboard.get_realtime_metrics()

        # Get dashboard analytics (filtered if requested)
        if filters:
            dashboard_data = dashboard.get_filtered_dashboard_data(filters)
        else:
            dashboard_data = dashboard.get_dashboard_data()

        # Merge real-time metrics with dashboard data
        dashboard_data.setdefault('summary', {})
        dashboard_data['summary'].update(realtime_data)

        return dashboard_data

    @http.route('/performance/dashboard/summary', type='json', auth='user')
    def get_summary_stats(self):
        """Return real-time summary statistics"""
        dashboard = request.env['performance.dashboard'].search([], limit=1)
        if not dashboard:
            dashboard = request.env['performance.dashboard'].create({})
        
        return dashboard.get_realtime_metrics()
    
    @http.route('/performance/dashboard/chart/<string:chart_type>', type='json', auth='user')
    def get_chart_data(self, chart_type):
        """Return specific chart data"""
        dashboard = request.env['performance.dashboard'].search([], limit=1)
        if not dashboard:
            dashboard = request.env['performance.dashboard'].create({})
            
        data = dashboard.get_dashboard_data()
        
        if chart_type == 'goals_performance':
            return {
                'labels': [goal['name'] for goal in data['goals_performance']],
                'datasets': [{
                    'label': 'Performance %',
                    'data': [goal['performance'] for goal in data['goals_performance']],
                    'backgroundColor': [
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                    ]
                }]
            }
        
        elif chart_type == 'distribution':
            dist = data['distribution']
            return {
                'labels': ['Excellent (90%+)', 'Good (70-89%)', 'Fair (50-69%)', 'Poor (<50%)'],
                'datasets': [{
                    'data': [dist['excellent'], dist['good'], dist['fair'], dist['poor']],
                    'backgroundColor': [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(255, 152, 0, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ]
                }]
            }
        
        elif chart_type == 'top_kpis':
            top_kpis = data['top_kpis'][:10]  # Top 10 KPIs
            return {
                'labels': [kpi['name'][:30] + '...' if len(kpi['name']) > 30 else kpi['name'] for kpi in top_kpis],
                'datasets': [{
                    'label': 'Achievement %',
                    'data': [kpi['performance'] for kpi in top_kpis],
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'fill': True
                }]
            }
        
        return {}
    
    @http.route('/performance/dashboard/summary', type='json', auth='user')
    def get_summary_stats(self):
        """Return summary statistics for dashboard widgets"""
        dashboard = request.env['performance.dashboard'].search([], limit=1)
        if not dashboard:
            dashboard = request.env['performance.dashboard'].create({})
        
        data = dashboard.get_dashboard_data()
        return data['summary']