# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class IntermediateOutcome(models.Model):
    _name = 'intermediate.outcome'
    _description = 'Intermediate Outcome'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Intermediate Outcome',
        required=True,
        tracking=True,
        help="Name of the intermediate outcome"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the intermediate outcome"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering outcomes within objective"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    objective_id = fields.Many2one(
        'programme.objective',
        string='Programme Objective',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Parent programme objective"
    )
    
    indicator_ids = fields.One2many(
        'performance.indicator',
        'outcome_id',
        string='Performance Indicators',
        help="Performance indicators for this outcome"
    )

    intervention_ids = fields.One2many(
        'intervention',
        'outcome_id',
        string='Interventions',
        help="Interventions under this intermediate outcome"
    )
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="Outcome start date"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="Outcome end date"
    )
    
    # Responsible person
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        help="Person responsible for this outcome"
    )
    
    # Computed fields
    indicator_count = fields.Integer(
        string='Indicators Count',
        compute='_compute_counts',
        store=True
    )

    intervention_count = fields.Integer(
        string='Interventions Count',
        compute='_compute_counts',
        store=True
    )

    output_count = fields.Integer(
        string='Outputs Count',
        compute='_compute_counts',
        store=True
    )

    piap_action_count = fields.Integer(
        string='PIAP Actions Count',
        compute='_compute_counts',
        store=True
    )
    
    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress',
        store=True,
        help="Progress based on performance indicators achievement"
    )
    
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        related='objective_id.programme_id',
        store=True,
        help="Related programme"
    )
    
    @api.depends('indicator_ids', 'intervention_ids', 'intervention_ids.output_ids',
                 'intervention_ids.output_ids.piap_action_ids')
    def _compute_counts(self):
        for record in self:
            record.indicator_count = len(record.indicator_ids)
            record.intervention_count = len(record.intervention_ids)
            record.output_count = len(record.intervention_ids.mapped('output_ids'))
            record.piap_action_count = len(record.intervention_ids.mapped('output_ids.piap_action_ids'))
    
    @api.depends('indicator_ids.achievement_percentage', 'intervention_ids.progress')
    def _compute_progress(self):
        for record in self:
            total_progress = 0.0
            count = 0

            # Include indicators achievement
            if record.indicator_ids:
                indicator_progress = sum(indicator.achievement_percentage for indicator in record.indicator_ids)
                total_progress += indicator_progress
                count += len(record.indicator_ids)

            # Include interventions progress
            if record.intervention_ids:
                intervention_progress = sum(intervention.progress for intervention in record.intervention_ids)
                total_progress += intervention_progress
                count += len(record.intervention_ids)

            record.progress = total_progress / count if count > 0 else 0.0
    
    def action_view_indicators(self):
        """Action to view performance indicators"""
        action = self.env.ref('robust_pmis.action_performance_indicator').read()[0]
        action['domain'] = [('outcome_id', '=', self.id)]
        action['context'] = {'default_outcome_id': self.id}
        return action

    def action_view_interventions(self):
        """Action to view interventions"""
        action = self.env.ref('robust_pmis.action_intervention').read()[0]
        action['domain'] = [('outcome_id', '=', self.id)]
        action['context'] = {'default_outcome_id': self.id}
        return action

    def action_view_outputs(self):
        """Action to view outputs"""
        action = self.env.ref('robust_pmis.action_output').read()[0]
        action['domain'] = [('intervention_id.outcome_id', '=', self.id)]
        action['context'] = {'default_outcome_id': self.id}
        return action

    def action_view_piap_actions(self):
        """Action to view PIAP actions"""
        action = self.env.ref('robust_pmis.action_piap_action').read()[0]
        action['domain'] = [('output_id.intervention_id.outcome_id', '=', self.id)]
        action['context'] = {'default_outcome_id': self.id}
        return action
