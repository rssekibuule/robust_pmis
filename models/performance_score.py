# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PerformanceScore(models.Model):
    _name = 'performance.score'
    _description = 'Performance Score History'
    _order = 'date desc, id desc'
    _rec_name = 'display_name'

    # Relationships
    indicator_id = fields.Many2one(
        'performance.indicator',
        string='Performance Indicator',
        required=True,
        ondelete='cascade',
        help="Performance indicator being scored"
    )
    
    action_id = fields.Many2one(
        'performance.action',
        string='Related Action',
        ondelete='set null',
        help="Action that created this score record"
    )
    
    # Score data
    date = fields.Date(
        string='Score Date',
        required=True,
        default=fields.Date.context_today,
        help="Date of this score record"
    )
    
    value = fields.Float(
        string='Value',
        required=True,
        help="Indicator value at this date"
    )
    
    achievement_percentage = fields.Float(
        string='Achievement (%)',
        required=True,
        help="Achievement percentage at this date"
    )
    
    target_value = fields.Float(
        string='Target Value',
        help="Target value at the time of scoring"
    )
    
    # Additional information
    notes = fields.Text(
        string='Notes',
        help="Additional notes about this score"
    )
    
    period = fields.Selection([
        ('q1', 'Q1'),
        ('q2', 'Q2'),
        ('q3', 'Q3'),
        ('q4', 'Q4'),
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('annual', 'Annual'),
    ], string='Reporting Period', help="Reporting period for this score")
    
    year = fields.Integer(
        string='Year',
        compute='_compute_year',
        store=True,
        help="Year of the score date"
    )
    
    # Computed fields
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
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
    
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('behind', 'Behind Schedule'),
        ('achieved', 'Achieved'),
    ], string='Status', compute='_compute_status', store=True)
    
    @api.depends('date')
    def _compute_year(self):
        for record in self:
            if record.date:
                record.year = record.date.year
            else:
                record.year = False
    
    @api.depends('indicator_id.name', 'date', 'achievement_percentage')
    def _compute_display_name(self):
        for record in self:
            if record.indicator_id and record.date:
                record.display_name = f"{record.indicator_id.name} - {record.date} ({record.achievement_percentage:.1f}%)"
            else:
                record.display_name = "Performance Score"
    
    @api.depends('achievement_percentage')
    def _compute_status(self):
        for record in self:
            if record.achievement_percentage == 0:
                record.status = 'not_started'
            elif record.achievement_percentage >= 100:
                record.status = 'achieved'
            elif record.achievement_percentage >= 80:
                record.status = 'on_track'
            elif record.achievement_percentage >= 60:
                record.status = 'at_risk'
            else:
                record.status = 'behind'
    
    @api.model
    def create_periodic_scores(self, period_type='quarterly'):
        """Create periodic score records for all active indicators"""
        indicators = self.env['performance.indicator'].search([('active', '=', True)])
        today = fields.Date.context_today(self)
        
        for indicator in indicators:
            # Check if score already exists for this period
            existing_score = self.search([
                ('indicator_id', '=', indicator.id),
                ('date', '=', today),
            ], limit=1)
            
            if not existing_score:
                self.create({
                    'indicator_id': indicator.id,
                    'date': today,
                    'value': indicator.current_value,
                    'achievement_percentage': indicator.achievement_percentage,
                    'target_value': indicator.target_value,
                    'notes': f'Automatic {period_type} score record',
                })
    
    def action_view_indicator(self):
        """Action to view the related indicator"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Performance Indicator',
            'res_model': 'performance.indicator',
            'res_id': self.indicator_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_view_action(self):
        """Action to view the related action"""
        if self.action_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Performance Action',
                'res_model': 'performance.action',
                'res_id': self.action_id.id,
                'view_mode': 'form',
                'target': 'current',
            }

    @api.model
    def cron_weekly_performance_summary(self):
        """Weekly cron job to generate performance summary"""
        from datetime import datetime, timedelta

        # Get last week's date range
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday() + 7)
        week_end = week_start + timedelta(days=6)

        # Generate summary for each directorate
        directorates = self.env['kcca.directorate'].search([('active', '=', True)])

        for directorate in directorates:
            self._generate_weekly_summary(directorate, week_start, week_end)

        return True

    @api.model
    def cron_monthly_performance_report(self):
        """Monthly cron job to generate performance report"""
        from datetime import datetime, timedelta
        import calendar

        # Get last month's date range
        today = datetime.now().date()
        if today.month == 1:
            last_month = 12
            year = today.year - 1
        else:
            last_month = today.month - 1
            year = today.year

        month_start = datetime(year, last_month, 1).date()
        month_end = datetime(year, last_month, calendar.monthrange(year, last_month)[1]).date()

        # Generate monthly report
        self._generate_monthly_report(month_start, month_end)

        return True

    def _generate_weekly_summary(self, directorate, start_date, end_date):
        """Generate weekly performance summary for a directorate"""
        # Get KPIs for this directorate
        kpis = self.env['key.performance.indicator'].search([
            ('directorate_id', '=', directorate.id),
            ('active', '=', True)
        ])

        # Calculate summary statistics
        total_kpis = len(kpis)
        achieved_kpis = len(kpis.filtered(lambda k: k.status == 'achieved'))
        on_track_kpis = len(kpis.filtered(lambda k: k.status == 'on_track'))
        at_risk_kpis = len(kpis.filtered(lambda k: k.status == 'at_risk'))
        behind_kpis = len(kpis.filtered(lambda k: k.status == 'behind'))

        # Send summary email to director
        if directorate.director_id:
            template = self.env.ref('robust_pmis.email_template_weekly_summary', raise_if_not_found=False)
            if template:
                template.with_context(
                    directorate=directorate,
                    start_date=start_date,
                    end_date=end_date,
                    total_kpis=total_kpis,
                    achieved_kpis=achieved_kpis,
                    on_track_kpis=on_track_kpis,
                    at_risk_kpis=at_risk_kpis,
                    behind_kpis=behind_kpis,
                ).send_mail(directorate.director_id.id, force_send=True)

    def _generate_monthly_report(self, start_date, end_date):
        """Generate monthly performance report for KCCA leadership"""
        # Get overall performance statistics
        all_kpis = self.env['key.performance.indicator'].search([('active', '=', True)])
        all_programmes = self.env['kcca.programme'].search([('active', '=', True)])

        # Calculate overall statistics
        overall_kpi_performance = sum(kpi.achievement_percentage for kpi in all_kpis) / len(all_kpis) if all_kpis else 0
        overall_programme_performance = sum(prog.overall_performance for prog in all_programmes) / len(all_programmes) if all_programmes else 0

        # Send to KCCA leadership
        leadership_users = self.env['res.users'].search([
            ('groups_id', 'in', [self.env.ref('robust_pmis.group_kcca_pmis_admin').id])
        ])

        template = self.env.ref('robust_pmis.email_template_monthly_report', raise_if_not_found=False)
        if template:
            for user in leadership_users:
                template.with_context(
                    start_date=start_date,
                    end_date=end_date,
                    overall_kpi_performance=overall_kpi_performance,
                    overall_programme_performance=overall_programme_performance,
                    total_kpis=len(all_kpis),
                    total_programmes=len(all_programmes),
                ).send_mail(user.id, force_send=True)
