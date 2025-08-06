# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KeyPerformanceIndicator(models.Model):
    _name = 'key.performance.indicator'
    _description = 'Key Performance Indicator (KPI)'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='KPI Name',
        required=True,
        tracking=True,
        help="Name of the key performance indicator"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the KPI"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering KPIs"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    kra_id = fields.Many2one(
        'key.result.area',
        string='Key Result Area',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Parent KRA"
    )
    
    # KPI Configuration
    measurement_unit = fields.Char(
        string='Unit of Measurement',
        help="Unit for measuring this KPI (e.g., %, Number, Days, etc.)"
    )
    
    target_value = fields.Float(
        string='Target Value',
        tracking=True,
        help="Target value to achieve for this KPI"
    )
    
    current_value = fields.Float(
        string='Current Value',
        tracking=True,
        help="Current achieved value"
    )
    
    baseline_value = fields.Float(
        string='Baseline Value',
        help="Starting/baseline value"
    )
    
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ], string='Reporting Frequency', default='quarterly')
    
    kpi_type = fields.Selection([
        ('increasing', 'Higher is Better'),
        ('decreasing', 'Lower is Better'),
        ('target', 'Target Value'),
    ], string='KPI Type', default='increasing', required=True)
    
    # Computed fields
    achievement_percentage = fields.Float(
        string='Achievement (%)',
        compute='_compute_achievement',
        store=True,
        help="Percentage of target achieved"
    )
    
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('behind', 'Behind Schedule'),
        ('achieved', 'Achieved'),
    ], string='Status', compute='_compute_status', store=True)
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="Start date for KPI measurement"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="End date for KPI measurement"
    )
    
    # Responsible parties
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        help="Person responsible for this KPI"
    )
    
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Responsible Directorate',
        help="Directorate responsible for this KPI"
    )

    weight = fields.Float(
        string='Weight',
        default=1.0,
        help="Weight of this KPI in calculations"
    )

    # Strategic-Programme Linkage Fields
    thematic_area = fields.Selection([
        ('infrastructure', 'Infrastructure & Transport'),
        ('health', 'Health Services'),
        ('education', 'Education Services'),
        ('economic', 'Economic Development'),
        ('environment', 'Environmental Management'),
        ('governance', 'Governance & Legal'),
        ('finance', 'Revenue & Finance'),
        ('climate', 'Climate & Resilience'),
        ('citizen', 'Citizen Satisfaction'),
        ('organizational', 'Organizational Performance')
    ], string='Thematic Area', help="Thematic area this KPI belongs to", default='organizational')

    # Direct Contribution Mapping
    contributing_programme_indicators = fields.Many2many(
        'performance.indicator',
        'kpi_programme_indicator_rel',
        'strategic_kpi_id',
        'programme_indicator_id',
        string='Contributing Programme Indicators',
        help="Programme-level indicators that contribute to this strategic KPI"
    )

    # Auto-calculation settings
    auto_calculate = fields.Boolean(
        string='Auto Calculate from Programmes',
        default=False,
        help="Automatically calculate this KPI value from programme indicators"
    )

    calculation_method = fields.Selection([
        ('weighted_average', 'Weighted Average'),
        ('sum', 'Sum of Values'),
        ('percentage_complete', 'Percentage of Targets Met'),
        ('milestone_count', 'Count of Milestones Achieved')
    ], string='Calculation Method', help="Method to calculate KPI from programme indicators")
    
    @api.depends('current_value', 'target_value', 'baseline_value', 'kpi_type')
    def _compute_achievement(self):
        for record in self:
            if not record.target_value:
                record.achievement_percentage = 0.0
                continue
                
            if record.kpi_type == 'increasing':
                # Higher is better
                if record.target_value > 0:
                    record.achievement_percentage = min(100.0, (record.current_value / record.target_value) * 100)
                else:
                    record.achievement_percentage = 0.0
            elif record.kpi_type == 'decreasing':
                # Lower is better
                if record.target_value > 0 and record.current_value <= record.target_value:
                    record.achievement_percentage = 100.0
                elif record.baseline_value and record.baseline_value > record.target_value:
                    # Calculate based on improvement from baseline
                    improvement = record.baseline_value - record.current_value
                    target_improvement = record.baseline_value - record.target_value
                    if target_improvement > 0:
                        record.achievement_percentage = min(100.0, (improvement / target_improvement) * 100)
                    else:
                        record.achievement_percentage = 0.0
                else:
                    record.achievement_percentage = 0.0
            else:  # target
                # Target value (exact match is best)
                if record.target_value > 0:
                    deviation = abs(record.current_value - record.target_value)
                    record.achievement_percentage = max(0.0, 100.0 - (deviation / record.target_value) * 100)
                else:
                    record.achievement_percentage = 0.0
    
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

    def write(self, vals):
        """Override write to log value changes and create performance tracking"""
        # Track current values before update
        old_values = {}
        if 'current_value' in vals or 'target_value' in vals:
            for record in self:
                old_values[record.id] = {
                    'current_value': record.current_value,
                    'target_value': record.target_value,
                }

        # Call parent write method
        result = super().write(vals)

        # Log value changes in chatter and audit log
        if 'current_value' in vals:
            for record in self:
                old_current = old_values.get(record.id, {}).get('current_value', 0.0)
                if old_current != record.current_value:
                    # Create audit log entry
                    self.env['audit.log'].log_field_change(
                        record=record,
                        field_name='current_value',
                        old_value=old_current,
                        new_value=record.current_value,
                        action_description=f"KPI value updated via inline editing"
                    )

                    # Post message to chatter
                    record.message_post(
                        body=f"<p><strong>KPI Value Updated</strong></p>"
                             f"<ul>"
                             f"<li>Previous Value: <strong>{old_current} {record.measurement_unit or ''}</strong></li>"
                             f"<li>New Value: <strong>{record.current_value} {record.measurement_unit or ''}</strong></li>"
                             f"<li>Achievement: <strong>{record.achievement_percentage:.1f}%</strong></li>"
                             f"<li>Status: <strong>{dict(record._fields['status'].selection)[record.status]}</strong></li>"
                             f"<li>Updated by: <strong>{self.env.user.name}</strong></li>"
                             f"<li>Update Time: <strong>{fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></li>"
                             f"</ul>",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )

        return result
    
    def update_current_value(self, new_value):
        """Method to update current value and trigger recalculation"""
        self.current_value = new_value
        self._compute_achievement()
        self._compute_status()

    @api.model
    def cron_daily_performance_check(self):
        """Daily cron job to check performance and send alerts"""
        # Find KPIs that are behind schedule or at risk
        at_risk_kpis = self.search([
            ('active', '=', True),
            ('status', 'in', ['behind', 'at_risk'])
        ])

        # Group by directorate for better organization
        directorate_alerts = {}
        for kpi in at_risk_kpis:
            if kpi.directorate_id:
                if kpi.directorate_id not in directorate_alerts:
                    directorate_alerts[kpi.directorate_id] = []
                directorate_alerts[kpi.directorate_id].append(kpi)

        # Send alerts to directorate heads
        for directorate, kpis in directorate_alerts.items():
            if directorate.director_id:
                self._send_performance_alert(directorate.director_id, directorate, kpis)

        return True

    @api.model
    def cron_performance_alerts(self):
        """Send performance alerts for KPIs requiring attention"""
        # Find KPIs with no recent updates (last 30 days)
        from datetime import datetime, timedelta

        thirty_days_ago = datetime.now() - timedelta(days=30)

        # Get KPIs without recent actions
        kpis_without_updates = self.search([
            ('active', '=', True),
            ('responsible_user_id', '!=', False),
        ])

        for kpi in kpis_without_updates:
            # Check if there are recent actions
            recent_actions = self.env['performance.action'].search([
                ('indicator_id', '=', kpi.id),
                ('date', '>=', thirty_days_ago.date()),
            ], limit=1)

            if not recent_actions and kpi.responsible_user_id:
                self._send_update_reminder(kpi.responsible_user_id, kpi)

        return True

    def _send_performance_alert(self, user, directorate, kpis):
        """Send performance alert email to user"""
        template = self.env.ref('robust_pmis.email_template_performance_alert', raise_if_not_found=False)
        if template:
            template.with_context(
                directorate=directorate,
                kpis=kpis,
            ).send_mail(user.id, force_send=True)

    def _send_update_reminder(self, user, kpi):
        """Send update reminder email to responsible user"""
        template = self.env.ref('robust_pmis.email_template_update_reminder', raise_if_not_found=False)
        if template:
            template.with_context(kpi=kpi).send_mail(user.id, force_send=True)

    # Strategic-Programme Linkage Methods
    @api.model
    def _cron_update_strategic_kpis(self):
        """Cron job to update strategic KPIs from programme data"""
        auto_kpis = self.search([('auto_calculate', '=', True)])
        updated_count = 0
        for kpi in auto_kpis:
            if kpi._calculate_from_programme_indicators():
                updated_count += 1
        return updated_count

    def _calculate_from_programme_indicators(self):
        """Calculate strategic KPI value from contributing programme indicators"""
        contributing_indicators = self.contributing_programme_indicators
        if not contributing_indicators:
            return False

        old_value = self.current_value

        if self.calculation_method == 'weighted_average':
            total_weight = sum(contributing_indicators.mapped('contribution_weight'))
            if total_weight > 0:
                weighted_sum = sum(
                    indicator.current_value * indicator.contribution_weight
                    for indicator in contributing_indicators
                )
                self.current_value = weighted_sum / total_weight
            else:
                # If no weights set, use simple average
                self.current_value = sum(contributing_indicators.mapped('current_value')) / len(contributing_indicators)

        elif self.calculation_method == 'sum':
            self.current_value = sum(contributing_indicators.mapped('current_value'))

        elif self.calculation_method == 'percentage_complete':
            completed = contributing_indicators.filtered(lambda x: x.achievement_percentage >= 100)
            self.current_value = (len(completed) / len(contributing_indicators)) * 100

        elif self.calculation_method == 'milestone_count':
            self.current_value = len(contributing_indicators.filtered(lambda x: x.achievement_percentage >= 80))

        # Return True if value changed
        return old_value != self.current_value

    def get_programme_performance_summary(self):
        """Get performance summary of programmes contributing to this KPI"""
        programme_data = []

        # Get programmes through strategic objective relationships
        strategic_objective = self.kra_id.strategic_objective_id
        if strategic_objective:
            for programme in strategic_objective.programme_ids:
                indicators = programme.performance_indicator_ids.filtered(
                    lambda x: self in x.strategic_kpi_ids
                )
                if indicators:
                    avg_achievement = sum(indicators.mapped('achievement_percentage')) / len(indicators)
                    programme_data.append({
                        'programme': programme.name,
                        'indicators_count': len(indicators),
                        'avg_achievement': avg_achievement,
                        'status': 'on_track' if avg_achievement >= 80 else 'at_risk' if avg_achievement >= 50 else 'behind'
                    })

        return programme_data

    def action_view_contributing_indicators(self):
        """Action to view contributing programme indicators"""
        action = self.env.ref('robust_pmis.action_performance_indicator').read()[0]
        action['domain'] = [('id', 'in', self.contributing_programme_indicators.ids)]
        action['context'] = {'default_strategic_kpi_ids': [(4, self.id)]}
        action['name'] = f'Programme Indicators Contributing to {self.name}'
        return action
