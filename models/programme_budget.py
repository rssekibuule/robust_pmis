# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProgrammeBudget(models.Model):
    _name = 'programme.budget'
    _description = 'Programme Budget Allocation - Strategic Plan Cost Breakdown'
    _order = 'sequence, programme_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Budget Name',
        compute='_compute_name',
        store=True,
        help="Auto-generated name based on programme and financial strategy"
    )
    
    sequence = fields.Integer(
        string='S/N',
        required=True,
        help="Serial number as shown in the strategic plan table"
    )
    
    # Foreign key relationships
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        required=True,
        ondelete='cascade',
        help="Programme for which budget is allocated"
    )
    
    financial_strategy_id = fields.Many2one(
        'financial.strategy',
        string='Financial Strategy',
        required=True,
        ondelete='cascade',
        help="Financial strategy this budget allocation belongs to"
    )
    
    # Budget allocations by fiscal year (in UGX Billions)
    budget_fy2025_26 = fields.Float(
        string='FY2025/26 (UGX Bns)',
        tracking=True,
        help="Budget allocation for FY2025/26 in UGX Billions"
    )
    
    budget_fy2026_27 = fields.Float(
        string='FY2026/27 (UGX Bns)',
        tracking=True,
        help="Budget allocation for FY2026/27 in UGX Billions"
    )
    
    budget_fy2027_28 = fields.Float(
        string='FY2027/28 (UGX Bns)',
        tracking=True,
        help="Budget allocation for FY2027/28 in UGX Billions"
    )
    
    budget_fy2028_29 = fields.Float(
        string='FY2028/29 (UGX Bns)',
        tracking=True,
        help="Budget allocation for FY2028/29 in UGX Billions"
    )
    
    budget_fy2029_30 = fields.Float(
        string='FY2029/30 (UGX Bns)',
        tracking=True,
        help="Budget allocation for FY2029/30 in UGX Billions"
    )
    
    # Computed total budget
    total_budget = fields.Float(
        string='TOTAL (UGX Bns)',
        compute='_compute_total_budget',
        store=True,
        help="Total budget allocation across all fiscal years"
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for budget amounts"
    )
    
    # Status and tracking
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    # Related fields for easier access
    programme_name = fields.Char(
        related='programme_id.name',
        string='Programme Name',
        store=True,
        readonly=True
    )
    
    programme_code = fields.Char(
        related='programme_id.code',
        string='Programme Code',
        store=True,
        readonly=True
    )
    
    financial_strategy_name = fields.Char(
        related='financial_strategy_id.name',
        string='Financial Strategy Name',
        store=True,
        readonly=True
    )
    
    # Notes and comments
    notes = fields.Html(
        string='Notes',
        help="Additional notes about this budget allocation"
    )
    
    # Responsible person
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        tracking=True,
        help="Person responsible for this budget allocation"
    )

    @api.depends('programme_id', 'financial_strategy_id')
    def _compute_name(self):
        for record in self:
            if record.programme_id and record.financial_strategy_id:
                record.name = f"{record.programme_id.name} - {record.financial_strategy_id.name}"
            elif record.programme_id:
                record.name = f"{record.programme_id.name} - Budget Allocation"
            else:
                record.name = "Programme Budget Allocation"

    @api.depends('budget_fy2025_26', 'budget_fy2026_27', 'budget_fy2027_28', 
                 'budget_fy2028_29', 'budget_fy2029_30')
    def _compute_total_budget(self):
        for record in self:
            record.total_budget = (
                record.budget_fy2025_26 + record.budget_fy2026_27 + 
                record.budget_fy2027_28 + record.budget_fy2028_29 + 
                record.budget_fy2029_30
            )

    @api.constrains('sequence', 'financial_strategy_id')
    def _check_unique_sequence(self):
        for record in self:
            if record.sequence:
                existing = self.search([
                    ('sequence', '=', record.sequence),
                    ('financial_strategy_id', '=', record.financial_strategy_id.id),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(
                        _("Sequence number %s already exists for this financial strategy. "
                          "Please use a different sequence number.") % record.sequence
                    )

    @api.constrains('programme_id', 'financial_strategy_id')
    def _check_unique_programme_strategy(self):
        for record in self:
            if record.programme_id and record.financial_strategy_id:
                existing = self.search([
                    ('programme_id', '=', record.programme_id.id),
                    ('financial_strategy_id', '=', record.financial_strategy_id.id),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(
                        _("Budget allocation for programme '%s' already exists for this financial strategy.") 
                        % record.programme_id.name
                    )

    def action_approve(self):
        """Approve the budget allocation"""
        self.write({'status': 'approved'})
        return True

    def action_activate(self):
        """Activate the budget allocation"""
        self.write({'status': 'active'})
        return True

    def action_complete(self):
        """Mark the budget allocation as completed"""
        self.write({'status': 'completed'})
        return True

    def action_cancel(self):
        """Cancel the budget allocation"""
        self.write({'status': 'cancelled'})
        return True
