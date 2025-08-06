# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PIAPAction(models.Model):
    _name = 'piap.action'
    _description = 'PIAP Action'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='PIAP Action Name',
        required=True,
        tracking=True,
        help="Name of the PIAP action"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the PIAP action"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering PIAP actions within output"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    output_id = fields.Many2one(
        'output',
        string='Output',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Parent output"
    )
    
    # Status and Progress
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='not_started', tracking=True)
    
    progress = fields.Float(
        string='Progress (%)',
        default=0.0,
        tracking=True,
        help="Completion percentage (0-100%)"
    )
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="PIAP action start date"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="PIAP action end date"
    )
    
    actual_start_date = fields.Date(
        string='Actual Start Date',
        help="Actual start date"
    )
    
    actual_end_date = fields.Date(
        string='Actual End Date',
        help="Actual completion date"
    )
    
    # Responsible person
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        help="Person responsible for this PIAP action"
    )
    
    # Budget fields - Multi-year tracking
    budget_fy2022_23 = fields.Float(
        string='Budget FY2022/23 (UGX Billion)',
        help="Budget allocation for FY2022/23"
    )
    
    budget_fy2023_24 = fields.Float(
        string='Budget FY2023/24 (UGX Billion)',
        help="Budget allocation for FY2023/24"
    )
    
    budget_fy2024_25 = fields.Float(
        string='Budget FY2024/25 (UGX Billion)',
        help="Budget allocation for FY2024/25"
    )
    
    budget_fy2025_26 = fields.Float(
        string='Budget FY2025/26 (UGX Billion)',
        help="Budget allocation for FY2025/26"
    )
    
    budget_fy2026_27 = fields.Float(
        string='Budget FY2026/27 (UGX Billion)',
        help="Budget allocation for FY2026/27"
    )

    budget_fy2027_28 = fields.Float(
        string='Budget FY2027/28 (UGX Billion)',
        help="Budget allocation for FY2027/28"
    )

    budget_fy2028_29 = fields.Float(
        string='Budget FY2028/29 (UGX Billion)',
        help="Budget allocation for FY2028/29"
    )

    budget_fy2029_30 = fields.Float(
        string='Budget FY2029/30 (UGX Billion)',
        help="Budget allocation for FY2029/30"
    )

    total_budget = fields.Float(
        string='Total Budget (UGX Billion)',
        compute='_compute_total_budget',
        store=True,
        help="Total budget across all fiscal years"
    )
    
    # Performance targets (if applicable)
    target_value = fields.Float(
        string='Target Value',
        help="Target value for this PIAP action (if measurable)"
    )
    
    current_value = fields.Float(
        string='Current Value',
        help="Current achieved value"
    )
    
    baseline_value = fields.Float(
        string='Baseline Value',
        help="Starting/baseline value"
    )
    
    measurement_unit = fields.Char(
        string='Unit of Measurement',
        help="Unit for measuring this PIAP action (e.g., Number, Km, etc.)"
    )
    
    # Related fields for easy access
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        related='output_id.intervention_id.outcome_id.objective_id.programme_id',
        store=True,
        help="Related programme"
    )
    
    objective_id = fields.Many2one(
        'programme.objective',
        string='Programme Objective',
        related='output_id.intervention_id.outcome_id.objective_id',
        store=True,
        help="Related programme objective"
    )
    
    outcome_id = fields.Many2one(
        'intermediate.outcome',
        string='Intermediate Outcome',
        related='output_id.intervention_id.outcome_id',
        store=True,
        help="Related intermediate outcome"
    )
    
    intervention_id = fields.Many2one(
        'intervention',
        string='Intervention',
        related='output_id.intervention_id',
        store=True,
        help="Related intervention"
    )
    
    @api.depends('budget_fy2022_23', 'budget_fy2023_24', 'budget_fy2024_25',
                 'budget_fy2025_26', 'budget_fy2026_27', 'budget_fy2027_28',
                 'budget_fy2028_29', 'budget_fy2029_30')
    def _compute_total_budget(self):
        for record in self:
            record.total_budget = (
                record.budget_fy2022_23 + record.budget_fy2023_24 +
                record.budget_fy2024_25 + record.budget_fy2025_26 +
                record.budget_fy2026_27 + record.budget_fy2027_28 +
                record.budget_fy2028_29 + record.budget_fy2029_30
            )
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Start date cannot be later than end date."))
    
    @api.constrains('actual_start_date', 'actual_end_date')
    def _check_actual_dates(self):
        for record in self:
            if record.actual_start_date and record.actual_end_date and record.actual_start_date > record.actual_end_date:
                raise ValidationError(_("Actual start date cannot be later than actual end date."))
    
    @api.constrains('progress')
    def _check_progress(self):
        for record in self:
            if record.progress < 0 or record.progress > 100:
                raise ValidationError(_("Progress must be between 0 and 100%."))
    
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.output_id:
                name = f"{record.output_id.name} - {name}"
            result.append((record.id, name))
        return result

    def write(self, vals):
        """Override write to log important changes in chatter"""
        # Track current values before update
        old_values = {}
        tracked_fields = ['status', 'progress', 'responsible_user_id', 'actual_start_date', 'actual_end_date']

        if any(field in vals for field in tracked_fields):
            for record in self:
                old_values[record.id] = {
                    'status': record.status,
                    'progress': record.progress,
                    'responsible_user_id': record.responsible_user_id,
                    'actual_start_date': record.actual_start_date,
                    'actual_end_date': record.actual_end_date,
                }

        # Call parent write method
        result = super().write(vals)

        # Log significant changes in chatter
        for record in self:
            old_vals = old_values.get(record.id, {})
            changes = []

            if 'status' in vals and old_vals.get('status') != record.status:
                old_status = dict(record._fields['status'].selection).get(old_vals.get('status'), 'Unknown')
                new_status = dict(record._fields['status'].selection).get(record.status, 'Unknown')
                changes.append(f"Status: <strong>{old_status}</strong> → <strong>{new_status}</strong>")

            if 'progress' in vals and old_vals.get('progress') != record.progress:
                changes.append(f"Progress: <strong>{old_vals.get('progress', 0):.1f}%</strong> → <strong>{record.progress:.1f}%</strong>")

            if 'responsible_user_id' in vals and old_vals.get('responsible_user_id') != record.responsible_user_id:
                old_user = old_vals.get('responsible_user_id').name if old_vals.get('responsible_user_id') else 'None'
                new_user = record.responsible_user_id.name if record.responsible_user_id else 'None'
                changes.append(f"Responsible Person: <strong>{old_user}</strong> → <strong>{new_user}</strong>")

            if 'actual_start_date' in vals and old_vals.get('actual_start_date') != record.actual_start_date:
                old_date = old_vals.get('actual_start_date').strftime('%Y-%m-%d') if old_vals.get('actual_start_date') else 'Not Set'
                new_date = record.actual_start_date.strftime('%Y-%m-%d') if record.actual_start_date else 'Not Set'
                changes.append(f"Actual Start Date: <strong>{old_date}</strong> → <strong>{new_date}</strong>")

            if 'actual_end_date' in vals and old_vals.get('actual_end_date') != record.actual_end_date:
                old_date = old_vals.get('actual_end_date').strftime('%Y-%m-%d') if old_vals.get('actual_end_date') else 'Not Set'
                new_date = record.actual_end_date.strftime('%Y-%m-%d') if record.actual_end_date else 'Not Set'
                changes.append(f"Actual End Date: <strong>{old_date}</strong> → <strong>{new_date}</strong>")

            if changes:
                # Create audit log entries for each change
                for field_name in ['status', 'progress', 'responsible_user_id', 'actual_start_date', 'actual_end_date']:
                    if field_name in vals and old_vals.get(field_name) != getattr(record, field_name):
                        self.env['audit.log'].log_field_change(
                            record=record,
                            field_name=field_name,
                            old_value=old_vals.get(field_name),
                            new_value=getattr(record, field_name),
                            action_description=f"PIAP Action {field_name.replace('_', ' ').title()} updated"
                        )

                # Post message to chatter
                record.message_post(
                    body=f"<p><strong>PIAP Action Updated</strong></p>"
                         f"<ul>{''.join(f'<li>{change}</li>' for change in changes)}</ul>"
                         f"<p><small>Updated by: <strong>{self.env.user.name}</strong> at {fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>",
                    subtype_id=self.env.ref('mail.mt_note').id
                )

        return result
