# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KCCAProgramme(models.Model):
    _name = 'kcca.programme'
    _description = 'KCCA Programme'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('programme_name_unique', 'unique(name)',
         'Programme names must be unique.'),
    ]

    name = fields.Char(
        string='Programme Name',
        required=True,
        tracking=True,
        help="Name of the programme"
    )
    
    code = fields.Char(
        string='Programme Code',
        help="Short code for the programme"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the programme"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering programmes"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Implementation Structure - Programme can be implemented by multiple Directorates
    implementing_directorate_ids = fields.Many2many(
        'kcca.directorate',
        'programme_directorate_rel',
        'programme_id',
        'directorate_id',
        string='Implementing Directorates',
        tracking=True,
        help="Directorates implementing this programme"
    )

    # Intermediate model for programme-directorate relationships
    programme_directorate_rel_ids = fields.One2many(
        'programme.directorate.rel',
        'programme_id',
        string='Programme-Directorate Relations',
        help="Detailed programme-directorate implementation relationships"
    )

    # Division relationships - Programme can be implemented by multiple Divisions
    division_programme_rel_ids = fields.One2many(
        'division.programme.rel',
        'programme_id',
        string='Division Relationships',
        help="All division relationships for this programme"
    )

    implementing_division_ids = fields.Many2many(
        'kcca.division',
        string='Implementing Divisions',
        compute='_compute_implementing_divisions',
        help="Divisions implementing this programme"
    )

    # Legacy fields for backward compatibility (can be removed later)
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Primary Implementing Directorate',
        ondelete='cascade',
        tracking=True,
        help="Primary directorate implementing this programme"
    )

    division_id = fields.Many2one(
        'kcca.division',
        string='Implementing Division',
        ondelete='cascade',
        tracking=True,
        help="Division implementing this programme (if through division)"
    )
    
    # Programme Management
    programme_manager_id = fields.Many2one(
        'res.users',
        string='Programme Manager',
        tracking=True,
        help="Manager responsible for this programme"
    )
    
    start_date = fields.Date(
        string='Start Date',
        tracking=True,
        help="Programme start date"
    )

    end_date = fields.Date(
        string='End Date',
        tracking=True,
        help="Programme end date"
    )
    
    budget = fields.Monetary(
        string='Budget',
        currency_field='currency_id',
        tracking=True,
        help="Programme budget"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    # Relationships
    objective_ids = fields.One2many(
        'programme.objective',
        'programme_id',
        string='Programme Objectives',
        help="Objectives under this programme"
    )
    
    performance_indicator_ids = fields.One2many(
        'performance.indicator',
        'programme_id',
        string='Performance Indicators',
        help="Performance indicators for this programme"
    )
    
    # Strategic linkage
    strategic_objective_ids = fields.Many2many(
        'strategic.objective',
        'objective_programme_rel',
        'programme_id',
        'objective_id',
        string='Contributing to Strategic Objectives',
        help="Strategic objectives this programme contributes to"
    )
    
    # Computed fields
    objective_count = fields.Integer(
        string='Objectives Count',
        compute='_compute_counts',
        store=True
    )
    
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

    # Budget allocations
    budget_allocation_ids = fields.One2many(
        'programme.budget',
        'programme_id',
        string='Budget Allocations',
        help="Budget allocations for this programme across different financial strategies"
    )

    budget_allocation_count = fields.Integer(
        string='Budget Allocations Count',
        compute='_compute_budget_count',
        help="Number of budget allocations for this programme"
    )
    
    overall_performance = fields.Float(
        string='Overall Performance (%)',
        compute='_compute_performance',
        store=True,
        help="Overall performance based on performance indicators"
    )
    
    implementing_unit = fields.Char(
        string='Implementing Unit',
        compute='_compute_implementing_unit',
        store=True,
        help="Shows which unit implements this programme"
    )
    
    @api.depends('objective_ids', 'objective_ids.outcome_ids', 'performance_indicator_ids')
    def _compute_counts(self):
        for record in self:
            record.objective_count = len(record.objective_ids)
            record.outcome_count = len(record.objective_ids.mapped('outcome_ids'))
            record.indicator_count = len(record.performance_indicator_ids)
    
    @api.depends('performance_indicator_ids.achievement_percentage')
    def _compute_performance(self):
        for record in self:
            if record.performance_indicator_ids:
                vals = [pi.achievement_percentage or 0.0 for pi in record.performance_indicator_ids]
                if vals:
                    avg = sum(vals) / len(vals)
                else:
                    avg = 0.0
                # clamp to 0..100 to avoid outliers propagating upwards
                record.overall_performance = max(0.0, min(100.0, avg))
            else:
                record.overall_performance = 0.0

    @api.depends('budget_allocation_ids')
    def _compute_budget_count(self):
        for record in self:
            record.budget_allocation_count = len(record.budget_allocation_ids)

    @api.depends('division_programme_rel_ids')
    def _compute_implementing_divisions(self):
        """Compute divisions implementing this programme"""
        for record in self:
            record.implementing_division_ids = record.division_programme_rel_ids.mapped('division_id')

    @api.depends('implementing_directorate_ids', 'implementing_division_ids', 'directorate_id', 'division_id')
    def _compute_implementing_unit(self):
        for record in self:
            units = []

            # Primary: Use many-to-many divisions (territorial divisions)
            if record.implementing_division_ids:
                units.extend([f"{d.directorate_id.name} - {d.name}" for d in record.implementing_division_ids])

            # Secondary: Use many-to-many directorates
            elif record.implementing_directorate_ids:
                units.extend([d.name for d in record.implementing_directorate_ids])

            # Fallback: Use legacy single directorate/division
            elif record.division_id:
                units.append(f"{record.division_id.directorate_id.name} - {record.division_id.name}")
            elif record.directorate_id:
                units.append(record.directorate_id.name)

            if units:
                record.implementing_unit = ", ".join(units)
            else:
                record.implementing_unit = "Not Assigned"
    
    @api.constrains('directorate_id', 'division_id')
    def _check_implementation_constraint(self):
        for record in self:
            if not record.directorate_id and not record.division_id:
                raise ValidationError(_("Programme must be implemented by either a Directorate or Division."))
            if record.directorate_id and record.division_id:
                # Check if division belongs to the directorate
                if record.division_id.directorate_id != record.directorate_id:
                    raise ValidationError(_("If both Directorate and Division are selected, the Division must belong to the selected Directorate."))
    
    def action_view_objectives(self):
        """Action to view programme objectives"""
        action = self.env.ref('robust_pmis.action_programme_objective').read()[0]
        action['domain'] = [('programme_id', '=', self.id)]
        action['context'] = {'default_programme_id': self.id}
        return action
    
    def action_view_indicators(self):
        """Action to view performance indicators"""
        action = self.env.ref('robust_pmis.action_performance_indicator').read()[0]
        action['domain'] = [('programme_id', '=', self.id)]
        action['context'] = {'default_programme_id': self.id}
        return action

    def sync_directorate_relationships(self):
        """Sync implementing_directorate_ids with programme_directorate_rel_ids"""
        for record in self:
            # Get directorates from intermediate model
            rel_directorates = record.programme_directorate_rel_ids.mapped('directorate_id')

            # Update the many-to-many field
            record.implementing_directorate_ids = [(6, 0, rel_directorates.ids)]

        return True
