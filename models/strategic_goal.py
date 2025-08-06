# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StrategicGoal(models.Model):
    _name = 'strategic.goal'
    _description = 'Strategic Goal'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Strategic Goal',
        required=True,
        tracking=True,
        help="Name of the strategic goal"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the strategic goal"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering strategic goals"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    color = fields.Char(
        string='Color',
        help="Color for kanban view"
    )
    
    # Relationships
    strategic_objective_ids = fields.One2many(
        'strategic.objective',
        'strategic_goal_id',
        string='Strategic Objectives',
        help="Strategic objectives under this goal"
    )
    
    kra_ids = fields.One2many(
        'key.result.area',
        'strategic_goal_id',
        string='Key Result Areas',
        help="Direct KRAs under this strategic goal"
    )
    
    # Computed fields
    objective_count = fields.Integer(
        string='Objectives Count',
        compute='_compute_counts',
        store=True
    )
    
    kra_count = fields.Integer(
        string='KRAs Count',
        compute='_compute_counts',
        store=True
    )
    
    kpi_count = fields.Integer(
        string='KPIs Count',
        compute='_compute_counts',
        store=True
    )
    
    progress = fields.Float(
        string='Overall Progress (%)',
        compute='_compute_progress',
        store=True,
        help="Overall progress based on KPIs achievement"
    )

    # Smart card computed fields
    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_smart_card_counts',
        help="Total programmes contributing to this strategic goal"
    )

    directorate_count = fields.Integer(
        string='Directorates Count',
        compute='_compute_smart_card_counts',
        help="Total directorates involved in this strategic goal"
    )

    division_count = fields.Integer(
        string='Divisions Count',
        compute='_compute_smart_card_counts',
        help="Total divisions involved in this strategic goal"
    )

    programme_ids = fields.Many2many(
        'kcca.programme',
        string='Related Programmes',
        compute='_compute_related_entities',
        help="All programmes contributing to this strategic goal"
    )

    directorate_ids = fields.Many2many(
        'kcca.directorate',
        string='Related Directorates',
        compute='_compute_related_entities',
        help="All directorates involved in this strategic goal"
    )

    division_ids = fields.Many2many(
        'kcca.division',
        string='Related Divisions',
        compute='_compute_related_entities',
        help="All divisions involved in this strategic goal"
    )
    # URLs for dashboard actions
    url_goals = fields.Char(
        string='Goals Dashboard URL',
        compute='_compute_urls',
        readonly=True
    )
    url_programmes = fields.Char(
        string='Programmes Dashboard URL',
        compute='_compute_urls',
        readonly=True
    )
    
    @api.depends('strategic_objective_ids', 'kra_ids', 'kra_ids.kpi_ids')
    def _compute_counts(self):
        for record in self:
            record.objective_count = len(record.strategic_objective_ids)
            
            # Count direct KRAs and KRAs from objectives
            direct_kras = record.kra_ids
            objective_kras = record.strategic_objective_ids.mapped('kra_ids')
            all_kras = direct_kras | objective_kras
            record.kra_count = len(all_kras)
            
            # Count all KPIs from all KRAs
            all_kpis = all_kras.mapped('kpi_ids')
            record.kpi_count = len(all_kpis)
    
    @api.depends('kra_ids.progress', 'strategic_objective_ids.kra_ids.progress')
    def _compute_progress(self):
        for record in self:
            # Get all KRAs (direct and from objectives)
            direct_kras = record.kra_ids
            objective_kras = record.strategic_objective_ids.mapped('kra_ids')
            all_kras = direct_kras | objective_kras

            if all_kras:
                total_progress = sum(kra.progress for kra in all_kras)
                record.progress = total_progress / len(all_kras)
            else:
                record.progress = 0.0

    @api.depends('strategic_objective_ids.programme_ids',
                 'strategic_objective_ids.programme_ids.implementing_directorate_ids',
                 'strategic_objective_ids.programme_ids.implementing_division_ids',
                 'strategic_objective_ids.programme_ids.directorate_id',
                 'strategic_objective_ids.programme_ids.division_id')
    def _compute_smart_card_counts(self):
        for record in self:
            # Get all programmes from strategic objectives
            programmes = record.strategic_objective_ids.mapped('programme_ids')
            record.programme_count = len(programmes)

            # Get all directorates implementing these programmes
            directorates = self.env['kcca.directorate']
            divisions = self.env['kcca.division']
            
            if programmes:
                # Get directorates from many-to-many relationships
                m2m_directorates = programmes.mapped('implementing_directorate_ids')

                # Get directorates from programme-directorate relationships
                prog_dir_rels = self.env['programme.directorate.rel'].search([
                    ('programme_id', 'in', programmes.ids)
                ])
                rel_directorates = prog_dir_rels.mapped('directorate_id')

                # Also get directorates from legacy single directorate field
                legacy_directorates = programmes.mapped('directorate_id').filtered(lambda x: x)

                # Combine all directorates
                directorates = m2m_directorates | rel_directorates | legacy_directorates

                # Compute divisions count (many2many and legacy field)
                div_m2m = programmes.mapped('implementing_division_ids')
                
                # Get divisions from division-programme relationships
                div_prog_rels = self.env['division.programme.rel'].search([
                    ('programme_id', 'in', programmes.ids)
                ])
                rel_divisions = div_prog_rels.mapped('division_id')
                
                legacy_divs = programmes.mapped('division_id').filtered(lambda d: d)
                divisions = div_m2m | rel_divisions | legacy_divs

            record.directorate_count = len(directorates)
            record.division_count = len(divisions)

    @api.depends()
    def _compute_urls(self):
        """
        Compute URLs for strategic goals and programmes dashboards.
        """
        base = '/web#menu_id=%s&action=%s'
        for rec in self:
            try:
                goal_menu = self.env.ref('robust_pmis.menu_strategic_goal').id
                goal_action = self.env.ref('robust_pmis.action_strategic_goal').id
                prog_menu = self.env.ref('robust_pmis.menu_kcca_programme').id
                prog_action = self.env.ref('robust_pmis.action_kcca_programme').id
                rec.url_goals = base % (goal_menu, goal_action)
                rec.url_programmes = base % (prog_menu, prog_action)
            except Exception:
                rec.url_goals = ''
                rec.url_programmes = ''

    @api.depends('strategic_objective_ids.programme_ids')
    def _compute_related_entities(self):
        for record in self:
            # Get all programmes from strategic objectives
            programmes = record.strategic_objective_ids.mapped('programme_ids')
            record.programme_ids = programmes

            # Get all directorates implementing these programmes
            directorates = self.env['kcca.directorate']
            if programmes:
                prog_dir_rels = self.env['programme.directorate.rel'].search([
                    ('programme_id', 'in', programmes.ids)
                ])
                directorates = prog_dir_rels.mapped('directorate_id')
            record.directorate_ids = directorates

            # Get all divisions implementing these programmes
            divisions = self.env['kcca.division']
            if programmes:
                div_prog_rels = self.env['division.programme.rel'].search([
                    ('programme_id', 'in', programmes.ids)
                ])
                divisions = div_prog_rels.mapped('division_id')
            record.division_ids = divisions
    
    def action_view_objectives(self):
        """Action to view strategic objectives"""
        action = self.env.ref('robust_pmis.action_strategic_objective').read()[0]
        action['domain'] = [('strategic_goal_id', '=', self.id)]
        action['context'] = {'default_strategic_goal_id': self.id}
        return action
    
    def action_view_kras(self):
        """Action to view all KRAs (direct and from objectives)"""
        direct_kras = self.kra_ids
        objective_kras = self.strategic_objective_ids.mapped('kra_ids')
        all_kras = direct_kras | objective_kras
        
        action = self.env.ref('robust_pmis.action_key_result_area').read()[0]
        action['domain'] = [('id', 'in', all_kras.ids)]
        return action
    
    def action_view_kpis(self):
        """Action to view all KPIs"""
        direct_kras = self.kra_ids
        objective_kras = self.strategic_objective_ids.mapped('kra_ids')
        all_kras = direct_kras | objective_kras
        all_kpis = all_kras.mapped('kpi_ids')

        action = self.env.ref('robust_pmis.action_key_performance_indicator').read()[0]
        action['domain'] = [('id', 'in', all_kpis.ids)]
        return action

    def action_view_programmes(self):
        """Action to view related programmes"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')

        action = self.env.ref('robust_pmis.action_kcca_programme').read()[0]
        action['domain'] = [('id', 'in', programmes.ids)]
        action['context'] = {'default_strategic_goal_id': self.id}
        return action

    def action_view_directorates(self):
        """Action to view related directorates"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')
        directorates = self.env['kcca.directorate']

        if programmes:
            prog_dir_rels = self.env['programme.directorate.rel'].search([
                ('programme_id', 'in', programmes.ids)
            ])
            directorates = prog_dir_rels.mapped('directorate_id')

        action = self.env.ref('robust_pmis.action_kcca_directorate').read()[0]
        action['domain'] = [('id', 'in', directorates.ids)]
        return action

    def action_view_divisions(self):
        """Action to view related divisions"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')
        divisions = self.env['kcca.division']

        if programmes:
            div_prog_rels = self.env['division.programme.rel'].search([
                ('programme_id', 'in', programmes.ids)
            ])
            divisions = div_prog_rels.mapped('division_id')

        action = self.env.ref('robust_pmis.action_kcca_division').read()[0]
        action['domain'] = [('id', 'in', divisions.ids)]
        return action

    def force_recompute_counts(self):
        """Force recomputation of all counts - for debugging"""
        self._compute_counts()
        self._compute_smart_card_counts()
        self._compute_related_entities()
        return True

    def recompute_all_counts(self):
        """Force recomputation of all counts"""
        self._compute_counts()
        self._compute_smart_card_counts()
        self._compute_progress()
        self._compute_related_entities()
        return True

    @api.model
    def recompute_all_strategic_goals(self):
        """Recompute all strategic goals counts"""
        goals = self.search([])
        for goal in goals:
            goal.recompute_all_counts()
        return True

    # Executive Dashboard Action Methods
    def action_view_programmes(self):
        """Action to view all programmes contributing to this strategic goal"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')
        action = self.env.ref('robust_pmis.action_kcca_programme').read()[0]
        action['domain'] = [('id', 'in', programmes.ids)]
        action['context'] = {'default_strategic_goal_id': self.id}
        return action

    def action_view_directorates(self):
        """Action to view all directorates implementing programmes for this goal"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')
        directorates = programmes.mapped('implementing_directorate_ids')
        action = self.env.ref('robust_pmis.action_kcca_directorate').read()[0]
        action['domain'] = [('id', 'in', directorates.ids)]
        return action

    def action_view_divisions(self):
        """Action to view all divisions involved in this strategic goal"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')
        divisions = programmes.mapped('implementing_division_ids')
        action = self.env.ref('robust_pmis.action_kcca_division').read()[0]
        action['domain'] = [('id', 'in', divisions.ids)]
        return action

    def action_performance_report(self):
        """Generate comprehensive performance report"""
        return {
            'type': 'ir.actions.report',
            'report_name': 'robust_pmis.strategic_goal_performance_report',
            'report_type': 'qweb-pdf',
            'data': {'goal_id': self.id},
            'context': self.env.context,
        }

    def action_view_alerts(self):
        """View performance alerts related to this strategic goal"""
        action = self.env.ref('robust_pmis.action_performance_alert').read()[0]
        action['domain'] = [('strategic_goal_id', '=', self.id)]
        action['context'] = {'default_strategic_goal_id': self.id}
        return action

    def action_financial_overview(self):
        """View financial overview for this strategic goal"""
        programmes = self.strategic_objective_ids.mapped('programme_ids')
        action = self.env.ref('robust_pmis.action_programme_budget').read()[0]
        action['domain'] = [('programme_id', 'in', programmes.ids)]
        return action

    def action_analytics_dashboard(self):
        """Open analytics dashboard for this strategic goal"""
        action = self.env.ref('robust_pmis.action_performance_analytics').read()[0]
        action['domain'] = [('strategic_goal_id', '=', self.id)]
        action['context'] = {'default_strategic_goal_id': self.id}
        return action
