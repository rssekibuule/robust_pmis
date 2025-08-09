#!/usr/bin/env python3
import sys
import json
import traceback
import odoo
from odoo import api, SUPERUSER_ID

DB = sys.argv[1] if len(sys.argv) > 1 else 'robust_pmis'

RESULT = {
    'db': DB,
    'actions_found': {},
    'views_found': {},
    'menus_found': {},
    'model_calls': {},
    'errors': []
}

ACTIONS = [
    'robust_pmis.action_performance_dashboard_unified',
    'robust_pmis.action_strategic_kpi_with_programmes',
    'robust_pmis.action_programme_objective_indicators',
    'robust_pmis.action_piap_action',
    'robust_pmis.action_directorate_performance_dashboard',
    'robust_pmis.action_division_performance_dashboard',
    'robust_pmis.action_strategic_plan_budget',
    'robust_pmis.action_kcca_programme',
    'robust_pmis.action_key_performance_indicator',
    'robust_pmis.action_key_result_area',
    'robust_pmis.action_strategic_goal',
]

VIEWS = [
    'robust_pmis.view_performance_dashboard_form',
]

MENUS = [
    'robust_pmis.menu_performance_dashboard_unified',
]

odoo.tools.config['db_name'] = DB

with api.Environment.manage():
    registry = odoo.modules.registry.Registry(DB)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Check actions
        for xmlid in ACTIONS:
            try:
                rec = env.ref(xmlid)
                RESULT['actions_found'][xmlid] = bool(rec)
            except Exception as e:
                RESULT['actions_found'][xmlid] = False
                RESULT['errors'].append(f"missing_action:{xmlid}:{e}")
        # Check views
        for xmlid in VIEWS:
            try:
                rec = env.ref(xmlid)
                RESULT['views_found'][xmlid] = bool(rec)
            except Exception as e:
                RESULT['views_found'][xmlid] = False
                RESULT['errors'].append(f"missing_view:{xmlid}:{e}")
        # Check menus
        for xmlid in MENUS:
            try:
                rec = env.ref(xmlid)
                RESULT['menus_found'][xmlid] = bool(rec)
            except Exception as e:
                RESULT['menus_found'][xmlid] = False
                RESULT['errors'].append(f"missing_menu:{xmlid}:{e}")
        # Call model methods
        try:
            dash = env['performance.dashboard'].search([], limit=1)
            if not dash:
                dash = env['performance.dashboard'].create({'name': 'Smoke Dashboard'})
            data = dash.get_dashboard_data()
            summary = dash.get_realtime_metrics()
            RESULT['model_calls'] = {
                'get_dashboard_data_ok': bool(data),
                'get_realtime_metrics_ok': bool(summary),
                'summary_keys': sorted(list(summary.keys()))[:6],
            }
        except Exception:
            RESULT['model_calls'] = {'error': traceback.format_exc()}

print(json.dumps(RESULT, indent=2))

