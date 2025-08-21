# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceDashboard(models.Model):
    _name = 'performance.dashboard'
    _description = 'Organization-wide Performance Dashboard'

    name = fields.Char(string='Dashboard', default='Organization Performance')
    # Legacy field kept for backward compatibility; label adjusted to avoid duplicate warning
    total_goals = fields.Integer(string='Total Goals (legacy)')
    total_strategic_goals = fields.Integer(string='Total Strategic Goals')
    total_kras = fields.Integer(string='Total KRAs')
    avg_kra_performance = fields.Float(string='Average KRA Performance')
    total_kpis = fields.Integer(string='Total KPIs')
    avg_kpi_performance = fields.Float(string='Average KPI Performance')
    total_programmes = fields.Integer(string='Total Programmes')
    avg_programme_performance = fields.Float(string='Average Programme Performance')
    total_directorates = fields.Integer(string='Total Directorates')
    avg_directorate_performance = fields.Float(string='Average Directorate Performance')
    total_divisions = fields.Integer(string='Total Divisions')
    avg_division_performance = fields.Float(string='Average Division Performance')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        # Recompute metrics for each created dashboard record
        for rec in records:
            rec.refresh_metrics()
        return records

    def _compute_dashboard_metrics(self):
        """Compute all dashboard metrics"""
        strategic_goals = self.env['strategic.goal'].search([('active', '=', True)])
        kras = self.env['key.result.area'].search([('active', '=', True)])
        # Include both strategic KPIs and programme-level performance indicators
        strategic_kpis = self.env['key.performance.indicator'].search([('active', '=', True)])
        programme_indicators = self.env['performance.indicator'].search([('active', '=', True)])
        # Combine both types of KPIs for total count
        total_kpi_count = len(strategic_kpis) + len(programme_indicators)
        
        programmes = self.env['kcca.programme'].search([('active', '=', True)])
        directorates = self.env['kcca.directorate'].search([('active', '=', True)])
        divisions = self.env['kcca.division'].search([('active', '=', True)])
        div_prog_rels = self.env['division.programme.rel'].search([('active', '=', True)])
        
        # Set basic counts
        self.total_goals = len(strategic_goals)  # Legacy field
        self.total_strategic_goals = len(strategic_goals)
        self.total_kras = len(kras)
        self.total_kpis = total_kpi_count  # Now includes both types
        self.total_programmes = len(programmes)
        self.total_directorates = len(directorates)
        self.total_divisions = len(divisions)
        
        # Calculate average KRA performance based on linked KPIs
        # Include 0% for KRAs that have no KPIs to avoid inflated averages
        if kras:
            kra_performances = []
            for kra in kras:
                kra_kpis = self.env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                if kra_kpis:
                    avg_kra_perf = sum((kpi.achievement_percentage or 0.0) for kpi in kra_kpis) / len(kra_kpis)
                    kra_performances.append(avg_kra_perf)
                else:
                    kra_performances.append(0.0)

            self.avg_kra_performance = (sum(kra_performances) / len(kra_performances)) if kra_performances else 0.0
        else:
            self.avg_kra_performance = 0.0
        
        # Calculate average KPI performance including both strategic KPIs and programme indicators
        all_performances = []
        
        # Add strategic KPI performances
        if strategic_kpis:
            strategic_performances = [kpi.achievement_percentage or 0.0 for kpi in strategic_kpis]
            all_performances.extend(strategic_performances)
        
        # Add programme indicator performances
        if programme_indicators:
            programme_performances = [ind.achievement_percentage or 0.0 for ind in programme_indicators]
            all_performances.extend(programme_performances)
        
        # Calculate overall KPI performance
        if all_performances:
            self.avg_kpi_performance = sum(all_performances) / len(all_performances)
        else:
            self.avg_kpi_performance = 0.0

        # Programmes: average of programme overall performance
        if programmes:
            prog_vals = [p.overall_performance or 0.0 for p in programmes]
            self.avg_programme_performance = (sum(prog_vals) / len(prog_vals)) if prog_vals else 0.0
        else:
            self.avg_programme_performance = 0.0

        # Directorates overall performance (from their KPI roll-ups)
        if directorates:
            dir_vals = [d.overall_performance or 0.0 for d in directorates]
            self.avg_directorate_performance = (sum(dir_vals) / len(dir_vals)) if dir_vals else 0.0
        else:
            self.avg_directorate_performance = 0.0

        # Divisions overall performance (if present on model)
        if divisions:
            div_vals = [v.overall_performance or 0.0 for v in divisions]
            self.avg_division_performance = (sum(div_vals) / len(div_vals)) if div_vals else 0.0
        else:
            self.avg_division_performance = 0.0
    
    def get_filtered_dashboard_data(self, filters=None):
        """Return filtered JSON data for dashboard charts using intuitive filters.
        Supported filters: data_type ('strategic'|'programme'|'all'),
        scope ('organization'|'strategic_goal'|'strategic_objective'|'programme'|'directorate'|'division'),
        entity (id or 'all'), performance (excellent/good/fair/poor/all), period (fy/q1..q4 - placeholder).
        """
        self.ensure_one()

        if not filters:
            return self.get_dashboard_data()

        # Build domains for both datasets (strategic KPIs and programme indicators)
        domain_kpi = []
        domain_prog = []
        domain_div_rel = [('active', '=', True)]

        # Performance filter
        perf = (filters or {}).get('performance')
        if perf and perf != 'all':
            if perf == 'excellent':
                domain_kpi.append(('achievement_percentage', '>=', 90))
                domain_prog.append(('achievement_percentage', '>=', 90))
                domain_div_rel.append(('performance_score', '>=', 90))
            elif perf == 'good':
                rng = [('achievement_percentage', '>=', 70), ('achievement_percentage', '<', 90)]
                domain_kpi.extend(rng)
                domain_prog.extend(rng)
                domain_div_rel.extend([('performance_score', '>=', 70), ('performance_score', '<', 90)])
            elif perf == 'fair':
                rng = [('achievement_percentage', '>=', 50), ('achievement_percentage', '<', 70)]
                domain_kpi.extend(rng)
                domain_prog.extend(rng)
                domain_div_rel.extend([('performance_score', '>=', 50), ('performance_score', '<', 70)])
            elif perf == 'poor':
                domain_kpi.append(('achievement_percentage', '<', 50))
                domain_prog.append(('achievement_percentage', '<', 50))
                domain_div_rel.append(('performance_score', '<', 50))

        # Scope + entity filter
        scope = (filters or {}).get('scope') or 'organization'
        entity = (filters or {}).get('entity') or 'all'
        try:
            entity_id = int(entity) if entity and entity != 'all' else None
        except Exception:
            entity_id = None

        if entity_id:
            if scope == 'strategic_goal':
                domain_kpi.append(('kra_id.strategic_objective_id.strategic_goal_id', '=', entity_id))
                # Programme indicators through programme -> objectives -> goal
                domain_prog.append(('parent_programme_id.strategic_objective_ids.strategic_goal_id', '=', entity_id))
                domain_div_rel.append(('programme_id.strategic_objective_ids.strategic_goal_id', '=', entity_id))
            elif scope == 'strategic_objective':
                domain_kpi.append(('kra_id.strategic_objective_id', '=', entity_id))
                domain_prog.append(('parent_programme_id.strategic_objective_ids', 'in', [entity_id]))
                domain_div_rel.append(('programme_id.strategic_objective_ids', 'in', [entity_id]))
            elif scope == 'programme':
                # Strategic KPIs via Objective -> Programmes linkage
                domain_kpi.append(('kra_id.strategic_objective_id.programme_ids', 'in', [entity_id]))
                domain_prog.append(('parent_programme_id', '=', entity_id))
                domain_div_rel.append(('programme_id', '=', entity_id))
            elif scope == 'directorate':
                # Strategic KPIs via Programmes implemented by this directorate
                domain_kpi.append(('kra_id.strategic_objective_id.programme_ids.implementing_directorate_ids', 'in', [entity_id]))
                domain_prog.append(('parent_programme_id.implementing_directorate_ids', 'in', [entity_id]))
                # Division relationships for divisions under this directorate or programmes implemented by this directorate
                domain_div_rel.append('|')
                domain_div_rel.append(('division_id.directorate_id', '=', entity_id))
                domain_div_rel.append(('programme_id.implementing_directorate_ids', 'in', [entity_id]))
            elif scope == 'division':
                # Strategic KPIs via Programmes implemented by this division
                domain_kpi.append(('kra_id.strategic_objective_id.programme_ids.division_programme_rel_ids.division_id', '=', entity_id))
                # Use division relationships table via programme
                domain_prog.append(('parent_programme_id.division_programme_rel_ids.division_id', '=', entity_id))
                domain_div_rel.append(('division_id', '=', entity_id))

        # Period filter (FY/Q) – apply using start/end date ranges on KPI/PI and Division-Programme relations
        def _fy_range(year_start):
            # Uganda FY assumed: Jul 1 (year_start) to Jun 30 (year_start+1)
            from datetime import date
            return date(year_start, 7, 1), date(year_start + 1, 6, 30)

        def _quarter_range(year_start, quarter):
            from datetime import date
            # Q1: Jul-Sep, Q2: Oct-Dec, Q3: Jan-Mar, Q4: Apr-Jun
            if quarter == 1:
                return date(year_start, 7, 1), date(year_start, 9, 30)
            if quarter == 2:
                return date(year_start, 10, 1), date(year_start, 12, 31)
            if quarter == 3:
                return date(year_start + 1, 1, 1), date(year_start + 1, 3, 31)
            # default Q4
            return date(year_start + 1, 4, 1), date(year_start + 1, 6, 30)

        period = (filters or {}).get('period')
        date_start = date_end = None
        try:
            if isinstance(period, str) and period:
                # Formats supported: 'fy:2024', 'q1:2024', 'q2:2024', 'q3:2024', 'q4:2024'
                if period.startswith('fy:'):
                    y = int(period.split(':', 1)[1])
                    date_start, date_end = _fy_range(y)
                elif period[0].lower() == 'q' and ':' in period:
                    qpart, ypart = period.split(':', 1)
                    q = int(qpart[1])
                    y = int(ypart)
                    date_start, date_end = _quarter_range(y, q)
        except Exception:
            date_start = date_end = None

        if date_start and date_end:
            # Overlap of [start_date, end_date] with [date_start, date_end]
            overlap = ['&', ('start_date', '<=', date_end), '|', ('end_date', '=', False), ('end_date', '>=', date_start)]
            domain_kpi.extend(overlap)
            domain_prog.extend(overlap)
            domain_div_rel.extend(overlap)

        # Compute strategic (KPI) aggregates for KRAs and Goals regardless of data_type,
        # as these structures are inherently strategic.
        kras_data = []
        kras = self.env['key.result.area'].search([])
        for kra in kras:
            kpi_domain = [('kra_id', '=', kra.id)] + domain_kpi
            kpis = self.env['key.performance.indicator'].search(kpi_domain)
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                kpi_count = len(kpis)
            else:
                # Treat KRA with no KPIs in scope as 0% to avoid inflated averages
                avg_performance = 0.0
                kpi_count = 0
            kras_data.append({
                'name': kra.name,
                'performance': avg_performance,
                'kpi_count': kpi_count,
                'strategic_objective': kra.strategic_objective_id.name if kra.strategic_objective_id else 'No Objective'
            })

        goals_data = []
        strategic_goals = self.env['strategic.goal'].search([])
        for goal in strategic_goals:
            goal_domain = [('kra_id.strategic_objective_id.strategic_goal_id', '=', goal.id)] + domain_kpi
            kpis = self.env['key.performance.indicator'].search(goal_domain)
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                kpi_count = len(kpis)
            else:
                avg_performance = 0.0
                kpi_count = 0
            target_value = getattr(goal, 'target_percentage', 100.0) or 100.0
            goals_data.append({
                'name': goal.name,
                'performance': avg_performance,
                'kpi_count': kpi_count,
                'target': target_value
            })

        # Build top performers and distribution depending on data_type
        data_type = (filters or {}).get('data_type') or 'all'
        top_kpis_data = []
        distribution_data = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}

        def _dist_from_records(records):
            return {
                'excellent': len([r for r in records if (r.achievement_percentage or 0) >= 90]),
                'good': len([r for r in records if 70 <= (r.achievement_percentage or 0) < 90]),
                'fair': len([r for r in records if 50 <= (r.achievement_percentage or 0) < 70]),
                'poor': len([r for r in records if (r.achievement_percentage or 0) < 50]),
            }

        def _safe_avg(values):
            vals = [float(v) for v in values if v is not None]
            return round(sum(vals) / len(vals), 2) if vals else 0.0

        if data_type in ('strategic', 'all'):
            kpi_domain = [('achievement_percentage', '>', 0)] + domain_kpi
            top_strat = self.env['key.performance.indicator'].search(kpi_domain, order='achievement_percentage desc', limit=10)
            top_kpis_data.extend([{
                'name': k.name,
                'performance': k.achievement_percentage,
                'target': k.target_value,
                'current': k.current_value,
                'kra': k.kra_id.name if k.kra_id else 'No KRA',
                'type': 'Strategic KPI'
            } for k in top_strat])
            distribution_data = _dist_from_records(self.env['key.performance.indicator'].search(domain_kpi))

        if data_type in ('programme', 'all'):
            prog_domain = [('achievement_percentage', '>', 0)] + domain_prog
            top_prog = self.env['performance.indicator'].search(prog_domain, order='achievement_percentage desc', limit=10)
            top_kpis_data.extend([{
                'name': p.name,
                'performance': p.achievement_percentage,
                'target': p.target_value,
                'current': p.current_value,
                'kra': p.parent_programme_id.name if p.parent_programme_id else 'No Programme',
                'type': 'Programme KPI'
            } for p in top_prog])
            # Merge distributions by summing bins
            prog_dist = _dist_from_records(self.env['performance.indicator'].search(domain_prog))
            for k in distribution_data:
                distribution_data[k] = (distribution_data.get(k, 0) or 0) + prog_dist.get(k, 0)

        # Sort combined list and cap to 10
        top_kpis_data = sorted(top_kpis_data, key=lambda x: x['performance'] or 0, reverse=True)[:10]

        # Summary numbers (counts)
        filtered_count = 0
        if data_type == 'strategic':
            filtered_count = self.env['key.performance.indicator'].search_count(domain_kpi)
        elif data_type == 'programme':
            filtered_count = self.env['performance.indicator'].search_count(domain_prog)
        else:
            filtered_count = (
                self.env['key.performance.indicator'].search_count(domain_kpi)
                + self.env['performance.indicator'].search_count(domain_prog)
            )

        # Compute averages for gauges including division-programme performance
        strat_recs = self.env['key.performance.indicator'].search(domain_kpi)
        prog_recs = self.env['performance.indicator'].search(domain_prog)
        div_rel_recs = self.env['division.programme.rel'].search(domain_div_rel)

        # KPI-only (treat missing values as 0)
        kpi_only_avg = _safe_avg([(r.achievement_percentage or 0.0) for r in strat_recs] + [(r.achievement_percentage or 0.0) for r in prog_recs])

        # Average KRA performance across all KRAs (0 if none in scope) to avoid inflation
        avg_kra = _safe_avg([k.get('performance') for k in kras_data])

        # Programme average across all programmes in scope (not only those with indicators) to avoid inflation
        programmes_domain = [('active', '=', True)]
        if scope == 'strategic_goal' and entity_id:
            programmes_domain.append(('strategic_objective_ids.strategic_goal_id', '=', entity_id))
        elif scope == 'strategic_objective' and entity_id:
            programmes_domain.append(('strategic_objective_ids', 'in', [entity_id]))
        elif scope == 'programme' and entity_id:
            programmes_domain.append(('id', '=', entity_id))
        elif scope == 'directorate' and entity_id:
            programmes_domain.append(('implementing_directorate_ids', 'in', [entity_id]))
        elif scope == 'division' and entity_id:
            programmes_domain.append(('division_programme_rel_ids.division_id', '=', entity_id))

        # Apply period overlap to programme via its start/end dates if available
        if date_start and date_end:
            programmes_domain.extend(['&', ('start_date', '<=', date_end), '|', ('end_date', '=', False), ('end_date', '>=', date_start)])

        programmes_all = self.env['kcca.programme'].search(programmes_domain)
        avg_prog = _safe_avg([(p.overall_performance or 0.0) for p in programmes_all]) if (data_type in ('programme', 'all')) else 0.0

        avg_div_prog = _safe_avg([r.performance_score for r in div_rel_recs])

        # Blended overall: average of the three macro-aggregates to keep semantics consistent with unfiltered endpoint
        components = []
        if data_type in ('strategic', 'all'):
            components.append(kpi_only_avg)
        if data_type in ('programme', 'all'):
            components.append(avg_prog)
        # Always consider division-programme component for 'all' or when filtering across entities including divisions/directorates
        if data_type == 'all' or scope in ('directorate', 'division', 'organization'):
            components.append(avg_div_prog)
        avg_performance = _safe_avg(components)

        # No fallback inflation: keep KPI-only average as-is to avoid overstating progress

        return {
            'kras_performance': kras_data,
            'goals_performance': goals_data,
            'top_kpis': top_kpis_data,
            'distribution': distribution_data,
            'filters_applied': filters,
            'summary': {
                'filtered_kpis': filtered_count,
                'total_goals': len(strategic_goals),
                'total_kras': len(kras),
                # Added core averages used by gauges
                'avg_performance': avg_performance,
                'kpi_only_performance': kpi_only_avg,
                'avg_kpi_performance': kpi_only_avg,
                'avg_kra_performance': avg_kra,
                'avg_programme_performance': avg_prog,
                'avg_division_programme_performance': avg_div_prog,
                'avg_budget_utilization': _safe_avg([r.budget_utilization for r in div_rel_recs]),
            }
        }

    @api.model
    def get_period_options(self):
        """Return configurable FY/Q options for the 5-year strategic plan.

        Reads plan start year and span from config parameters and builds:
        [{ key: 'fy:2024', label: 'FY 2024/25' }, { key: 'q1:2024', label: 'Q1 2024/25' }, ...]
        """
        Param = self.env['ir.config_parameter'].sudo()
        try:
            start_year = int(Param.get_param('robust_pmis.plan_start_year') or 2024)
        except Exception:
            start_year = 2024
        try:
            years = int(Param.get_param('robust_pmis.plan_years') or 5)
        except Exception:
            years = 5

        def _fy_label(y):
            return f"FY {y}/{str((y + 1) % 100).zfill(2)}"

        options = []
        for y in range(start_year, start_year + years):
            options.append({'key': f'fy:{y}', 'label': _fy_label(y)})
            options.append({'key': f'q1:{y}', 'label': f'Q1 {_fy_label(y)}'})
            options.append({'key': f'q2:{y}', 'label': f'Q2 {_fy_label(y)}'})
            options.append({'key': f'q3:{y}', 'label': f'Q3 {_fy_label(y)}'})
            options.append({'key': f'q4:{y}', 'label': f'Q4 {_fy_label(y)}'})
        return options

    def get_dashboard_data(self):
        """Return JSON data for dashboard charts"""
        self.ensure_one()
        
        def _safe_avg(values):
            vals = [float(v) for v in values if v is not None]
            return round(sum(vals) / len(vals), 2) if vals else 0.0

        # KRA Performance data
        kras_data = []
        kras = self.env['key.result.area'].search([])

        for kra in kras:
            kpis = self.env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                kpi_count = len(kpis)
            else:
                avg_performance = 0.0
                kpi_count = 0
            kras_data.append({
                'name': kra.name,
                'performance': avg_performance,
                'kpi_count': kpi_count,
                'strategic_objective': kra.strategic_objective_id.name if kra.strategic_objective_id else 'No Objective'
            })

        # KPI Performance by Strategic Goal
        goals_data = []
        strategic_goals = self.env['strategic.goal'].search([])

        for goal in strategic_goals:
            kpis = self.env['key.performance.indicator'].search([
                ('kra_id.strategic_objective_id.strategic_goal_id', '=', goal.id)
            ])
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                kpi_count = len(kpis)
            else:
                avg_performance = 0.0
                kpi_count = 0

            # Get target values if they exist, otherwise set to 100 (100%)
            target_value = 100.0  # Default target is 100%
            if hasattr(goal, 'target_percentage'):
                target_value = goal.target_percentage

            goals_data.append({
                'name': goal.name,
                'performance': avg_performance,
                'kpi_count': kpi_count,
                'target': target_value
            })

        # Top performing KPIs - include both strategic KPIs and programme indicators
        top_strategic_kpis = self.env['key.performance.indicator'].search([
            ('achievement_percentage', '>', 0)
        ], order='achievement_percentage desc', limit=5)

        top_programme_kpis = self.env['performance.indicator'].search([
            ('achievement_percentage', '>', 0)
        ], order='achievement_percentage desc', limit=5)

        top_kpis_data = []

        # Add strategic KPIs
        for kpi in top_strategic_kpis:
            top_kpis_data.append({
                'name': kpi.name,
                'performance': kpi.achievement_percentage,
                'target': kpi.target_value,
                'current': kpi.current_value,
                'kra': kpi.kra_id.name if kpi.kra_id else 'No KRA',
                'type': 'Strategic KPI'
            })

        # Add programme indicators
        for kpi in top_programme_kpis:
            top_kpis_data.append({
                'name': kpi.name,
                'performance': kpi.achievement_percentage,
                'target': kpi.target_value,
                'current': kpi.current_value,
                'kra': kpi.parent_programme_id.name if kpi.parent_programme_id else 'No Programme',
                'type': 'Programme KPI'
            })

        # Sort combined list by performance
        top_kpis_data = sorted(top_kpis_data, key=lambda x: x['performance'], reverse=True)[:10]

        # Performance distribution - include both types (treat None as 0 to reflect no progress)
        strategic_kpis = self.env['key.performance.indicator'].search([])
        programme_kpis = self.env['performance.indicator'].search([])
        div_prog_rels = self.env['division.programme.rel'].search([('active', '=', True)])

        all_achievements = []
        for kpi in strategic_kpis:
            val = kpi.achievement_percentage if kpi.achievement_percentage is not None else 0.0
            all_achievements.append(val)
        for kpi in programme_kpis:
            val = kpi.achievement_percentage if kpi.achievement_percentage is not None else 0.0
            all_achievements.append(val)

        distribution_data = {
            'excellent': len([a for a in all_achievements if a >= 90]),
            'good': len([a for a in all_achievements if 70 <= a < 90]),
            'fair': len([a for a in all_achievements if 50 <= a < 70]),
            'poor': len([a for a in all_achievements if a < 50])
        }

        # Directorate contributions against targets (KPI achievement and Programme progress)
        directorate_contributions = []
        directorates = self.env['kcca.directorate'].search([])
        for d in directorates:
            dir_kpis = self.env['key.performance.indicator'].search([('directorate_id', '=', d.id)])
            kpi_ach = sum(k.achievement_percentage or 0.0 for k in dir_kpis) / len(dir_kpis) if dir_kpis else 0.0
            progs = d.all_programme_ids
            prog_ach = sum(p.overall_performance or 0.0 for p in progs) / len(progs) if progs else 0.0
            # Blend with division-programme performance for divisions under this directorate
            rels = self.env['division.programme.rel'].search([('division_id.directorate_id', '=', d.id)])
            div_rel_ach = sum(r.performance_score or 0.0 for r in rels) / len(rels) if rels else 0.0
            blended_prog = (prog_ach + div_rel_ach) / 2.0 if (prog_ach or div_rel_ach) else 0.0
            on_target_kpis = len([k for k in dir_kpis if (k.achievement_percentage or 0.0) >= 100])
            directorate_contributions.append({
                'name': d.name,
                'kpi_achievement': round(kpi_ach, 2),
                'programme_progress': round(blended_prog, 2),
                'on_target_kpis': on_target_kpis,
                'total_kpis': len(dir_kpis),
            })

        # Division contributions against targets (Programme progress and Indicator achievement)
        division_contributions = []
        divisions = self.env['kcca.division'].search([])
        for v in divisions:
            all_programmes = (v.programme_ids | v.implementing_programme_ids)
            prog_ach = sum(p.overall_performance or 0.0 for p in all_programmes) / len(all_programmes) if all_programmes else 0.0
            # Division-programme relationship performance for this division
            rels = self.env['division.programme.rel'].search([('division_id', '=', v.id)])
            div_rel_ach = sum(r.performance_score or 0.0 for r in rels) / len(rels) if rels else 0.0
            blended_prog = (prog_ach + div_rel_ach) / 2.0 if (prog_ach or div_rel_ach) else 0.0
            indicators = all_programmes.mapped('performance_indicator_ids')
            ind_ach = sum(pi.achievement_percentage or 0.0 for pi in indicators) / len(indicators) if indicators else 0.0
            on_target_inds = len([pi for pi in indicators if (pi.achievement_percentage or 0.0) >= 100])
            division_contributions.append({
                'name': v.name,
                'programme_progress': round(blended_prog, 2),
                'indicator_achievement': round(ind_ach, 2),
                'on_target_indicators': on_target_inds,
                'total_indicators': len(indicators),
            })

        # Global averages for gauges (conservative, bounded)
        # Treat missing values as 0 to avoid overstating progress
        avg_kpi_performance = _safe_avg([(k.achievement_percentage or 0.0) for k in strategic_kpis] + [(p.achievement_percentage or 0.0) for p in programme_kpis])
        avg_programme_performance = _safe_avg([(p.overall_performance or 0.0) for p in self.env['kcca.programme'].search([])])
        avg_division_programme_performance = _safe_avg([r.performance_score for r in div_prog_rels])
        avg_overall = _safe_avg([avg_kpi_performance, avg_programme_performance, avg_division_programme_performance])
        # Clamp all displayed values to 0..100
        def _clamp01(x):
            try:
                v = float(x)
            except Exception:
                return 0.0
            return 0.0 if v < 0 else (100.0 if v > 100 else v)
        avg_kpi_performance = _clamp01(avg_kpi_performance)
        avg_programme_performance = _clamp01(avg_programme_performance)
        avg_division_programme_performance = _clamp01(avg_division_programme_performance)
        avg_overall = _clamp01(avg_overall)
        # No fallback inflation: keep KPI-only average as-is to avoid overstating progress

        return {
            'kras_performance': kras_data,
            'goals_performance': goals_data,
            'top_kpis': top_kpis_data,
            'distribution': distribution_data,
            'directorate_contributions': directorate_contributions,
            'division_contributions': division_contributions,
            'summary': {
                'total_goals': self.total_goals,
                'total_kras': self.total_kras,
                'avg_kra_performance': self.avg_kra_performance,
                'total_kpis': self.total_kpis,  # Now includes both types
                'avg_performance': avg_overall,  # Blended KPI + Programme + Division-Programme
                'kpi_only_performance': avg_kpi_performance,  # Explicit KPI-only average for UI mapping
                'avg_kpi_performance': avg_kpi_performance,
                'avg_programme_performance': avg_programme_performance,
                'avg_division_programme_performance': avg_division_programme_performance,
                'avg_budget_utilization': _safe_avg([r.budget_utilization for r in div_prog_rels]),
                'total_programmes': self.total_programmes,
                'total_directorates': self.total_directorates,
                'total_divisions': self.total_divisions,
                # Add breakdown
                'strategic_kpis_count': len(strategic_kpis),
                'programme_kpis_count': len(programme_kpis)
            }
        }
    
    @api.model
    def refresh_metrics(self, ids=None):
        """Refresh all dashboard metrics - called by data loading"""
        if ids:
            dashboard_records = self.browse(ids)
        else:
            dashboard_records = self.search([])
        for dashboard in dashboard_records:
            # Force recomputation of all computed fields
            dashboard._compute_dashboard_metrics()
        return True
    
    def get_realtime_metrics(self):
        """Get real-time metrics without using computed fields"""
        # Get counts directly from database
        strategic_goals = self.env['strategic.goal'].search([])
        kras = self.env['key.result.area'].search([])
        strategic_kpis = self.env['key.performance.indicator'].search([])
        programme_indicators = self.env['performance.indicator'].search([])
        programmes = self.env['kcca.programme'].search([])
        directorates = self.env['kcca.directorate'].search([])
        divisions = self.env['kcca.division'].search([])
        
        # Calculate KRA performance
        avg_kra_performance = 0.0
        if kras:
            kra_performances = []
            for kra in kras:
                kra_kpis = self.env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                if kra_kpis:
                    avg_kra_perf = sum(kpi.achievement_percentage or 0.0 for kpi in kra_kpis) / len(kra_kpis)
                    kra_performances.append(avg_kra_perf)
            
            if kra_performances:
                avg_kra_performance = sum(kra_performances) / len(kra_performances)
        
        # Calculate KPI performance
        avg_kpi_performance = 0.0
        if strategic_kpis or programme_indicators:
            all_kpi_values = [k.achievement_percentage or 0.0 for k in strategic_kpis] + [p.achievement_percentage or 0.0 for p in programme_indicators]
            if all_kpi_values:
                avg_kpi_performance = sum(all_kpi_values) / len(all_kpi_values)
        
        # Calculate programme performance
        avg_programme_performance = 0.0
        if programmes:
            programme_performances = []
            for prog in programmes:
                if hasattr(prog, 'overall_performance') and prog.overall_performance:
                    programme_performances.append(prog.overall_performance)
            
            if programme_performances:
                avg_programme_performance = sum(programme_performances) / len(programme_performances)
        
        return {
            'total_goals': len(strategic_goals),
            'total_strategic_goals': len(strategic_goals),
            'total_kras': len(kras),
            'total_kpis': len(strategic_kpis) + len(programme_indicators),
            'total_programmes': len(programmes),
            'total_directorates': len(directorates),
            'total_divisions': len(divisions),
            'avg_kra_performance': avg_kra_performance,
            'avg_kpi_performance': avg_kpi_performance,
            'kpi_only_performance': avg_kpi_performance,
            'avg_programme_performance': avg_programme_performance,
            'avg_directorate_performance': 0.0,  # Can be enhanced later
            'avg_division_performance': 0.0,     # Can be enhanced later
        }
    
    def action_view_all_kpis(self):
        """Return action to view all KPIs (strategic + programme indicators)"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'All KPIs (Strategic + Programme Indicators)',
            'res_model': 'key.performance.indicator',
            'view_mode': 'tree,form,kanban',
            'target': 'current',
            'context': {'create': False},
        }
    
    def action_view_strategic_kpis(self):
        """Return action to view only strategic KPIs"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Strategic KPIs',
            'res_model': 'key.performance.indicator',
            'view_mode': 'tree,form,kanban',
            'domain': [('classification_level', '=', 'kpi'), ('parent_type', '=', 'kra')],
            'target': 'current',
            'context': {'create': False},
        }
    
    def action_view_programme_kpis(self):
        """Return action to view programme-level KPIs (Performance Indicators)"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Programme KPIs (Performance Indicators)',
            'res_model': 'performance.indicator',
            'view_mode': 'tree,form,kanban',
            'target': 'current',
            'context': {'create': False},
        }
