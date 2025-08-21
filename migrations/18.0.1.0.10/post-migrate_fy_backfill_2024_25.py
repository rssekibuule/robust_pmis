# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

"""
Backfill for FY 2024/25:
- Ensure plan_start_year and plan_years have sane defaults if unset (2024, 5).
- For KPIs and Programme Indicators with no dates, set start_date to FY2024/25 start to scope constraints sanely.
- For Performance Indicators: if target_fy2024_25 or actual_fy2024_25 are None, set them conservatively:
  * target_fy2024_25 := target_value if present else 0.0 (explicit, conservative)
  * actual_fy2024_25 := current_value if present else 0.0 (explicit, conservative)
- For KPIs: if target/current are None, set them to 0.0 so validations pass without optimistic inflation.
This migration is idempotent and only fills Nones, it does not overwrite explicit numbers.
"""

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Param = env['ir.config_parameter'].sudo()

    # Ensure plan config exists
    if not Param.get_param('robust_pmis.plan_start_year'):
        Param.set_param('robust_pmis.plan_start_year', '2024')
    if not Param.get_param('robust_pmis.plan_years'):
        Param.set_param('robust_pmis.plan_years', '5')

    # Compute FY 2024/25 boundaries (Uganda FY: Jul 1, 2024 to Jun 30, 2025)
    from datetime import date
    fy_start = date(2024, 7, 1)
    fy_end = date(2025, 6, 30)

    # Backfill KPIs
    KPI = env['key.performance.indicator']
    kpis = KPI.search([])
    filled_kpi_targets = filled_kpi_currents = dated_kpis = 0
    for kpi in kpis:
        # Set default dates if missing to ensure FY assignment works
        if not kpi.start_date and not kpi.end_date:
            # Limit scope to FY2024/25 only to satisfy FY validations without forcing future years yet
            kpi.start_date = fy_start
            kpi.end_date = fy_end
            dated_kpis += 1
        # Conservative fill for None values
        if kpi.target_value is None:
            kpi.target_value = 0.0
            filled_kpi_targets += 1
        if kpi.current_value is None:
            kpi.current_value = 0.0
            filled_kpi_currents += 1

    # Backfill Programme Performance Indicators
    PI = env['performance.indicator']
    indicators = PI.search([])
    filled_pi_targets = filled_pi_actuals = dated_indicators = 0
    for pi in indicators:
        # Default dates if missing
        if not pi.start_date and not pi.end_date:
            # Limit scope to FY2024/25 only to satisfy FY validations without forcing future years yet
            pi.start_date = fy_start
            pi.end_date = fy_end
            dated_indicators += 1
        # Only fill None, do not overwrite explicit values
        if hasattr(pi, 'target_fy2024_25'):
            if pi.target_fy2024_25 is None:
                pi.target_fy2024_25 = pi.target_value if pi.target_value is not None else 0.0
                filled_pi_targets += 1
        if hasattr(pi, 'actual_fy2024_25'):
            if pi.actual_fy2024_25 is None:
                pi.actual_fy2024_25 = pi.current_value if pi.current_value is not None else 0.0
                filled_pi_actuals += 1

    print(f"[migration] FY 2024/25 backfill complete. KPIs dated: {dated_kpis}, KPI targets filled: {filled_kpi_targets}, KPI currents filled: {filled_kpi_currents}. PIs dated: {dated_indicators}, PI targets filled: {filled_pi_targets}, PI actuals filled: {filled_pi_actuals}.")
