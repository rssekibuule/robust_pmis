# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PerformanceDashboard(models.Model):
    _name = 'performance.dashboard'
    _description = 'Organization-wide Performance Dashboard'

    name = fields.Char(string='Dashboard', default='Organization Performance')
    total_goals = fields.Integer(string='Total Strategic Goals', compute='_compute_metrics', store=True)
    total_kpis = fields.Integer(string='Total KPIs', compute='_compute_metrics', store=True)
    avg_kpi_performance = fields.Float(string='Average KPI Performance', compute='_compute_metrics', store=True)
    total_programmes = fields.Integer(string='Total Programmes', compute='_compute_metrics', store=True)
    avg_programme_performance = fields.Float(string='Average Programme Performance', compute='_compute_metrics', store=True)
    total_directorates = fields.Integer(string='Total Directorates', compute='_compute_metrics', store=True)
    avg_directorate_performance = fields.Float(string='Average Directorate Performance', compute='_compute_metrics', store=True)
    total_divisions = fields.Integer(string='Total Divisions', compute='_compute_metrics', store=True)
    avg_division_performance = fields.Float(string='Average Division Performance', compute='_compute_metrics', store=True)

    @api.depends()
    def _compute_metrics(self):
        Strategic = self.env['strategic.goal']
        KPI = self.env['key.performance.indicator']
        Programme = self.env['kcca.programme']
        Directorate = self.env['kcca.directorate']
        Division = self.env['kcca.division']
        
        goals = Strategic.search([])
        kpis = KPI.search([])
        programmes = Programme.search([])
        directorates = Directorate.search([])
        divisions = Division.search([])
        
        for rec in self:
            rec.total_goals = len(goals)
            rec.total_kpis = len(kpis)
            
            # Calculate average KPI performance using achievement_percentage
            if rec.total_kpis:
                total_achievement = sum(kpi.achievement_percentage for kpi in kpis)
                rec.avg_kpi_performance = total_achievement / rec.total_kpis
            else:
                rec.avg_kpi_performance = 0.0
            
            rec.total_programmes = len(programmes)
            if rec.total_programmes:
                rec.avg_programme_performance = sum(programmes.mapped('overall_performance')) / rec.total_programmes
            else:
                rec.avg_programme_performance = 0.0
            
            rec.total_directorates = len(directorates)
            if rec.total_directorates:
                rec.avg_directorate_performance = sum(directorates.mapped('overall_performance')) / rec.total_directorates
            else:
                rec.avg_directorate_performance = 0.0
            
            rec.total_divisions = len(divisions)
            if rec.total_divisions:
                rec.avg_division_performance = sum(divisions.mapped('overall_performance')) / rec.total_divisions
            else:
                rec.avg_division_performance = 0.0


class KeyPerformanceIndicator(models.Model):
    _name = 'key.performance.indicator'
    _description = 'Key Performance Indicator'

    name = fields.Char(string='KPI Name', required=True)
    kra_id = fields.Many2one('key.result.area', string='Key Result Area', required=True)
    description = fields.Text(string='Description')
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual')
    ], string='Frequency', default='annual')
    active = fields.Boolean(string='Active', default=True)
    target_value = fields.Float(string='Target Value', help='The target value for this KPI.')
    current_value = fields.Float(string='Current Value', help='The current value achieved for this KPI.')
    achievement_percentage = fields.Float(string='Achievement Percentage', compute='_compute_achievement_percentage', store=True)

    @api.depends('target_value', 'current_value')
    def _compute_achievement_percentage(self):
        for rec in self:
            if rec.target_value:
                rec.achievement_percentage = (rec.current_value / rec.target_value) * 100
            else:
                rec.achievement_percentage = 0.0
