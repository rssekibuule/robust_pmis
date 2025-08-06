# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KCCADirectorate(models.Model):
    _name = 'kcca.directorate'
    _description = 'KCCA Directorate'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Directorate Name',
        required=True,
        tracking=True,
        help="Name of the directorate"
    )
    
    code = fields.Char(
        string='Directorate Code',
        help="Short code for the directorate"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the directorate"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering directorates"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    color = fields.Char(
        string='Color',
        help="Color for kanban view"
    )
    
    # Leadership
    director_id = fields.Many2one(
        'res.users',
        string='Director',
        help="Director of this directorate"
    )
    
    deputy_director_id = fields.Many2one(
        'res.users',
        string='Deputy Director',
        help="Deputy director of this directorate"
    )
    
    # Contact Information
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    office_location = fields.Char(string='Office Location')
    
    # Relationships
    division_ids = fields.One2many(
        'kcca.division',
        'directorate_id',
        string='Divisions',
        help="Divisions under this directorate"
    )
    
    # Programmes implemented by this directorate (many-to-many relationship)
    implementing_programme_ids = fields.Many2many(
        'kcca.programme',
        'programme_directorate_rel',
        'directorate_id',
        'programme_id',
        string='Implementing Programmes',
        help="Programmes implemented by this directorate"
    )

    # Direct programmes (legacy - some directorates implement programmes directly)
    direct_programme_ids = fields.One2many(
        'kcca.programme',
        'directorate_id',
        string='Primary Programmes',
        help="Programmes where this directorate is the primary implementer"
    )

    # All programmes (direct + through divisions + implementing)
    all_programme_ids = fields.Many2many(
        'kcca.programme',
        string='All Programmes',
        compute='_compute_all_programmes',
        help="All programmes under this directorate (direct, through divisions, and implementing)"
    )

    # Related territorial divisions (for functional directorates)
    related_territorial_divisions = fields.Many2many(
        'kcca.division',
        string='Related Territorial Divisions',
        compute='_compute_related_territorial_divisions',
        help="Territorial divisions that implement programmes this directorate is responsible for"
    )

    kpi_ids = fields.One2many(
        'key.performance.indicator',
        'directorate_id',
        string='Responsible KPIs',
        help="KPIs this directorate is responsible for"
    )
    
    # Computed fields
    division_count = fields.Integer(
        string='Divisions Count',
        compute='_compute_counts',
        store=True
    )

    related_divisions_count = fields.Integer(
        string='Related Territorial Divisions Count',
        compute='_compute_counts',
        store=True
    )

    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_counts',
        store=True
    )

    kpi_count = fields.Integer(
        string='KPIs Count',
        compute='_compute_counts',
        store=True
    )
    
    overall_performance = fields.Float(
        string='Overall Performance (%)',
        compute='_compute_performance',
        store=True,
        help="Overall performance based on KPIs achievement"
    )
    
    @api.depends('division_ids', 'direct_programme_ids', 'implementing_programme_ids', 'division_ids.programme_ids')
    def _compute_all_programmes(self):
        for record in self:
            direct_programmes = record.direct_programme_ids
            division_programmes = record.division_ids.mapped('programme_ids')
            implementing_programmes = record.implementing_programme_ids
            record.all_programme_ids = direct_programmes | division_programmes | implementing_programmes

    @api.depends('implementing_programme_ids')
    def _compute_related_territorial_divisions(self):
        """Compute territorial divisions that implement programmes this directorate is responsible for"""
        for record in self:
            if record.implementing_programme_ids:
                # Find all division-programme relationships for programmes this directorate implements
                division_programme_rels = self.env['division.programme.rel'].search([
                    ('programme_id', 'in', record.implementing_programme_ids.ids)
                ])
                # Get unique territorial divisions
                territorial_divisions = division_programme_rels.mapped('division_id')
                record.related_territorial_divisions = territorial_divisions
            else:
                record.related_territorial_divisions = False
    
    @api.depends('division_ids', 'related_territorial_divisions', 'all_programme_ids', 'kpi_ids')
    def _compute_counts(self):
        for record in self:
            record.division_count = len(record.division_ids)
            record.related_divisions_count = len(record.related_territorial_divisions)
            record.programme_count = len(record.all_programme_ids)
            record.kpi_count = len(record.kpi_ids)
    
    @api.depends('kpi_ids.achievement_percentage')
    def _compute_performance(self):
        for record in self:
            if record.kpi_ids:
                total_achievement = sum(kpi.achievement_percentage for kpi in record.kpi_ids)
                record.overall_performance = total_achievement / len(record.kpi_ids)
            else:
                record.overall_performance = 0.0
    
    def action_view_divisions(self):
        """Action to view divisions"""
        action = self.env.ref('robust_pmis.action_kcca_division').read()[0]
        action['domain'] = [('directorate_id', '=', self.id)]
        action['context'] = {'default_directorate_id': self.id}
        return action

    def action_view_related_territorial_divisions(self):
        """Action to view related territorial divisions"""
        action = self.env.ref('robust_pmis.action_kcca_division').read()[0]
        action['domain'] = [('id', 'in', self.related_territorial_divisions.ids)]
        action['context'] = {
            'search_default_group_by_directorate': 1,
            'default_active': True
        }
        action['name'] = f'Territorial Divisions implementing {self.name} programmes'
        return action
    
    def action_view_programmes(self):
        """Action to view all programmes"""
        action = self.env.ref('robust_pmis.action_kcca_programme').read()[0]
        action['domain'] = [('id', 'in', self.all_programme_ids.ids)]
        return action
    
    def action_view_kpis(self):
        """Action to view responsible KPIs"""
        action = self.env.ref('robust_pmis.action_key_performance_indicator').read()[0]
        action['domain'] = [('directorate_id', '=', self.id)]
        return action
