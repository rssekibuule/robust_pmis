# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Intervention(models.Model):
    _name = 'intervention'
    _description = 'Programme Intervention'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Intervention Name',
        required=True,
        tracking=True,
        help="Name of the intervention"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the intervention"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering interventions within intermediate outcome"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    outcome_id = fields.Many2one(
        'intermediate.outcome',
        string='Intermediate Outcome',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Parent intermediate outcome"
    )
    
    output_ids = fields.One2many(
        'output',
        'intervention_id',
        string='Outputs',
        help="Outputs under this intervention"
    )
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="Intervention start date"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="Intervention end date"
    )
    
    # Responsible person
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        tracking=True,
        help="Person responsible for this intervention"
    )
    
    # Computed fields
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
    
    indicator_count = fields.Integer(
        string='Indicators Count',
        compute='_compute_counts',
        store=True
    )
    
    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress',
        store=True,
        help="Progress based on outputs achievement"
    )
    
    # Related fields for easy access
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        related='outcome_id.objective_id.programme_id',
        store=True,
        help="Related programme"
    )
    
    objective_id = fields.Many2one(
        'programme.objective',
        string='Programme Objective',
        related='outcome_id.objective_id',
        store=True,
        help="Related programme objective"
    )
    
    @api.depends('output_ids', 'output_ids.piap_action_ids', 'output_ids.indicator_ids')
    def _compute_counts(self):
        for record in self:
            record.output_count = len(record.output_ids)
            record.piap_action_count = len(record.output_ids.mapped('piap_action_ids'))
            record.indicator_count = len(record.output_ids.mapped('indicator_ids'))
    
    @api.depends('output_ids.progress')
    def _compute_progress(self):
        for record in self:
            if record.output_ids:
                total_progress = sum(output.progress for output in record.output_ids)
                record.progress = total_progress / len(record.output_ids)
            else:
                record.progress = 0.0
    
    def action_view_outputs(self):
        """Action to view outputs"""
        action = self.env.ref('robust_pmis.action_output').read()[0]
        action['domain'] = [('intervention_id', '=', self.id)]
        action['context'] = {'default_intervention_id': self.id}
        return action
    
    def action_view_piap_actions(self):
        """Action to view PIAP actions"""
        action = self.env.ref('robust_pmis.action_piap_action').read()[0]
        action['domain'] = [('output_id.intervention_id', '=', self.id)]
        action['context'] = {'default_intervention_id': self.id}
        return action
    
    def action_view_indicators(self):
        """Action to view performance indicators"""
        action = self.env.ref('robust_pmis.action_performance_indicator').read()[0]
        action['domain'] = [('output_id.intervention_id', '=', self.id)]
        action['context'] = {'default_intervention_id': self.id}
        return action
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Start date cannot be later than end date."))
    
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.outcome_id:
                name = f"{record.outcome_id.name} - {name}"
            result.append((record.id, name))
        return result

    def write(self, vals):
        """Override write to log important changes in chatter"""
        # Track current values before update
        old_values = {}
        tracked_fields = ['responsible_user_id', 'start_date', 'end_date']

        if any(field in vals for field in tracked_fields):
            for record in self:
                old_values[record.id] = {
                    'responsible_user_id': record.responsible_user_id,
                    'start_date': record.start_date,
                    'end_date': record.end_date,
                }

        # Call parent write method
        result = super().write(vals)

        # Log significant changes in chatter
        for record in self:
            old_vals = old_values.get(record.id, {})
            changes = []

            if 'responsible_user_id' in vals and old_vals.get('responsible_user_id') != record.responsible_user_id:
                old_user = old_vals.get('responsible_user_id').name if old_vals.get('responsible_user_id') else 'None'
                new_user = record.responsible_user_id.name if record.responsible_user_id else 'None'
                changes.append(f"Responsible Person: <strong>{old_user}</strong> → <strong>{new_user}</strong>")

            if 'start_date' in vals and old_vals.get('start_date') != record.start_date:
                old_date = old_vals.get('start_date').strftime('%Y-%m-%d') if old_vals.get('start_date') else 'Not Set'
                new_date = record.start_date.strftime('%Y-%m-%d') if record.start_date else 'Not Set'
                changes.append(f"Start Date: <strong>{old_date}</strong> → <strong>{new_date}</strong>")

            if 'end_date' in vals and old_vals.get('end_date') != record.end_date:
                old_date = old_vals.get('end_date').strftime('%Y-%m-%d') if old_vals.get('end_date') else 'Not Set'
                new_date = record.end_date.strftime('%Y-%m-%d') if record.end_date else 'Not Set'
                changes.append(f"End Date: <strong>{old_date}</strong> → <strong>{new_date}</strong>")

            if changes:
                record.message_post(
                    body=f"<p><strong>Intervention Updated</strong></p>"
                         f"<ul>{''.join(f'<li>{change}</li>' for change in changes)}</ul>"
                         f"<p><small>Updated by: <strong>{self.env.user.name}</strong> at {fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>",
                    message_type='comment',
                    subtype_xmlid='mail.mt_note'
                )

        return result
