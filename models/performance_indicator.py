# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PerformanceIndicator(models.Model):
    _name = 'performance.indicator'
    _description = 'Performance Indicator'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Performance Indicator',
        required=True,
        tracking=True,
        help="Name of the performance indicator"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the performance indicator"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering indicators"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships - Performance Indicator can be linked to Programme directly OR to Intermediate Outcome
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        ondelete='cascade',
        tracking=True,
        help="Programme this indicator belongs to (if direct link)"
    )
    
    outcome_id = fields.Many2one(
        'intermediate.outcome',
        string='Intermediate Outcome',
        ondelete='cascade',
        tracking=True,
        help="Intermediate outcome this indicator measures (if through outcome)"
    )

    output_id = fields.Many2one(
        'output',
        string='Output',
        ondelete='cascade',
        tracking=True,
        help="Output this indicator measures (if through output)"
    )

    piap_action_id = fields.Many2one(
        'piap.action',
        string='PIAP Action',
        ondelete='cascade',
        tracking=True,
        help="PIAP Action this indicator measures (if through PIAP action)"
    )
    
    # Actions that update this indicator
    action_ids = fields.One2many(
        'performance.action',
        'indicator_id',
        string='Actions',
        help="Actions that update this performance indicator"
    )
    
    # Indicator Configuration
    measurement_unit = fields.Char(
        string='Unit of Measurement',
        help="Unit for measuring this indicator (e.g., %, Number, Days, etc.)"
    )
    
    target_value = fields.Float(
        string='Target Value',
        tracking=True,
        help="Target value to achieve for this indicator"
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

    # Multi-year targets
    target_fy2022_23 = fields.Float(
        string='Target FY2022/23',
        help="Target value for FY2022/23"
    )

    target_fy2023_24 = fields.Float(
        string='Target FY2023/24',
        help="Target value for FY2023/24"
    )

    target_fy2024_25 = fields.Float(
        string='Target FY2024/25',
        help="Target value for FY2024/25"
    )

    target_fy2025_26 = fields.Float(
        string='Target FY2025/26',
        help="Target value for FY2025/26"
    )

    target_fy2026_27 = fields.Float(
        string='Target FY2026/27',
        help="Target value for FY2026/27"
    )

    target_fy2027_28 = fields.Float(
        string='Target FY2027/28',
        help="Target value for FY2027/28"
    )

    target_fy2028_29 = fields.Float(
        string='Target FY2028/29',
        help="Target value for FY2028/29"
    )

    target_fy2029_30 = fields.Float(
        string='Target FY2029/30',
        help="Target value for FY2029/30"
    )

    # Multi-year actual values
    actual_fy2022_23 = fields.Float(
        string='Actual FY2022/23',
        help="Actual value for FY2022/23"
    )

    actual_fy2023_24 = fields.Float(
        string='Actual FY2023/24',
        help="Actual value for FY2023/24"
    )

    actual_fy2024_25 = fields.Float(
        string='Actual FY2024/25',
        help="Actual value for FY2024/25"
    )

    actual_fy2025_26 = fields.Float(
        string='Actual FY2025/26',
        help="Actual value for FY2025/26"
    )

    actual_fy2026_27 = fields.Float(
        string='Actual FY2026/27',
        help="Actual value for FY2026/27"
    )

    actual_fy2027_28 = fields.Float(
        string='Actual FY2027/28',
        help="Actual value for FY2027/28"
    )

    actual_fy2028_29 = fields.Float(
        string='Actual FY2028/29',
        help="Actual value for FY2028/29"
    )

    actual_fy2029_30 = fields.Float(
        string='Actual FY2029/30',
        help="Actual value for FY2029/30"
    )

    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
    ], string='Reporting Frequency', default='quarterly')
    
    indicator_type = fields.Selection([
        ('increasing', 'Higher is Better'),
        ('decreasing', 'Lower is Better'),
        ('target', 'Target Value'),
    ], string='Indicator Type', default='increasing', required=True)

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
    ], string='Thematic Area', help="Thematic area this indicator belongs to")

    # Strategic KPI Linkage
    strategic_kpi_ids = fields.Many2many(
        'key.performance.indicator',
        'kpi_programme_indicator_rel',
        'programme_indicator_id',
        'strategic_kpi_id',
        string='Linked Strategic KPIs',
        help="Strategic KPIs this programme indicator contributes to"
    )

    # Contribution settings
    contribution_weight = fields.Float(
        string='Contribution Weight (%)',
        default=0.0,
        help="Weight of this indicator in strategic KPI calculation (0-100%)"
    )

    impact_relationship = fields.Selection([
        ('direct', 'Direct Impact'),
        ('indirect', 'Indirect Impact'),
        ('supporting', 'Supporting Impact')
    ], string='Impact Relationship', help="Type of impact relationship with strategic KPIs")

    # Results Chain Level
    results_chain_level = fields.Selection([
        ('activity', 'Activity Level'),
        ('output', 'Output Level'),
        ('outcome', 'Outcome Level'),
        ('impact', 'Impact Level')
    ], string='Results Chain Level', help="Level in the results chain hierarchy")

    # Target Cascade
    parent_strategic_kpi_id = fields.Many2one(
        'key.performance.indicator',
        string='Parent Strategic KPI',
        help="Strategic KPI this programme indicator contributes to"
    )

    target_allocation_percentage = fields.Float(
        string='Target Allocation %',
        default=0.0,
        help="Percentage of strategic target allocated to this programme indicator"
    )

    cascaded_target = fields.Float(
        string='Cascaded Target',
        compute='_compute_cascaded_target',
        store=True,
        help="Target cascaded from strategic KPI"
    )

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

    achievement_level = fields.Selection([
        ('high', 'High (≥80%)'),
        ('medium', 'Medium (50-79%)'),
        ('low', 'Low (<50%)'),
        ('none', 'Not Started (0%)'),
    ], string='Achievement Level', compute='_compute_achievement_level', store=True)
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        help="Start date for indicator measurement"
    )
    
    end_date = fields.Date(
        string='End Date',
        help="End date for indicator measurement"
    )
    
    # Responsible parties
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        help="Person responsible for this indicator"
    )
    
    # Computed parent programme
    parent_programme_id = fields.Many2one(
        'kcca.programme',
        string='Parent Programme',
        compute='_compute_parent_programme',
        store=True,
        help="The ultimate parent programme"
    )
    
    @api.depends('programme_id', 'outcome_id.programme_id', 'output_id.programme_id', 'piap_action_id.output_id.programme_id')
    def _compute_parent_programme(self):
        for record in self:
            if record.programme_id:
                record.parent_programme_id = record.programme_id
            elif record.outcome_id and record.outcome_id.programme_id:
                record.parent_programme_id = record.outcome_id.programme_id
            elif record.output_id and record.output_id.programme_id:
                record.parent_programme_id = record.output_id.programme_id
            elif record.piap_action_id and record.piap_action_id.output_id and record.piap_action_id.output_id.programme_id:
                record.parent_programme_id = record.piap_action_id.output_id.programme_id
            else:
                record.parent_programme_id = False
    
    @api.depends('current_value', 'target_value', 'baseline_value', 'indicator_type')
    def _compute_achievement(self):
        for record in self:
            if not record.target_value:
                record.achievement_percentage = 0.0
                continue
                
            if record.indicator_type == 'increasing':
                # Higher is better
                if record.target_value > 0:
                    record.achievement_percentage = min(100.0, (record.current_value / record.target_value) * 100)
                else:
                    record.achievement_percentage = 0.0
            elif record.indicator_type == 'decreasing':
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

    @api.depends('achievement_percentage')
    def _compute_achievement_level(self):
        for record in self:
            if record.achievement_percentage == 0:
                record.achievement_level = 'none'
            elif record.achievement_percentage >= 80:
                record.achievement_level = 'high'
            elif record.achievement_percentage >= 50:
                record.achievement_level = 'medium'
            else:
                record.achievement_level = 'low'

    def write(self, vals):
        """Override write to log value changes and create performance actions"""
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

        # Create performance actions and audit logs for value changes
        if 'current_value' in vals:
            for record in self:
                old_current = old_values.get(record.id, {}).get('current_value', 0.0)
                if old_current != record.current_value:
                    # Create performance action to log the change
                    self.env['performance.action'].create({
                        'name': f"Value Update: {record.name}",
                        'description': f"Current value updated from {old_current} to {record.current_value}",
                        'date': fields.Date.context_today(self),
                        'indicator_id': record.id,
                        'action_type': 'update',
                        'previous_value': old_current,
                        'new_value': record.current_value,
                        'progress_notes': f"Value updated by {self.env.user.name} via inline editing",
                        'state': 'approved',  # Auto-approve inline edits
                        'approved_by_id': self.env.user.id,
                    })

                    # Create performance score record
                    self.env['performance.score'].create({
                        'indicator_id': record.id,
                        'date': fields.Date.context_today(self),
                        'value': record.current_value,
                        'achievement_percentage': record.achievement_percentage,
                        'target_value': record.target_value,
                        'notes': f"Inline edit by {self.env.user.name}",
                    })

                    # Create audit log entry
                    self.env['audit.log'].log_field_change(
                        record=record,
                        field_name='current_value',
                        old_value=old_current,
                        new_value=record.current_value,
                        action_description=f"Performance Indicator value updated via inline editing"
                    )

                    # Post message to chatter
                    record.message_post(
                        body=f"<p><strong>Value Updated</strong></p>"
                             f"<ul>"
                             f"<li>Previous Value: <strong>{old_current} {record.measurement_unit or ''}</strong></li>"
                             f"<li>New Value: <strong>{record.current_value} {record.measurement_unit or ''}</strong></li>"
                             f"<li>Achievement: <strong>{record.achievement_percentage:.1f}%</strong></li>"
                             f"<li>Updated by: <strong>{self.env.user.name}</strong></li>"
                             f"</ul>",
                        subtype_id=self.env.ref('mail.mt_note').id
                    )

        return result
    
    @api.constrains('programme_id', 'outcome_id')
    def _check_parent_constraint(self):
        for record in self:
            if not record.programme_id and not record.outcome_id:
                raise ValidationError(_("Performance Indicator must be linked to either a Programme or Intermediate Outcome."))
            if record.programme_id and record.outcome_id:
                raise ValidationError(_("Performance Indicator cannot be linked to both Programme and Intermediate Outcome. Choose one."))
    
    @api.depends('parent_strategic_kpi_id.target_value', 'target_allocation_percentage')
    def _compute_cascaded_target(self):
        """Compute cascaded target from parent strategic KPI"""
        for record in self:
            if record.parent_strategic_kpi_id and record.target_allocation_percentage:
                record.cascaded_target = (
                    record.parent_strategic_kpi_id.target_value *
                    record.target_allocation_percentage / 100
                )
            else:
                record.cascaded_target = 0.0

    def action_view_actions(self):
        """Action to view actions that update this indicator"""
        action = self.env.ref('robust_pmis.action_performance_action').read()[0]
        action['domain'] = [('indicator_id', '=', self.id)]
        action['context'] = {'default_indicator_id': self.id}
        return action
