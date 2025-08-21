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

        # Merge real-time metrics with dashboard data without overriding computed averages
        # Keep only totals from realtime to avoid zeroing analytics-driven averages
        dashboard_data.setdefault('summary', {})
        if isinstance(realtime_data, dict):
            safe_keys = {
                'total_goals',
                'total_strategic_goals',
                'total_kras',
                'total_kpis',
                'total_programmes',
                'total_directorates',
                'total_divisions',
            }
            for k in safe_keys:
                if k in realtime_data:
                    dashboard_data['summary'][k] = realtime_data[k]

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

    @http.route(['/odoo/action-<string:xmlid>'], type='http', auth='user')
    def legacy_action_redirect(self, xmlid, **kw):
        """Redirect legacy /odoo/action-<xmlid>?... to /web#action=<xmlid>&...
        This preserves any useful query params such as view_type and avoids
        the deprecated route which can trigger 'tree' default view errors.
        """
        try:
            # Preserve only safe params to append to the hash
            params = []
            view_type = kw.get('view_type')
            if view_type:
                # Normalize legacy 'tree' to 'list' for Odoo 18
                if view_type == 'tree':
                    view_type = 'list'
                params.append(f"view_type={view_type}")
            menu_id = kw.get('menu_id')
            if menu_id:
                params.append(f"menu_id={menu_id}")
            model = kw.get('model')
            if model:
                params.append(f"model={model}")
            # Build target hash URL
            suffix = ('&' + '&'.join(params)) if params else ''
            target = f"/web#action={xmlid}{suffix}"
            return request.redirect(target, code=301)
        except Exception:
            # Fallback to base web client
            return request.redirect('/web', code=302)


    @http.route(['/odoo/action-<int:action_id>'], type='http', auth='user')
    def legacy_action_id_redirect(self, action_id, **kw):
        """Redirect legacy /odoo/action-<id> to /web#action=<id> preserving safe params."""
        try:
            params = []
            view_type = kw.get('view_type')
            if view_type:
                if view_type == 'tree':
                    view_type = 'list'
                params.append(f"view_type={view_type}")
            menu_id = kw.get('menu_id')
            if menu_id:
                params.append(f"menu_id={menu_id}")
            model = kw.get('model')
            if model:
                params.append(f"model={model}")
            suffix = ('&' + '&'.join(params)) if params else ''
            target = f"/web#action={action_id}{suffix}"
            return request.redirect(target, code=301)
        except Exception:
            return request.redirect('/web', code=302)

    # Explicit redirects for stubborn legacy links observed in screenshots
    @http.route(['/odoo/action-robust_pmis.action_directorate_performance_dashboard'], type='http', auth='user')
    def legacy_directorate_dashboard(self, **kw):
        params = []
        if kw.get('view_type'):
            params.append(f"view_type={kw.get('view_type')}")
        target = '/web#action=robust_pmis.action_directorate_performance_dashboard' + (('&' + '&'.join(params)) if params else '')
        return request.redirect(target, code=301)

    @http.route(['/odoo/action-robust_pmis.action_division_performance_dashboard'], type='http', auth='user')
    def legacy_division_dashboard(self, **kw):
        params = []
        if kw.get('view_type'):
            params.append(f"view_type={kw.get('view_type')}")
        target = '/web#action=robust_pmis.action_division_performance_dashboard' + (('&' + '&'.join(params)) if params else '')
        return request.redirect(target, code=301)


    def get_summary_stats(self):
        """Return summary statistics for dashboard widgets"""
        dashboard = request.env['performance.dashboard'].search([], limit=1)
        if not dashboard:
            dashboard = request.env['performance.dashboard'].create({})

        data = dashboard.get_dashboard_data()
        return data['summary']