# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProgrammeObjective(models.Model):
    _name = 'programme.objective'
    _description = 'Programme Objective'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Programme Objective',
        required=True,
        tracking=True,
        help="Name of the programme objective"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the programme objective"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering objectives within programme"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Parent programme"
    )
    
    outcome_ids = fields.One2many(
        'intermediate.outcome',
        'objective_id',
        string='Intermediate Outcomes',
        help="Intermediate outcomes under this objective"
    )
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="Objective start date"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="Objective end date"
    )
    
    # Responsible person
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        help="Person responsible for this objective"
    )
    
    # Computed fields
    outcome_count = fields.Integer(
        string='Outcomes Count',
        compute='_compute_counts',
        store=True
    )
    
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
        help="Progress based on intermediate outcomes achievement"
    )
    
    @api.depends('outcome_ids', 'outcome_ids.indicator_ids', 'outcome_ids.intervention_ids',
                 'outcome_ids.intervention_ids.output_ids', 'outcome_ids.intervention_ids.output_ids.piap_action_ids',
                 'outcome_ids.intervention_ids.output_ids.indicator_ids')
    def _compute_counts(self):
        for record in self:
            record.outcome_count = len(record.outcome_ids)

            # Count indicators from both outcomes and outputs
            outcome_indicators = record.outcome_ids.mapped('indicator_ids')
            output_indicators = record.outcome_ids.mapped('intervention_ids.output_ids.indicator_ids')
            all_indicators = outcome_indicators | output_indicators
            record.indicator_count = len(all_indicators)

            record.intervention_count = len(record.outcome_ids.mapped('intervention_ids'))
            record.output_count = len(record.outcome_ids.mapped('intervention_ids.output_ids'))
            record.piap_action_count = len(record.outcome_ids.mapped('intervention_ids.output_ids.piap_action_ids'))
    
    @api.depends('outcome_ids.progress')
    def _compute_progress(self):
        for record in self:
            if record.outcome_ids:
                total_progress = sum(outcome.progress for outcome in record.outcome_ids)
                record.progress = total_progress / len(record.outcome_ids)
            else:
                record.progress = 0.0
    
    def action_view_outcomes(self):
        """Action to view intermediate outcomes"""
        action = self.env.ref('robust_pmis.action_intermediate_outcome').read()[0]
        action['domain'] = [('objective_id', '=', self.id)]
        action['context'] = {'default_objective_id': self.id}
        return action

    def action_view_indicators(self):
        """Action to view performance indicators"""
        action = self.env.ref('robust_pmis.action_performance_indicator').read()[0]
        # Get indicators from both outcomes and outputs under this objective
        outcome_ids = self.outcome_ids.ids
        output_ids = self.outcome_ids.mapped('intervention_ids.output_ids').ids

        # Create domain to include both outcome and output indicators
        domain = ['|', ('outcome_id', 'in', outcome_ids), ('output_id', 'in', output_ids)]
        action['domain'] = domain
        action['context'] = {'default_outcome_id': outcome_ids[0] if outcome_ids else False}
        return action

    def action_view_interventions(self):
        """Action to view interventions"""
        action = self.env.ref('robust_pmis.action_intervention').read()[0]
        outcome_ids = self.outcome_ids.ids
        action['domain'] = [('outcome_id', 'in', outcome_ids)]
        action['context'] = {'default_outcome_id': outcome_ids[0] if outcome_ids else False}
        return action

    def action_view_outputs(self):
        """Action to view outputs"""
        action = self.env.ref('robust_pmis.action_output').read()[0]
        outcome_ids = self.outcome_ids.ids
        action['domain'] = [('intervention_id.outcome_id', 'in', outcome_ids)]
        action['context'] = {'default_outcome_id': outcome_ids[0] if outcome_ids else False}
        return action

    def action_view_piap_actions(self):
        """Action to view PIAP actions"""
        action = self.env.ref('robust_pmis.action_piap_action').read()[0]
        outcome_ids = self.outcome_ids.ids
        action['domain'] = [('outcome_id', 'in', outcome_ids)]
        action['context'] = {'default_outcome_id': outcome_ids[0] if outcome_ids else False}
        return action

    def action_open_objective(self):
        """Action to open the programme objective form view"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Programme Objective',
            'res_model': 'programme.objective',
            'res_id': self.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }
