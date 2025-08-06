# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import calendar


class QuarterlyReportWizard(models.TransientModel):
    _name = 'quarterly.report.wizard'
    _description = 'Quarterly Performance Report Wizard'

    name = fields.Char(
        string='Report Name',
        required=True,
        compute='_compute_name',
        store=True
    )
    
    year = fields.Integer(
        string='Year',
        required=True,
        default=lambda self: date.today().year
    )
    
    quarter = fields.Selection([
        ('q1', 'Q1 (Jan-Mar)'),
        ('q2', 'Q2 (Apr-Jun)'),
        ('q3', 'Q3 (Jul-Sep)'),
        ('q4', 'Q4 (Oct-Dec)'),
    ], string='Quarter', required=True, default='q1')
    
    report_type = fields.Selection([
        ('strategic', 'Strategic Goals Report'),
        ('directorate', 'Directorate Performance Report'),
        ('programme', 'Programme Performance Report'),
        ('comprehensive', 'Comprehensive Report'),
    ], string='Report Type', default='comprehensive', required=True)
    
    directorate_ids = fields.Many2many(
        'kcca.directorate',
        string='Directorates',
        help="Select specific directorates (leave empty for all)"
    )
    
    programme_ids = fields.Many2many(
        'kcca.programme',
        string='Programmes',
        help="Select specific programmes (leave empty for all)"
    )
    
    include_charts = fields.Boolean(
        string='Include Charts',
        default=True,
        help="Include performance charts in the report"
    )
    
    include_trends = fields.Boolean(
        string='Include Trend Analysis',
        default=True,
        help="Include trend analysis compared to previous quarters"
    )
    
    include_recommendations = fields.Boolean(
        string='Include Recommendations',
        default=True,
        help="Include performance improvement recommendations"
    )
    
    @api.depends('year', 'quarter')
    def _compute_name(self):
        for record in self:
            if record.year and record.quarter:
                quarter_name = dict(record._fields['quarter'].selection)[record.quarter]
                record.name = f"Performance Report - {quarter_name} {record.year}"
            else:
                record.name = "Performance Report"
    
    def _get_quarter_dates(self):
        """Get start and end dates for the selected quarter"""
        quarter_months = {
            'q1': (1, 3),
            'q2': (4, 6),
            'q3': (7, 9),
            'q4': (10, 12),
        }
        
        start_month, end_month = quarter_months[self.quarter]
        start_date = date(self.year, start_month, 1)
        end_date = date(self.year, end_month, calendar.monthrange(self.year, end_month)[1])
        
        return start_date, end_date
    
    def action_generate_report(self):
        """Generate the quarterly performance report"""
        start_date, end_date = self._get_quarter_dates()
        
        # Create performance score records for the quarter if they don't exist
        self._create_quarterly_scores(start_date, end_date)
        
        # Generate the appropriate report based on type
        if self.report_type == 'strategic':
            return self._generate_strategic_report(start_date, end_date)
        elif self.report_type == 'directorate':
            return self._generate_directorate_report(start_date, end_date)
        elif self.report_type == 'programme':
            return self._generate_programme_report(start_date, end_date)
        else:
            return self._generate_comprehensive_report(start_date, end_date)
    
    def _create_quarterly_scores(self, start_date, end_date):
        """Create quarterly performance score records"""
        # Create scores for KPIs
        kpis = self.env['key.performance.indicator'].search([('active', '=', True)])
        for kpi in kpis:
            existing_score = self.env['performance.score'].search([
                ('indicator_id', '=', kpi.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('period', '=', self.quarter),
            ], limit=1)
            
            if not existing_score:
                self.env['performance.score'].create({
                    'indicator_id': kpi.id,
                    'date': end_date,
                    'value': kpi.current_value,
                    'achievement_percentage': kpi.achievement_percentage,
                    'target_value': kpi.target_value,
                    'period': self.quarter,
                    'notes': f'Quarterly score for {self.quarter.upper()} {self.year}',
                })
    
    def _generate_strategic_report(self, start_date, end_date):
        """Generate strategic goals performance report"""
        goals = self.env['strategic.goal'].search([('active', '=', True)])
        
        return {
            'type': 'ir.actions.report',
            'report_name': 'robust_pmis.report_quarterly_strategic_performance',
            'report_type': 'qweb-pdf',
            'data': {
                'goals': goals.ids,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'quarter': self.quarter,
                'year': self.year,
                'include_charts': self.include_charts,
                'include_trends': self.include_trends,
            },
            'context': self.env.context,
        }
    
    def _generate_directorate_report(self, start_date, end_date):
        """Generate directorate performance report"""
        directorates = self.directorate_ids or self.env['kcca.directorate'].search([('active', '=', True)])
        
        return {
            'type': 'ir.actions.report',
            'report_name': 'robust_pmis.report_quarterly_directorate_performance',
            'report_type': 'qweb-pdf',
            'data': {
                'directorates': directorates.ids,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'quarter': self.quarter,
                'year': self.year,
                'include_charts': self.include_charts,
                'include_trends': self.include_trends,
            },
            'context': self.env.context,
        }
    
    def _generate_programme_report(self, start_date, end_date):
        """Generate programme performance report"""
        programmes = self.programme_ids or self.env['kcca.programme'].search([('active', '=', True)])
        
        return {
            'type': 'ir.actions.report',
            'report_name': 'robust_pmis.report_quarterly_programme_performance',
            'report_type': 'qweb-pdf',
            'data': {
                'programmes': programmes.ids,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'quarter': self.quarter,
                'year': self.year,
                'include_charts': self.include_charts,
                'include_trends': self.include_trends,
            },
            'context': self.env.context,
        }
    
    def _generate_comprehensive_report(self, start_date, end_date):
        """Generate comprehensive performance report"""
        return {
            'type': 'ir.actions.report',
            'report_name': 'robust_pmis.report_quarterly_comprehensive_performance',
            'report_type': 'qweb-pdf',
            'data': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'quarter': self.quarter,
                'year': self.year,
                'include_charts': self.include_charts,
                'include_trends': self.include_trends,
                'include_recommendations': self.include_recommendations,
            },
            'context': self.env.context,
        }
