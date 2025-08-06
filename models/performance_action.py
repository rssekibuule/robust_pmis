# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PerformanceAction(models.Model):
    _name = 'performance.action'
    _description = 'Performance Action'
    _order = 'date desc, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Action Name',
        required=True,
        tracking=True,
        help="Name of the performance action"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the action taken"
    )
    
    date = fields.Date(
        string='Action Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
        help="Date when the action was taken"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    indicator_id = fields.Many2one(
        'performance.indicator',
        string='Performance Indicator',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Performance indicator this action updates"
    )
    
    # Action details
    action_type = fields.Selection([
        ('update', 'Value Update'),
        ('milestone', 'Milestone Achievement'),
        ('correction', 'Corrective Action'),
        ('improvement', 'Improvement Initiative'),
        ('review', 'Review/Assessment'),
    ], string='Action Type', required=True, default='update')
    
    # Value updates
    previous_value = fields.Float(
        string='Previous Value',
        help="Previous value before this action"
    )
    
    new_value = fields.Float(
        string='New Value',
        help="New value after this action"
    )
    
    value_change = fields.Float(
        string='Value Change',
        compute='_compute_value_change',
        store=True,
        help="Change in value due to this action"
    )
    
    # Progress tracking
    progress_notes = fields.Text(
        string='Progress Notes',
        help="Notes about progress made"
    )
    
    challenges = fields.Text(
        string='Challenges',
        help="Challenges encountered"
    )
    
    next_steps = fields.Text(
        string='Next Steps',
        help="Planned next steps"
    )
    
    # Responsible parties
    action_by_id = fields.Many2one(
        'res.users',
        string='Action Taken By',
        required=True,
        default=lambda self: self.env.user,
        help="User who took this action"
    )
    
    approved_by_id = fields.Many2one(
        'res.users',
        string='Approved By',
        help="User who approved this action"
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    
    # Attachments
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments',
        help="Supporting documents for this action"
    )
    
    # Computed fields
    indicator_name = fields.Char(
        string='Indicator Name',
        related='indicator_id.name',
        store=True
    )
    
    programme_name = fields.Char(
        string='Programme',
        related='indicator_id.parent_programme_id.name',
        store=True
    )
    
    @api.depends('previous_value', 'new_value')
    def _compute_value_change(self):
        for record in self:
            record.value_change = record.new_value - record.previous_value
    
    @api.onchange('indicator_id')
    def _onchange_indicator_id(self):
        if self.indicator_id:
            self.previous_value = self.indicator_id.current_value
    
    def action_submit(self):
        """Submit action for approval"""
        self.state = 'submitted'
        self.message_post(body=_("Action submitted for approval"))
    
    def action_approve(self):
        """Approve action and update indicator value"""
        if self.state != 'submitted':
            raise ValidationError(_("Only submitted actions can be approved"))
        
        # Update the indicator's current value
        if self.new_value != self.previous_value:
            self.indicator_id.current_value = self.new_value
        
        self.state = 'approved'
        self.approved_by_id = self.env.user
        
        # Create performance score record
        self.env['performance.score'].create({
            'indicator_id': self.indicator_id.id,
            'action_id': self.id,
            'date': self.date,
            'value': self.new_value,
            'achievement_percentage': self.indicator_id.achievement_percentage,
            'notes': self.progress_notes,
        })
        
        self.message_post(body=_("Action approved and indicator updated"))
    
    def action_reject(self):
        """Reject action"""
        if self.state != 'submitted':
            raise ValidationError(_("Only submitted actions can be rejected"))
        
        self.state = 'rejected'
        self.message_post(body=_("Action rejected"))
    
    def action_reset_to_draft(self):
        """Reset to draft"""
        self.state = 'draft'
