# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KeyResultArea(models.Model):
    _name = 'key.result.area'
    _description = 'Key Result Area (KRA)'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        # Enforce uniqueness of KRA names within each parent scope
        ('kra_unique_by_objective', 'unique(strategic_objective_id, name)',
         'KRA names must be unique within each Strategic Objective.'),
        ('kra_unique_by_goal', 'unique(strategic_goal_id, name)',
         'KRA names must be unique within each Strategic Goal (when not under an Objective).'),
    ]

    name = fields.Char(
        string='Key Result Area',
        required=True,
        tracking=True,
        help="Name of the key result area"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the KRA"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering KRAs"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships - KRA can be linked directly to Strategic Goal OR to Strategic Objective
    strategic_goal_id = fields.Many2one(
        'strategic.goal',
        string='Strategic Goal',
        ondelete='cascade',
        tracking=True,
        help="Direct link to strategic goal (if not under an objective)"
    )
    
    strategic_objective_id = fields.Many2one(
        'strategic.objective',
        string='Strategic Objective',
        ondelete='cascade',
        tracking=True,
        help="Parent strategic objective (if under an objective)"
    )
    
    kpi_ids = fields.One2many(
        'key.performance.indicator',
        'kra_id',
        string='Key Performance Indicators',
        help="KPIs under this KRA"
    )
    
    # Computed fields
    kpi_count = fields.Integer(
        string='KPIs Count',
        compute='_compute_counts',
        store=True
    )
    
    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress',
        store=True,
        help="Progress based on KPIs achievement"
    )
    
    parent_goal_id = fields.Many2one(
        'strategic.goal',
        string='Parent Strategic Goal',
        compute='_compute_parent_goal',
        store=True,
        help="The ultimate parent strategic goal"
    )
    
    @api.depends('kpi_ids')
    def _compute_counts(self):
        for record in self:
            record.kpi_count = len(record.kpi_ids)
    
    @api.depends('kpi_ids.achievement_percentage')
    def _compute_progress(self):
        for record in self:
            if record.kpi_ids:
                total_achievement = sum(kpi.achievement_percentage for kpi in record.kpi_ids)
                record.progress = total_achievement / len(record.kpi_ids)
            else:
                record.progress = 0.0
    
    @api.depends('strategic_goal_id', 'strategic_objective_id.strategic_goal_id')
    def _compute_parent_goal(self):
        for record in self:
            if record.strategic_goal_id:
                record.parent_goal_id = record.strategic_goal_id
            elif record.strategic_objective_id:
                record.parent_goal_id = record.strategic_objective_id.strategic_goal_id
            else:
                record.parent_goal_id = False
    
    @api.constrains('strategic_goal_id', 'strategic_objective_id')
    def _check_parent_constraint(self):
        for record in self:
            if not record.strategic_goal_id and not record.strategic_objective_id:
                raise ValidationError(_("KRA must be linked to either a Strategic Goal or Strategic Objective."))
            if record.strategic_goal_id and record.strategic_objective_id:
                raise ValidationError(_("KRA cannot be linked to both Strategic Goal and Strategic Objective. Choose one."))
    
    def action_view_kpis(self):
        """Action to view KPIs"""
        action = self.env.ref('robust_pmis.action_key_performance_indicator').read()[0]
        action['domain'] = [('kra_id', '=', self.id)]
        action['context'] = {'default_kra_id': self.id}
        return action
