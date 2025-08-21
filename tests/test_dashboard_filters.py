# -*- coding: utf-8 -*-
"""
Smoke tests for dashboard filter computations and period options.
These are lightweight and can be run with Odoo test runner or as reference.
"""
from odoo import api, SUPERUSER_ID


def _call(env, method, args=None):
    rec = env['performance.dashboard'].search([], limit=1)
    if not rec:
        rec = env['performance.dashboard'].create({})
    return getattr(rec, method)(*(args or []))


def test_period_options(env):
    opts = _call(env, 'get_period_options')
    assert isinstance(opts, list) and len(opts) >= 5
    assert any(o.get('key', '').startswith('fy:') for o in opts)


def test_filtered_averages_do_not_inflate(env):
    # Baseline: unfiltered
    data_all = _call(env, 'get_dashboard_data')
    # Filter to a FY where many programmes may have no progress; averages should not inflate > 100 and should be numeric
    # Pick first FY key from options to ensure existence
    opts = _call(env, 'get_period_options')
    fy_keys = [o['key'] for o in opts if o['key'].startswith('fy:')]
    if not fy_keys:
        return
    data_filtered = _call(env, 'get_filtered_dashboard_data', [ {'period': fy_keys[0], 'data_type': 'all', 'scope': 'organization', 'entity': 'all', 'performance': 'all'} ])

    for payload in (data_all, data_filtered):
        assert 'summary' in payload
        s = payload['summary']
        for k in ('avg_performance', 'kpi_only_performance', 'avg_kpi_performance', 'avg_kra_performance', 'avg_programme_performance', 'avg_division_programme_performance'):
            v = float(s.get(k, 0) or 0)
            assert 0.0 <= v <= 100.0


def run(env):
    test_period_options(env)
    test_filtered_averages_do_not_inflate(env)
    return True
