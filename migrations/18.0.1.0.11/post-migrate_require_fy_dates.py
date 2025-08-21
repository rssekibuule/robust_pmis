# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Param = env['ir.config_parameter'].sudo()

    # Ensure plan baseline
    if not Param.get_param('robust_pmis.plan_start_year'):
        Param.set_param('robust_pmis.plan_start_year', '2024')
    if not Param.get_param('robust_pmis.plan_years'):
        Param.set_param('robust_pmis.plan_years', '5')

    from datetime import date
    fy_start = date(2024, 7, 1)
    fy_end = date(2025, 6, 30)

    # Normalize missing/partial FY dates to FY 2024/25 to satisfy new constraints.
    KPI = env['key.performance.indicator']
    PI = env['performance.indicator']

    def _fix_dates(records):
        fixed = 0
        partial = 0
        for r in records:
            if not r.start_date and not r.end_date:
                r.start_date, r.end_date = fy_start, fy_end
                fixed += 1
            elif r.start_date and not r.end_date:
                r.end_date = fy_end
                partial += 1
            elif r.end_date and not r.start_date:
                r.start_date = fy_start
                partial += 1
        return fixed, partial

    k_all = KPI.search([])
    p_all = PI.search([])

    k_fixed, k_partial = _fix_dates(k_all)
    p_fixed, p_partial = _fix_dates(p_all)

    print(f"[migration] FY date normalization complete. KPI fixed={k_fixed}, partial={k_partial}; PI fixed={p_fixed}, partial={p_partial}.")
