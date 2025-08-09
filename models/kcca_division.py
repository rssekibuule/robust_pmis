# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KCCADivision(models.Model):
    _name = 'kcca.division'
    _description = 'KCCA Division'
    _order = 'directorate_id, sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Division Name',
        required=True,
        tracking=True,
        help="Name of the division"
    )
    
    code = fields.Char(
        string='Division Code',
        help="Short code for the division"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the division"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering divisions within directorate"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Directorate',
        required=False,
        ondelete='set null',
        tracking=True,
        help="Parent directorate (optional for territorial divisions)"
    )

    programme_ids = fields.One2many(
        'kcca.programme',
        'division_id',
        string='Direct Programmes',
        help="Programmes directly assigned to this division"
    )

    # Many-to-many relationship with programmes through intermediate model
    division_programme_rel_ids = fields.One2many(
        'division.programme.rel',
        'division_id',
        string='Programme Relationships',
        help="All programme relationships for this division"
    )

    implementing_programme_ids = fields.Many2many(
        'kcca.programme',
        string='Implementing Programmes',
        compute='_compute_implementing_programmes',
        help="All programmes this division implements (via relationships)"
    )
    
    # Leadership
    head_id = fields.Many2one(
        'res.users',
        string='Division Head',
        help="Head of this division"
    )
    
    deputy_head_id = fields.Many2one(
        'res.users',
        string='Deputy Head',
        help="Deputy head of this division"
    )
    
    # Contact Information
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    office_location = fields.Char(string='Office Location')
    
    # Computed fields
    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_counts',
        store=True
    )
    
    performance_indicator_count = fields.Integer(
        string='Performance Indicators Count',
        compute='_compute_counts',
        store=True
    )
    
    overall_performance = fields.Float(
        string='Overall Performance (%)',
        compute='_compute_performance',
        store=True,
        help="Overall performance based on programme performance indicators"
    )
    
    @api.depends('division_programme_rel_ids')
    def _compute_implementing_programmes(self):
        """Compute programmes this division implements"""
        for record in self:
            record.implementing_programme_ids = record.division_programme_rel_ids.mapped('programme_id')

    @api.depends('programme_ids', 'programme_ids.performance_indicator_ids', 'implementing_programme_ids')
    def _compute_counts(self):
        for record in self:
            # Count both direct and implementing programmes
            all_programmes = record.programme_ids | record.implementing_programme_ids
            record.programme_count = len(all_programmes)
            all_indicators = all_programmes.mapped('performance_indicator_ids')
            record.performance_indicator_count = len(all_indicators)
    
    @api.depends('programme_ids.overall_performance', 'division_programme_rel_ids.performance_score')
    def _compute_performance(self):
        for record in self:
            # Combine direct programme performance and relationship performance scores
            direct_performance = 0.0
            relationship_performance = 0.0

            if record.programme_ids:
                direct_performance = sum(prog.overall_performance for prog in record.programme_ids) / len(record.programme_ids)

            if record.division_programme_rel_ids:
                relationship_performance = sum(rel.performance_score for rel in record.division_programme_rel_ids) / len(record.division_programme_rel_ids)

            # Weight the performances (70% relationship, 30% direct)
            if record.division_programme_rel_ids and record.programme_ids:
                record.overall_performance = (relationship_performance * 0.7) + (direct_performance * 0.3)
            elif record.division_programme_rel_ids:
                record.overall_performance = relationship_performance
            elif record.programme_ids:
                record.overall_performance = direct_performance
            else:
                record.overall_performance = 0.0
    
    def action_view_programmes(self):
        """Action to view programmes"""
        action = self.env.ref('robust_pmis.action_kcca_programme').read()[0]
        action['domain'] = [('division_id', '=', self.id)]
        action['context'] = {'default_division_id': self.id, 'default_directorate_id': self.directorate_id.id}
        return action

    def action_view_division_performance(self):
        """Action to view division performance across programmes"""
        action = self.env.ref('robust_pmis.action_division_programme_performance').read()[0]
        action['domain'] = [('division_id', '=', self.id)]
        action['context'] = {
            'default_division_id': self.id,
            'search_default_active': 1
        }
        return action
