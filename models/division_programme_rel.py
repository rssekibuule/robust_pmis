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
    _sql_constraints = [
        (
            'uniq_division_programme',
            'unique(division_id, programme_id)',
            'A relationship between this Division and Programme already exists.'
        ),
    ]

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

    # Relationship semantics: mark whether this programme is directly owned by the division
    is_direct = fields.Boolean(
        string='Direct Programme',
        default=False,
        index=True,
        help='Check if this programme is directly owned by the division (not just implementing).'
    )

    # Implementation details
    implementation_status = fields.Selection([
        ('not_started', 'Not Started'),
        ('planning', 'Planning Phase'),
        ('implementing', 'Implementing'),
        ('monitoring', 'Monitoring'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended')
    ], string='Implementation Status', default='not_started', tracking=True, index=True)

    priority_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority Level', default='medium', tracking=True, index=True)

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
        index=True,
        help="Overall completion percentage of the programme in this division"
    )

    performance_score = fields.Float(
        string='Performance Score',
        compute='_compute_performance_score',
        store=True,
        index=True,
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
    budget_utilization_raw = fields.Float(
        string='Budget Utilization (Raw %)',
        compute='_compute_budget_utilization',
        store=True,
        help="Raw budget utilization before capping to 100% for scoring"
    )

    # Beneficiary achievement percentage
    beneficiary_achievement = fields.Float(
        string='Beneficiary Achievement %',
        compute='_compute_beneficiary_achievement',
        store=True,
        help="Percentage of target beneficiaries reached"
    )
    beneficiary_achievement_raw = fields.Float(
        string='Beneficiary Achievement (Raw %)',
        compute='_compute_beneficiary_achievement',
        store=True,
        help="Raw beneficiary achievement before capping to 100% for scoring"
    )

    # Status indicators
    is_on_track = fields.Boolean(
        string='On Track',
        compute='_compute_status_indicators',
        store=True,
        help="Whether the programme is on track"
    )
    completion_pct_raw = fields.Float(
        string='Completion (Raw %)',
        compute='_compute_completion_percentage',
        store=True,
        help="Raw completion percentage before capping to 100% for scoring"
    )
    completion_over_pct = fields.Float(
        string='Overachievement %',
        compute='_compute_completion_percentage',
        store=True,
        help="Amount by which completion exceeds 100% (0 if not exceeded)"
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
        index=True,
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
            if record.allocated_budget and record.allocated_budget > 0:
                pct = (record.utilized_budget or 0.0) / record.allocated_budget * 100.0
                record.budget_utilization_raw = max(0.0, pct)
                # Cap to 100 for scoring
                record.budget_utilization = min(record.budget_utilization_raw, 100.0)
            else:
                record.budget_utilization_raw = 0.0
                record.budget_utilization = 0.0
    
    @api.depends('target_beneficiaries', 'actual_beneficiaries')
    def _compute_beneficiary_achievement(self):
        """Compute beneficiary achievement percentage"""
        for record in self:
            target = record.target_beneficiaries or 0
            actual = record.actual_beneficiaries or 0
            if target > 0:
                pct = (float(actual) / float(target)) * 100.0
                record.beneficiary_achievement_raw = max(0.0, pct)
                # Cap to 100 for scoring
                record.beneficiary_achievement = min(record.beneficiary_achievement_raw, 100.0)
            else:
                record.beneficiary_achievement_raw = 0.0
                record.beneficiary_achievement = 0.0
    
    @api.depends('actual_beneficiaries', 'target_beneficiaries')
    def _compute_completion_percentage(self):
        """Compute completion percentage based on beneficiaries achieved versus target"""
        for record in self:
            target = record.target_beneficiaries or 0
            actual = record.actual_beneficiaries or 0
            if target > 0:
                pct = (float(actual) / float(target)) * 100.0
                record.completion_pct_raw = max(0.0, pct)
                # Cap to 100 for scoring
                record.completion_percentage = min(record.completion_pct_raw, 100.0)
                record.completion_over_pct = max(0.0, record.completion_pct_raw - 100.0)
            else:
                record.completion_pct_raw = 0.0
                record.completion_over_pct = 0.0
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
            clamped_completion = min(max(float(record.completion_percentage or 0.0), 0.0), 100.0)
            clamped_budget = min(max(float(record.budget_utilization or 0.0), 0.0), 100.0)
            clamped_beneficiary = min(max(float(record.beneficiary_achievement or 0.0), 0.0), 100.0)
            score = (
                (clamped_completion * completion_weight) +
                (clamped_budget * budget_weight) +
                (clamped_beneficiary * beneficiary_weight)
            )
            # Final clamp to 0..100
            record.performance_score = min(max(score, 0.0), 100.0)
    
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

    # --- Quick navigation actions for Kanban/dashboard ---
    def action_view_division(self):
        """Open the related Division form view."""
        self.ensure_one()
        if not self.division_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Division'),
            'res_model': 'kcca.division',
            'res_id': self.division_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_programme(self):
        """Open the related Programme form view."""
        self.ensure_one()
        if not self.programme_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Programme'),
            'res_model': 'kcca.programme',
            'res_id': self.programme_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # --- Direct programme tagging helpers ---
    @api.model
    def _compute_is_direct_value(self, division_id, programme_id):
        """Return True if the programme is directly owned by the division.

        Business rule: programme is direct when programme.division_id == division_id.
        """
        if not division_id or not programme_id:
            return False
        Programme = self.env['kcca.programme']
        prog = Programme.browse(programme_id)
        return bool(prog and prog.division_id and prog.division_id.id == division_id)

    @api.model_create_multi
    def create(self, vals_list):
        """Batch-safe create override that auto-derives is_direct.

        For each payload, compute is_direct based on programme.division_id when
        both division_id and programme_id are provided.
        """
        # Normalize single-dict input just in case
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        for vals in vals_list:
            division_id = vals.get('division_id')
            programme_id = vals.get('programme_id')
            if division_id and programme_id and 'is_direct' not in vals:
                vals['is_direct'] = self._compute_is_direct_value(division_id, programme_id)
        records = super().create(vals_list)
        return records

    def write(self, vals):
        res = super().write(vals)
        # If division or programme changed (or either present in vals), recompute is_direct
        if any(k in vals for k in ('division_id', 'programme_id')):
            for rec in self:
                rec.is_direct = self._compute_is_direct_value(rec.division_id.id, rec.programme_id.id)
        return res

    @api.model
    def mark_direct_programme_flags(self):
        """Batch-tag existing relationships where the programme is owned by the same division.

        This is safe to call on upgrade to initialize the is_direct flag.
        """
        rels = self.search([])
        updates = []
        for rel in rels:
            should_be_direct = self._compute_is_direct_value(rel.division_id.id, rel.programme_id.id)
            if rel.is_direct != should_be_direct:
                updates.append(rel.id)
        if updates:
            self.browse(updates).write({'is_direct': True})
        return len(updates)

    @api.model
    def cron_integrity_check(self):
        """Nightly integrity pass for relationships.

        - Normalize direct flags based on programme ownership
        - Enforce allowed implementing relations via division utility
        """
        try:
            self.sudo().mark_direct_programme_flags()
        except Exception:
            pass
        try:
            self.env['kcca.division'].sudo().enforce_allowed_implementing_relations()
        except Exception:
            pass
        return True
