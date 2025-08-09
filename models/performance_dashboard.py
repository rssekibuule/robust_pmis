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
        
        # Set basic counts
        self.total_goals = len(strategic_goals)  # Legacy field
        self.total_strategic_goals = len(strategic_goals)
        self.total_kras = len(kras)
        self.total_kpis = total_kpi_count  # Now includes both types
        self.total_programmes = len(programmes)
        self.total_directorates = len(directorates)
        self.total_divisions = len(divisions)
        
        # Calculate average KRA performance based on linked KPIs
        if kras:
            kra_performances = []
            for kra in kras:
                kra_kpis = self.env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                if kra_kpis:
                    avg_kra_perf = sum(kpi.achievement_percentage or 0.0 for kpi in kra_kpis) / len(kra_kpis)
                    kra_performances.append(avg_kra_perf)
            
            if kra_performances:
                self.avg_kra_performance = sum(kra_performances) / len(kra_performances)
            else:
                self.avg_kra_performance = 0.0
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
            
            # Programmes
            programmes = self.env['kcca.programme'].search([])
            rec.total_programmes = len(programmes)
            
            if programmes:
                # Use a safer approach for programme performance
                programme_performances = []
                for prog in programmes:
                    if hasattr(prog, 'overall_performance') and prog.overall_performance:
                        programme_performances.append(prog.overall_performance)
                
                if programme_performances:
                    rec.avg_programme_performance = sum(programme_performances) / len(programme_performances)
                else:
                    rec.avg_programme_performance = 0.0
            else:
                rec.avg_programme_performance = 0.0
            
            # Directorates
            directorates = self.env['kcca.directorate'].search([])
            rec.total_directorates = len(directorates)
            
            if directorates:
                # Use a safer approach for directorate performance
                directorate_performances = []
                for dir in directorates:
                    if hasattr(dir, 'overall_performance') and dir.overall_performance:
                        directorate_performances.append(dir.overall_performance)
                
                if directorate_performances:
                    rec.avg_directorate_performance = sum(directorate_performances) / len(directorate_performances)
                else:
                    rec.avg_directorate_performance = 0.0
            else:
                rec.avg_directorate_performance = 0.0
            
            # Divisions
            divisions = self.env['kcca.division'].search([])
            rec.total_divisions = len(divisions)
            
            if divisions:
                # Use a safer approach for division performance
                division_performances = []
                for div in divisions:
                    if hasattr(div, 'overall_performance') and div.overall_performance:
                        division_performances.append(div.overall_performance)
                
                if division_performances:
                    rec.avg_division_performance = sum(division_performances) / len(division_performances)
                else:
                    rec.avg_division_performance = 0.0
            else:
                rec.avg_division_performance = 0.0
    
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

        # Performance filter
        perf = (filters or {}).get('performance')
        if perf and perf != 'all':
            if perf == 'excellent':
                domain_kpi.append(('achievement_percentage', '>=', 90))
                domain_prog.append(('achievement_percentage', '>=', 90))
            elif perf == 'good':
                rng = [('achievement_percentage', '>=', 70), ('achievement_percentage', '<', 90)]
                domain_kpi.extend(rng)
                domain_prog.extend(rng)
            elif perf == 'fair':
                rng = [('achievement_percentage', '>=', 50), ('achievement_percentage', '<', 70)]
                domain_kpi.extend(rng)
                domain_prog.extend(rng)
            elif perf == 'poor':
                domain_kpi.append(('achievement_percentage', '<', 50))
                domain_prog.append(('achievement_percentage', '<', 50))

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
            elif scope == 'strategic_objective':
                domain_kpi.append(('kra_id.strategic_objective_id', '=', entity_id))
                domain_prog.append(('parent_programme_id.strategic_objective_ids', 'in', [entity_id]))
            elif scope == 'programme':
                # Strategic KPIs via Objective -> Programmes linkage
                domain_kpi.append(('kra_id.strategic_objective_id.programme_ids', 'in', [entity_id]))
                domain_prog.append(('parent_programme_id', '=', entity_id))
            elif scope == 'directorate':
                # Strategic KPIs via Programmes implemented by this directorate
                domain_kpi.append(('kra_id.strategic_objective_id.programme_ids.implementing_directorate_ids', 'in', [entity_id]))
                domain_prog.append(('parent_programme_id.implementing_directorate_ids', 'in', [entity_id]))
            elif scope == 'division':
                # Strategic KPIs via Programmes implemented by this division
                domain_kpi.append(('kra_id.strategic_objective_id.programme_ids.division_programme_rel_ids.division_id', '=', entity_id))
                # Use division relationships table via programme
                domain_prog.append(('parent_programme_id.division_programme_rel_ids.division_id', '=', entity_id))

        # Period filter placeholder (FY/Q) – can be refined when date baselines are standardized
        # We intentionally do not filter by date yet to avoid hiding data inadvertently.

        # Compute strategic (KPI) aggregates for KRAs and Goals regardless of data_type,
        # as these structures are inherently strategic.
        kras_data = []
        kras = self.env['key.result.area'].search([])
        for kra in kras:
            kpi_domain = [('kra_id', '=', kra.id)] + domain_kpi
            kpis = self.env['key.performance.indicator'].search(kpi_domain)
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                kras_data.append({
                    'name': kra.name,
                    'performance': avg_performance,
                    'kpi_count': len(kpis),
                    'strategic_objective': kra.strategic_objective_id.name if kra.strategic_objective_id else 'No Objective'
                })

        goals_data = []
        strategic_goals = self.env['strategic.goal'].search([])
        for goal in strategic_goals:
            goal_domain = [('kra_id.strategic_objective_id.strategic_goal_id', '=', goal.id)] + domain_kpi
            kpis = self.env['key.performance.indicator'].search(goal_domain)
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                target_value = getattr(goal, 'target_percentage', 100.0) or 100.0
                goals_data.append({
                    'name': goal.name,
                    'performance': avg_performance,
                    'kpi_count': len(kpis),
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

        # Compute averages for gauges to avoid blanks when using ORM fallback (no controller merge)
        strat_recs = self.env['key.performance.indicator'].search(domain_kpi)
        prog_recs = self.env['performance.indicator'].search(domain_prog)

        if data_type == 'strategic':
            avg_performance = _safe_avg([r.achievement_percentage for r in strat_recs])
        elif data_type == 'programme':
            avg_performance = _safe_avg([r.achievement_percentage for r in prog_recs])
        else:
            avg_performance = _safe_avg(
                [r.achievement_percentage for r in strat_recs]
                + [r.achievement_percentage for r in prog_recs]
            )

        avg_kra = _safe_avg([k.get('performance') for k in kras_data])

        avg_prog = 0.0
        if data_type in ('programme', 'all'):
            programmes = prog_recs.mapped('parent_programme_id') if prog_recs else self.env['kcca.programme']
            if programmes:
                avg_prog = _safe_avg([p.overall_performance for p in programmes])

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
                'avg_kra_performance': avg_kra,
                'avg_programme_performance': avg_prog,
            }
        }

    def get_dashboard_data(self):
        """Return JSON data for dashboard charts"""
        self.ensure_one()
        
        # KRA Performance data
        kras_data = []
        kras = self.env['key.result.area'].search([])
        
        for kra in kras:
            kpis = self.env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
            if kpis:
                avg_performance = sum(kpi.achievement_percentage or 0.0 for kpi in kpis) / len(kpis)
                kras_data.append({
                    'name': kra.name,
                    'performance': avg_performance,
                    'kpi_count': len(kpis),
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
                
                # Get target values if they exist, otherwise set to 100 (100%)
                target_value = 100.0  # Default target is 100%
                if hasattr(goal, 'target_percentage'):
                    target_value = goal.target_percentage
                
                goals_data.append({
                    'name': goal.name,
                    'performance': avg_performance,
                    'kpi_count': len(kpis),
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
        
        # Performance distribution - include both types
        strategic_kpis = self.env['key.performance.indicator'].search([])
        programme_kpis = self.env['performance.indicator'].search([])
        
        all_achievements = []
        for kpi in strategic_kpis:
            if kpi.achievement_percentage:
                all_achievements.append(kpi.achievement_percentage)
        for kpi in programme_kpis:
            if kpi.achievement_percentage:
                all_achievements.append(kpi.achievement_percentage)
        
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
            on_target_kpis = len([k for k in dir_kpis if (k.achievement_percentage or 0.0) >= 100])
            directorate_contributions.append({
                'name': d.name,
                'kpi_achievement': round(kpi_ach, 2),
                'programme_progress': round(prog_ach, 2),
                'on_target_kpis': on_target_kpis,
                'total_kpis': len(dir_kpis),
            })

        # Division contributions against targets (Programme progress and Indicator achievement)
        division_contributions = []
        divisions = self.env['kcca.division'].search([])
        for v in divisions:
            all_programmes = (v.programme_ids | v.implementing_programme_ids)
            prog_ach = sum(p.overall_performance or 0.0 for p in all_programmes) / len(all_programmes) if all_programmes else 0.0
            indicators = all_programmes.mapped('performance_indicator_ids')
            ind_ach = sum(pi.achievement_percentage or 0.0 for pi in indicators) / len(indicators) if indicators else 0.0
            on_target_inds = len([pi for pi in indicators if (pi.achievement_percentage or 0.0) >= 100])
            division_contributions.append({
                'name': v.name,
                'programme_progress': round(prog_ach, 2),
                'indicator_achievement': round(ind_ach, 2),
                'on_target_indicators': on_target_inds,
                'total_indicators': len(indicators),
            })

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
                'avg_performance': self.avg_kpi_performance,  # Now includes both types
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
        kpis = self.env['key.performance.indicator'].search([])
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
        if kpis:
            total_achievement = sum(kpi.achievement_percentage or 0.0 for kpi in kpis)
            avg_kpi_performance = total_achievement / len(kpis)
        
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
            'total_kpis': len(kpis),
            'total_programmes': len(programmes),
            'total_directorates': len(directorates),
            'total_divisions': len(divisions),
            'avg_kra_performance': avg_kra_performance,
            'avg_kpi_performance': avg_kpi_performance,
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
