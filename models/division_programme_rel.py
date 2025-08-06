# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DivisionProgrammeRel(models.Model):
    """Intermediate model for Division-Programme relationships
    
    This model manages the many-to-many relationships between KCCA territorial divisions 
    and programmes, allowing for tracking of implementation status, resource allocation,
    and performance metrics at the division level.
    """
    _name = 'division.programme.rel'
    _description = 'Division-Programme Relationship'
    _table = 'division_programme_relationship'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'division_sequence, programme_sequence'
    
    # Core relationship fields
    division_id = fields.Many2one(
        'kcca.division',
        string='Division',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="KCCA territorial division"
    )
    
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="KCCA programme implemented by the division"
    )
    
    # Implementation details
    implementation_status = fields.Selection([
        ('not_started', 'Not Started'),
        ('planning', 'Planning Phase'),
        ('implementing', 'Implementing'),
        ('monitoring', 'Monitoring'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended')
    ], string='Implementation Status', default='not_started', tracking=True)
    
    priority_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority Level', default='medium', tracking=True)
    
    # Resource allocation
    allocated_budget = fields.Monetary(
        string='Allocated Budget',
        currency_field='currency_id',
        help="Budget allocated for this programme in this division"
    )
    
    utilized_budget = fields.Monetary(
        string='Utilized Budget',
        currency_field='currency_id',
        help="Budget utilized so far"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    # Performance tracking
    target_beneficiaries = fields.Integer(
        string='Target Beneficiaries',
        help="Number of people/entities targeted to benefit from this programme"
    )
    
    actual_beneficiaries = fields.Integer(
        string='Actual Beneficiaries',
        help="Number of people/entities actually benefiting"
    )
    
    completion_percentage = fields.Float(
        string='Completion %',
        compute='_compute_completion_percentage',
        store=True,
        help="Overall completion percentage of the programme in this division"
    )
    
    performance_score = fields.Float(
        string='Performance Score',
        compute='_compute_performance_score',
        store=True,
        help="Computed performance score based on various metrics"
    )
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="Programme implementation start date in this division"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="Programme implementation end date in this division"
    )
    
    last_review_date = fields.Date(
        string='Last Review Date',
        help="Date of last performance review"
    )
    
    next_review_date = fields.Date(
        string='Next Review Date',
        help="Date of next scheduled review"
    )
    
    # Responsible persons
    division_coordinator_id = fields.Many2one(
        'res.users',
        string='Division Coordinator',
        help="Person coordinating this programme in the division"
    )
    
    programme_officer_id = fields.Many2one(
        'res.users',
        string='Programme Officer',
        help="Officer responsible for programme implementation"
    )
    
    # Computed fields for display and sorting
    division_name = fields.Char(
        string='Division Name',
        related='division_id.name',
        store=True
    )
    
    programme_name = fields.Char(
        string='Programme Name',
        related='programme_id.name',
        store=True
    )
    
    division_sequence = fields.Integer(
        string='Division Sequence',
        related='division_id.sequence',
        store=True
    )
    
    programme_sequence = fields.Integer(
        string='Programme Sequence',
        related='programme_id.sequence',
        store=True
    )
    
    # Budget utilization percentage
    budget_utilization = fields.Float(
        string='Budget Utilization %',
        compute='_compute_budget_utilization',
        store=True,
        help="Percentage of allocated budget utilized"
    )
    
    # Beneficiary achievement percentage
    beneficiary_achievement = fields.Float(
        string='Beneficiary Achievement %',
        compute='_compute_beneficiary_achievement',
        store=True,
        help="Percentage of target beneficiaries reached"
    )
    
    # Status indicators
    is_on_track = fields.Boolean(
        string='On Track',
        compute='_compute_status_indicators',
        store=True,
        help="Whether the programme is on track"
    )
    
    is_delayed = fields.Boolean(
        string='Delayed',
        compute='_compute_status_indicators',
        store=True,
        help="Whether the programme is delayed"
    )
    
    requires_attention = fields.Boolean(
        string='Requires Attention',
        compute='_compute_status_indicators',
        store=True,
        help="Whether the programme requires management attention"
    )
    
    # Display name
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    @api.depends('division_id', 'programme_id')
    def _compute_display_name(self):
        """Compute display name for the relationship"""
        for record in self:
            if record.division_id and record.programme_id:
                record.display_name = f"{record.division_id.name} → {record.programme_id.name}"
            else:
                record.display_name = "Division-Programme Relationship"
    
    @api.depends('allocated_budget', 'utilized_budget')
    def _compute_budget_utilization(self):
        """Compute budget utilization percentage"""
        for record in self:
            if record.allocated_budget > 0:
                record.budget_utilization = (record.utilized_budget / record.allocated_budget) * 100
            else:
                record.budget_utilization = 0.0
    
    @api.depends('target_beneficiaries', 'actual_beneficiaries')
    def _compute_beneficiary_achievement(self):
        """Compute beneficiary achievement percentage"""
        for record in self:
            if record.target_beneficiaries > 0:
                record.beneficiary_achievement = (record.actual_beneficiaries / record.target_beneficiaries) * 100
            else:
                record.beneficiary_achievement = 0.0
    
    @api.depends('actual_beneficiaries', 'target_beneficiaries')
    def _compute_completion_percentage(self):
        """Compute completion percentage based on beneficiaries achieved versus target"""
        for record in self:
            if record.target_beneficiaries > 0:
                record.completion_percentage = (record.actual_beneficiaries / record.target_beneficiaries) * 100
            else:
                record.completion_percentage = 0.0
    
    @api.depends('completion_percentage', 'budget_utilization', 'beneficiary_achievement')
    def _compute_performance_score(self):
        """Compute overall performance score"""
        for record in self:
            # Weighted average of different performance metrics
            completion_weight = 0.4
            budget_weight = 0.3
            beneficiary_weight = 0.3
            
            # Clamp completion, budget, and beneficiary percentages to 100
            clamped_completion = min(record.completion_percentage, 100)
            clamped_budget = min(record.budget_utilization, 100)
            clamped_beneficiary = min(record.beneficiary_achievement, 100)
            score = (
                (clamped_completion * completion_weight) +
                (min(record.budget_utilization, 100) * budget_weight) +
                (min(record.beneficiary_achievement, 100) * beneficiary_weight)
            )
            record.performance_score = score
    
    @api.depends('performance_score', 'implementation_status', 'completion_percentage')
    def _compute_status_indicators(self):
        """Compute status indicators"""
        for record in self:
            # On track: good performance and active implementation
            record.is_on_track = (
                record.performance_score >= 70 and 
                record.implementation_status in ['implementing', 'monitoring']
            )
            
            # Delayed: poor performance or suspended
            record.is_delayed = (
                record.performance_score < 50 or 
                record.implementation_status == 'suspended'
            )
            
            # Requires attention: moderate performance issues
            record.requires_attention = (
                50 <= record.performance_score < 70 or
                record.implementation_status == 'not_started'
            )
    
    @api.constrains('division_id', 'programme_id')
    def _check_unique_relationship(self):
        """Ensure no duplicate division-programme relationships"""
        for record in self:
            if record.division_id and record.programme_id:
                existing = self.search([
                    ('division_id', '=', record.division_id.id),
                    ('programme_id', '=', record.programme_id.id),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(_(
                        "A relationship between division '%s' and programme '%s' already exists."
                    ) % (record.division_id.name, record.programme_id.name))
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Validate date constraints"""
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Start date cannot be later than end date."))
    
    @api.constrains('allocated_budget', 'utilized_budget')
    def _check_budget(self):
        """Validate budget constraints"""
        for record in self:
            if record.allocated_budget < 0:
                raise ValidationError(_("Allocated budget cannot be negative."))
            if record.utilized_budget < 0:
                raise ValidationError(_("Utilized budget cannot be negative."))
    
    def action_start_implementation(self):
        """Start programme implementation"""
        self.write({
            'implementation_status': 'implementing',
            'start_date': fields.Date.today()
        })
        return True
    
    def action_complete_implementation(self):
        """Complete programme implementation"""
        self.write({
            'implementation_status': 'completed',
            'completion_percentage': 100.0,
            'end_date': fields.Date.today()
        })
        return True
    
    def action_suspend_implementation(self):
        """Suspend programme implementation"""
        self.write({'implementation_status': 'suspended'})
        return True
